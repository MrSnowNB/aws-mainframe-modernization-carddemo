#!/usr/bin/env python3
import json
import yaml
from pathlib import Path

def main():
    prog = "CBACT02C"
    cfg_path = Path(f"validation/structure/{prog}_cfg.json")
    props_path = Path(f"validation/pass2/{prog}_propositions.json")
    out_path = Path(f"translations/gold-candidate/{prog}.md")

    cfg = json.loads(cfg_path.read_text())
    props = json.loads(props_path.read_text())

    # Build frontmatter
    fm = {
        "schema_version": "cobol-md/1.0",
        "program_id": prog,
        "source_file": cfg["source_file"],
        "source_sha": cfg["source_sha"],
        "translation_date": "2026-04-30",
        "translating_agent": "gemini-cli-agent",
        "aifirst_task_id": "T-CBACT02C-TRANSLATION",
        "cfg_source": str(cfg_path).replace("\\", "/"),
        "business_domain": "Account Management",
        "subtype": "Batch",
        "data_items": [
            {
                "name": d["name"],
                "level": d["level"],
                "redefines": d["redefines"],
                "reachable": d["reachable"]
            }
            for d in cfg["data_items"]
        ],
        "procedure_paragraphs": [
            {
                "name": p["name"],
                "reachable": p["reachable"],
                "synthetic": False
            }
            for p in cfg["paragraphs"]
        ],
        "calls_to": [
            {"program": c, "condition": "unconditional", "call_type": "STATIC"}
            for c in cfg["calls_to"]
        ],
        "copybooks_used": [
            {"name": c, "path": f"app/cpy/{c}.cpy"}
            for c in cfg["copybooks_used"]
        ],
        "cics_commands": cfg["cics_commands"]
    }

    content = "---\n" + yaml.dump(fm, sort_keys=False) + "---\n\n# File Summary\n\nAutomated translation for " + prog + "\n\n"
    
    # Add paragraphs from propositions
    paras = {}
    for p in props:
        paras.setdefault(p["paragraph"], []).append(p)
        
    for name, p_list in paras.items():
        content += f"## {name}\n\n"
        for p in p_list:
            content += f"- {p['proposition']}\n"
        content += "\n"

    out_path.write_text(content)
    print(f"[ok] Synthesized {out_path}")

if __name__ == "__main__":
    main()
