#!/usr/bin/env python3
"""
run_rekt_all.py
===============
Batch Cobol-REKT runner for every COBOL source file under app/cbl/.

For each program that does not yet have a REKT report directory the script:
  1. Invokes smojol-cli with the WRITE_CFG command.
  2. On success, immediately runs extract_cfg_summary.py to build
     validation/structure/<PROG>_cfg.json.

Usage
-----
  py -3 validation/run_rekt_all.py                  # skip already-done
  py -3 validation/run_rekt_all.py --force          # re-run everything
  py -3 validation/run_rekt_all.py --only CBTRN02C CBTRN03C
  py -3 validation/run_rekt_all.py --dry-run        # print commands only
  py -3 validation/run_rekt_all.py --jar path/to/smojol-cli.jar
  py -3 validation/run_rekt_all.py --timeout 600    # seconds per program

Environment
-----------
  SMOJOL_JAR    Full path to smojol-cli.jar     (overrides auto-detect)
  DIALECT_JAR   Full path to dialect-idms.jar   (overrides auto-detect)

JAR auto-detect order
---------------------
  smojol-cli.jar:
    1. SMOJOL_JAR env var
    2. --jar CLI argument
    3. Paths in CANDIDATE_JARS below

  dialect-idms.jar:
    1. DIALECT_JAR env var
    2. Paths in CANDIDATE_DIALECT_JARS below

Quick start (PowerShell)
------------------------
  $env:SMOJOL_JAR  = "C:\\work\\cobol-rekt\\smojol-cli\\target\\smojol-cli.jar"
  $env:DIALECT_JAR = "C:\\work\\cobol-rekt\\che-che4z-lsp-for-cobol-integration\\server\\dialect-idms\\target\\dialect-idms.jar"
  py -3 validation/run_rekt_all.py --dry-run
  py -3 validation/run_rekt_all.py

Exit codes
----------
  0   All targeted programs succeeded or were already skipped.
  1   One or more programs failed or timed out.
  2   smojol-cli JAR or dialect JAR could not be located.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------
ROOT         = Path(__file__).parent.parent.resolve()
SRC_DIR      = ROOT / "app" / "cbl"
COPY_DIR     = ROOT / "app" / "cpy"
COPY_BMS_DIR = ROOT / "app" / "cpy-bms"
REKT_DIR     = ROOT / "validation" / "rekt"
EXTRACT      = ROOT / "validation" / "extract_cfg_summary.py"

# ---------------------------------------------------------------------------
# JAR candidate paths
# ---------------------------------------------------------------------------
_COBOL_REKT = Path(r"C:\work\cobol-rekt")

CANDIDATE_JARS = [
    _COBOL_REKT / "smojol-cli" / "target" / "smojol-cli.jar",
    ROOT  / "tools" / "smojol-cli.jar",
    ROOT  / "tools" / "cobol-rekt" / "smojol-cli.jar",
    ROOT  / "smojol-cli.jar",
    Path.home() / "tools" / "smojol-cli.jar",
    Path.home() / "cobol-rekt" / "smojol-cli.jar",
]

CANDIDATE_DIALECT_JARS = [
    _COBOL_REKT / "che-che4z-lsp-for-cobol-integration" / "server" / "dialect-idms" / "target" / "dialect-idms.jar",
    ROOT  / "tools" / "dialect-idms.jar",
    ROOT  / "tools" / "cobol-rekt" / "dialect-idms.jar",
    ROOT  / "dialect-idms.jar",
    Path.home() / "tools" / "dialect-idms.jar",
    Path.home() / "cobol-rekt" / "dialect-idms.jar",
]

# Minimum JAR size — rejects archive-tmp stubs.
_MIN_JAR_BYTES = 1_000_000

DEFAULT_TIMEOUT = 300  # seconds per program

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------
_USE_COLOR = sys.stdout.isatty()

def _c(code, text):
    return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text

OK      = lambda t: _c("32", t)
FAIL    = lambda t: _c("31", t)
SKIP    = lambda t: _c("33", t)
INFO    = lambda t: _c("36", t)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_sources():
    return sorted(p for p in SRC_DIR.iterdir() if p.suffix.lower() == ".cbl")

def prog_name(src):
    return src.stem.upper()

def report_dir(prog):
    return REKT_DIR / f"{prog}.cbl.report"

def cfg_json(prog):
    return ROOT / "validation" / "structure" / f"{prog}_cfg.json"


def locate_jar(candidates, env_var, arg_val, label):
    """Find a valid JAR from env var, CLI arg, or candidate list."""
    def _check(p, source):
        p = Path(p)
        if not p.exists():
            return None
        if p.stat().st_size < _MIN_JAR_BYTES:
            print(FAIL(f"[JAR] Rejected {p} ({p.stat().st_size // 1024} KB) -- too small, likely a stub"))
            return None
        print(INFO(f"[JAR] {label} ({source}): {p}"))
        return p

    env = os.environ.get(env_var)
    if env:
        return _check(env, f"{env_var} env")
    if arg_val:
        return _check(arg_val, "--jar")
    for c in candidates:
        r = _check(c, "auto")
        if r:
            return r
    return None


def build_rekt_cmd(jar, dialect_jar, src, prog):
    """
    Constructs the smojol-cli invocation.

    Matches the pattern from cobol-rekt/scripts/aws-carddemo.sh:

      java -jar smojol-cli.jar run <PROG>.cbl
        --commands="WRITE_CFG"
        --srcDir          app/cbl
        --copyBooksDir    app/cpy,app/cpy-bms
        --dialectJarPath  <dialect-idms.jar>
        --dialect         COBOL
        --reportDir       validation/rekt
        --generation=PARAGRAPH

    Output lands at: validation/rekt/<PROG>.cbl.report/cfg/cfg-<PROG>.cbl.json
    """
    copybooks = str(COPY_DIR)
    if COPY_BMS_DIR.exists():
        copybooks += f",{COPY_BMS_DIR}"

    return [
        "java", "-jar", str(jar),
        "run", f"{prog}.cbl",
        "--commands=WRITE_CFG",
        "--srcDir",         str(SRC_DIR),
        "--copyBooksDir",   copybooks,
        "--dialectJarPath", str(dialect_jar),
        "--dialect",        "COBOL",
        "--reportDir",      str(REKT_DIR),
        "--generation=PARAGRAPH",
    ]


def run_extract(prog, dry_run):
    cmd = [sys.executable, str(EXTRACT), prog]
    if dry_run:
        print(INFO(f"  [DRY] {' '.join(cmd)}"))
        return True
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Per-program runner
# ---------------------------------------------------------------------------

def run_program(jar, dialect_jar, src, *, force, dry_run, timeout):
    prog   = prog_name(src)
    rdir   = report_dir(prog)
    cfjson = cfg_json(prog)

    if not force and rdir.exists() and cfjson.exists():
        print(SKIP(f"[SKIP] {prog}: report dir + cfg.json already exist"))
        return "skipped"

    cmd      = build_rekt_cmd(jar, dialect_jar, src, prog)
    size_kb  = src.stat().st_size // 1024

    if dry_run:
        print(INFO(f"[DRY]  {prog}  ({size_kb} KB)"))
        print(INFO(f"       {' '.join(cmd)}"))
        run_extract(prog, dry_run=True)
        return "dry"

    print(INFO(f"[REKT] {prog}  ({size_kb} KB) ..."))

    try:
        result = subprocess.run(cmd, cwd=ROOT, timeout=timeout)
    except subprocess.TimeoutExpired:
        print(FAIL(f"[TIMEOUT] {prog}: exceeded {timeout}s -- use --timeout N to increase"))
        return "timeout"
    except FileNotFoundError:
        print(FAIL("[ERROR] 'java' not found -- is a JDK on PATH?"))
        return "failed"

    if result.returncode != 0:
        print(FAIL(f"[FAIL] {prog}: smojol-cli exited {result.returncode}"))
        return "failed"

    # Verify REKT actually wrote the expected output
    expected_cfg = rdir / "cfg" / f"cfg-{prog}.cbl.json"
    if not expected_cfg.exists():
        print(FAIL(f"[FAIL] {prog}: exit 0 but {expected_cfg.name} not found"))
        print(FAIL(f"       Expected at: {expected_cfg}"))
        return "failed"

    print(OK(f"[REKT-OK] {prog}: cfg JSON found"))

    ok = run_extract(prog, dry_run=False)
    if ok:
        print(OK(f"[CFG-OK]  {prog}: structure/{prog}_cfg.json written"))
        return "ok"
    else:
        print(FAIL(f"[CFG-FAIL] {prog}: extract_cfg_summary.py failed"))
        return "failed"


# ---------------------------------------------------------------------------
# CLI parser
# ---------------------------------------------------------------------------

def parse_args():
    args = sys.argv[1:]
    opts = {"force": False, "dry_run": False, "jar": None,
            "only": [], "timeout": DEFAULT_TIMEOUT}
    i = 0
    while i < len(args):
        a = args[i]
        if   a == "--force":                opts["force"]   = True
        elif a in ("--dry-run", "--dry"):   opts["dry_run"] = True
        elif a == "--jar":    i += 1;        opts["jar"]     = args[i]
        elif a == "--timeout":i += 1;        opts["timeout"] = int(args[i])
        elif a == "--only":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                opts["only"].append(args[i].upper()); i += 1
            continue
        elif a in ("--help", "-h"):
            print(textwrap.dedent(__doc__).strip()); sys.exit(0)
        i += 1
    return opts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    opts = parse_args()

    if not opts["dry_run"]:
        jar = locate_jar(CANDIDATE_JARS, "SMOJOL_JAR", opts["jar"], "smojol-cli")
        if jar is None:
            print(FAIL("\n[ERROR] Cannot locate smojol-cli.jar."))
            print(      "  Set $env:SMOJOL_JAR or use --jar PATH")
            print(      "  Searched:")
            for p in CANDIDATE_JARS: print(f"    {p}")
            return 2

        dialect_jar = locate_jar(CANDIDATE_DIALECT_JARS, "DIALECT_JAR", None, "dialect-idms")
        if dialect_jar is None:
            print(FAIL("\n[ERROR] Cannot locate dialect-idms.jar."))
            print(      "  Set $env:DIALECT_JAR or place the jar in one of:")
            for p in CANDIDATE_DIALECT_JARS: print(f"    {p}")
            return 2
    else:
        jar = Path("smojol-cli.jar")
        dialect_jar = Path("dialect-idms.jar")

    sources = find_sources()
    if opts["only"]:
        sources = [s for s in sources if prog_name(s) in opts["only"]]
        if not sources:
            print(FAIL(f"[ERROR] --only matched no files: {opts['only']}")); return 1

    total   = len(sources)
    already = sum(1 for s in sources
                  if report_dir(prog_name(s)).exists() and cfg_json(prog_name(s)).exists())
    print(INFO(f"[INFO] {total} source file(s) targeted, {already} already done (will skip)"))
    print()

    results = {}
    for src in sources:
        status = run_program(
            jar, dialect_jar, src,
            force=opts["force"],
            dry_run=opts["dry_run"],
            timeout=opts["timeout"],
        )
        results[prog_name(src)] = status
        print()

    # ---- summary table ---------------------------------------------------
    col_w   = max(len(p) for p in results) + 2
    divider = "-" * 52
    labels  = {"ok": "PASS", "skipped": "SKIP", "failed": "FAIL",
               "timeout": "TIMEOUT", "dry": "DRY"}
    colours = {"ok": OK, "skipped": SKIP, "failed": FAIL,
               "timeout": FAIL, "dry": INFO}
    counts  = {k: 0 for k in labels}

    print(divider)
    print(f"{'Program':<{col_w}}  Status")
    print(divider)
    for prog, status in sorted(results.items()):
        counts[status] = counts.get(status, 0) + 1
        colour = colours.get(status, INFO)
        print(f"{prog:<{col_w}}  {colour(labels.get(status, status))}")
    print(divider)
    print(f"  ok={counts['ok']}  skipped={counts['skipped']}  "
          f"failed={counts['failed']}  timeout={counts['timeout']}")
    print(divider)

    failures = [p for p, s in results.items() if s in ("failed", "timeout")]
    if failures:
        print(FAIL("\nSome programs failed. Re-run only failures with:"))
        print(FAIL(f"  py -3 validation/run_rekt_all.py --only {' '.join(failures)}"))
        return 1

    if opts["dry_run"]:
        print(INFO("\nDry run complete -- no files written."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
