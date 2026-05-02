#!/usr/bin/env python3
"""
run_rekt_all.py
===============
Batch Cobol-REKT runner for every COBOL source file under app/cbl/.

For each program that does not yet have a REKT report directory the script:
  1. Invokes smojol-cli with the GENERATE_CFG task.
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
  SMOJOL_JAR   Full path to smojol-cli.jar (highest priority).

JAR auto-detect order
----------------------
  1. SMOJOL_JAR environment variable
  2. --jar CLI argument
  3. Paths in CANDIDATE_JARS below

  Use the REAL jar (75 MB), not the archive-tmp stub (22 KB):
    C:\\work\\cobol-rekt\\smojol-cli\\target\\smojol-cli.jar

Quick start (PowerShell)
------------------------
  $env:SMOJOL_JAR = "C:\\work\\cobol-rekt\\smojol-cli\\target\\smojol-cli.jar"
  py -3 validation/run_rekt_all.py --dry-run
  py -3 validation/run_rekt_all.py

Exit codes
----------
  0   All targeted programs succeeded or were already skipped.
  1   One or more programs failed or timed out.
  2   smojol-cli JAR could not be located.
"""

import os
import subprocess
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Repo layout
# ---------------------------------------------------------------------------
ROOT      = Path(__file__).parent.parent.resolve()
SRC_DIR   = ROOT / "app" / "cbl"
COPY_DIR  = ROOT / "app" / "cpy"
REKT_DIR  = ROOT / "validation" / "rekt"
EXTRACT   = ROOT / "validation" / "extract_cfg_summary.py"

# ---------------------------------------------------------------------------
# JAR candidate paths (tried in order when env var / --jar not provided)
# ---------------------------------------------------------------------------
CANDIDATE_JARS = [
    # Developer machine — confirmed location
    Path(r"C:\work\cobol-rekt\smojol-cli\target\smojol-cli.jar"),
    # Repo-local copies (convenient to drop the jar here)
    ROOT / "tools" / "smojol-cli.jar",
    ROOT / "tools" / "cobol-rekt" / "smojol-cli.jar",
    ROOT / "smojol-cli.jar",
    # Home-directory installs
    Path.home() / "tools" / "smojol-cli.jar",
    Path.home() / "cobol-rekt" / "smojol-cli.jar",
]

# Minimum JAR size in bytes — rejects the 22 KB archive-tmp stub.
_MIN_JAR_BYTES = 1_000_000

DEFAULT_TIMEOUT = 300  # seconds per program

# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------
_USE_COLOR = sys.stdout.isatty() and os.environ.get("TERM", "dumb") != "dumb"

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _USE_COLOR else text

OK   = lambda t: _c("32", t)
FAIL = lambda t: _c("31", t)
SKIP = lambda t: _c("33", t)
INFO = lambda t: _c("36", t)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_sources() -> list:
    """All .cbl / .CBL files in app/cbl/, sorted by name."""
    return sorted(p for p in SRC_DIR.iterdir() if p.suffix.lower() == ".cbl")


def prog_name(src: Path) -> str:
    return src.stem.upper()


def report_dir(prog: str) -> Path:
    return REKT_DIR / f"{prog}.cbl.report"


def cfg_json(prog: str) -> Path:
    return ROOT / "validation" / "structure" / f"{prog}_cfg.json"


def locate_jar(jar_arg) -> Path | None:
    """Return a valid, non-stub JAR path or None."""
    def _check(p: Path, label: str):
        if not p.exists():
            return None
        if p.stat().st_size < _MIN_JAR_BYTES:
            print(FAIL(
                f"[JAR] Rejected {p} ({p.stat().st_size // 1024} KB) — "
                f"looks like the archive-tmp stub, not the real JAR."
            ))
            return None
        print(INFO(f"[JAR] {label}: {p}"))
        return p

    env = os.environ.get("SMOJOL_JAR")
    if env:
        return _check(Path(env), "SMOJOL_JAR env")

    if jar_arg:
        return _check(Path(jar_arg), "--jar")

    for candidate in CANDIDATE_JARS:
        result = _check(candidate, "auto-detected")
        if result:
            return result

    return None


def build_rekt_cmd(jar: Path, src: Path, prog: str) -> list:
    """
    Build the smojol-cli invocation.

    smojol-cli command shape (matches aws-carddemo.sh):

      java -jar smojol-cli.jar
        GENERATE_CFG
        --programs          <PROG>.cbl
        --cobol-collection-path  app/cbl
        --copybook-collection-path  app/cpy
        --output-path       validation/rekt
        --dialect           IDMS          # omit if not needed; safe default

    REKT creates:  validation/rekt/<PROG>.cbl.report/cfg/cfg-<PROG>.cbl.json
    """
    return [
        "java", "-jar", str(jar),
        "GENERATE_CFG",
        "--programs",                  f"{prog}.cbl",
        "--cobol-collection-path",     str(SRC_DIR),
        "--copybook-collection-path",  str(COPY_DIR),
        "--output-path",               str(REKT_DIR),
    ]


def run_extract(prog: str, dry_run: bool) -> bool:
    cmd = [sys.executable, str(EXTRACT), prog]
    if dry_run:
        print(INFO(f"  [DRY] {' '.join(cmd)}"))
        return True
    result = subprocess.run(cmd, cwd=ROOT)
    return result.returncode == 0


# ---------------------------------------------------------------------------
# Per-program runner
# ---------------------------------------------------------------------------

def run_program(jar: Path, src: Path, *, force: bool, dry_run: bool, timeout: int) -> str:
    """
    Returns one of: 'skipped' | 'ok' | 'failed' | 'timeout' | 'dry'
    """
    prog  = prog_name(src)
    rdir  = report_dir(prog)
    cfjson = cfg_json(prog)

    if not force and rdir.exists() and cfjson.exists():
        print(SKIP(f"[SKIP] {prog}: report dir + cfg.json already exist"))
        return "skipped"

    cmd = build_rekt_cmd(jar, src, prog)
    size_kb = src.stat().st_size // 1024

    if dry_run:
        print(INFO(f"[DRY]  {prog}  ({size_kb} KB)"))
        print(INFO(f"       {' '.join(cmd)}"))
        run_extract(prog, dry_run=True)
        return "dry"

    print(INFO(f"[REKT] {prog}  ({size_kb} KB) ..."))

    try:
        result = subprocess.run(
            cmd,
            cwd=ROOT,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(FAIL(f"[TIMEOUT] {prog}: exceeded {timeout}s — increase with --timeout N"))
        return "timeout"
    except FileNotFoundError:
        print(FAIL("[ERROR] 'java' not found — is a JDK on PATH?"))
        return "failed"

    if result.returncode != 0:
        print(FAIL(f"[FAIL] {prog}: smojol-cli exited {result.returncode}"))
        return "failed"

    # Verify REKT actually wrote the expected CFG JSON
    expected_cfg = rdir / "cfg" / f"cfg-{prog}.cbl.json"
    if not expected_cfg.exists():
        print(FAIL(f"[FAIL] {prog}: REKT returned 0 but {expected_cfg.name} not found"))
        print(FAIL(f"       Expected: {expected_cfg}"))
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

def parse_args() -> dict:
    args = sys.argv[1:]
    opts = {
        "force":   False,
        "dry_run": False,
        "jar":     None,
        "only":    [],
        "timeout": DEFAULT_TIMEOUT,
    }
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--force":
            opts["force"] = True
        elif a in ("--dry-run", "--dry"):
            opts["dry_run"] = True
        elif a == "--skip-existing":
            pass
        elif a == "--jar":
            i += 1; opts["jar"] = args[i]
        elif a == "--timeout":
            i += 1; opts["timeout"] = int(args[i])
        elif a == "--only":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                opts["only"].append(args[i].upper())
                i += 1
            continue
        elif a in ("--help", "-h"):
            print(textwrap.dedent(__doc__).strip())
            sys.exit(0)
        i += 1
    return opts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    opts = parse_args()

    if not opts["dry_run"]:
        jar = locate_jar(opts["jar"])
        if jar is None:
            print(FAIL("\n[ERROR] Cannot locate smojol-cli JAR."))
            print(FAIL(  "        Set SMOJOL_JAR or use --jar PATH."))
            print(FAIL(  "        Searched:"))
            for p in CANDIDATE_JARS:
                print(FAIL(f"          {p}"))
            print()
            print(      "  Tip: $env:SMOJOL_JAR = 'C:\\work\\cobol-rekt\\smojol-cli\\target\\smojol-cli.jar'")
            return 2
    else:
        jar = Path("smojol-cli.jar")

    sources = find_sources()
    if opts["only"]:
        sources = [s for s in sources if prog_name(s) in opts["only"]]
        if not sources:
            print(FAIL(f"[ERROR] --only matched no files: {opts['only']}"))
            return 1

    total = len(sources)
    print(INFO(f"[INFO] {total} source file(s) targeted"))
    if not opts["force"]:
        already = sum(1 for s in sources
                      if report_dir(prog_name(s)).exists()
                      and cfg_json(prog_name(s)).exists())
        print(INFO(f"[INFO] {already} already have report+cfg.json (will skip)"))
    print()

    results: dict = {}
    for src in sources:
        status = run_program(
            jar, src,
            force=opts["force"],
            dry_run=opts["dry_run"],
            timeout=opts["timeout"],
        )
        results[prog_name(src)] = status
        print()

    # ---- summary table --------------------------------------------------
    col_w = max(len(p) for p in results) + 2
    divider = "-" * 52
    print(divider)
    print(f"{'Program':<{col_w}}  Status")
    print(divider)
    counts: dict = {"ok": 0, "skipped": 0, "failed": 0, "timeout": 0, "dry": 0}
    for prog, status in sorted(results.items()):
        counts[status] = counts.get(status, 0) + 1
        label = {"ok": "PASS", "skipped": "SKIP", "failed": "FAIL",
                 "timeout": "TIMEOUT", "dry": "DRY"}.get(status, status)
        colour = {"ok": OK, "skipped": SKIP, "failed": FAIL,
                  "timeout": FAIL, "dry": INFO}.get(status, INFO)
        print(f"{prog:<{col_w}}  {colour(label)}")
    print(divider)
    print(f"  ok={counts['ok']}  skipped={counts['skipped']}  "
          f"failed={counts['failed']}  timeout={counts['timeout']}")
    print(divider)

    if counts["failed"] or counts["timeout"]:
        print(FAIL("\nSome programs failed. Re-run only failures:"))
        failures = [p for p, s in results.items() if s in ("failed", "timeout")]
        print(FAIL(f"  py -3 validation/run_rekt_all.py --only {' '.join(failures)}"))
        return 1

    if opts["dry_run"]:
        print(INFO("\nDry run complete -- no files written."))

    return 0


if __name__ == "__main__":
    sys.exit(main())
