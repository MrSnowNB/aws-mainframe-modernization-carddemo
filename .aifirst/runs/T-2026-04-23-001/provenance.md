---
schema_version: "aifirst/1.0"
task_id: "T-2026-04-23-001"
artifact: provenance-manifest
created: "2026-04-27T12:31:00-04:00"
author: "Mark Snow"
purpose: "Cryptographic chain: source COBOL → CFG JSON → Markdown narration → validation report"
sha_algorithm: "git-blob-sha1"
---

# Provenance Manifest — Pilot Batch T-2026-04-23-001

> Each row links one COBOL program through its full evidence chain.
> SHAs are git blob SHA-1 (output of `git hash-object`), reproducible from the working tree.
> Any change to any artifact invalidates the row and requires re-validation.

## Manifest

| program  | source_cobol_sha | cfg_json_sha | markdown_sha | validation_report_sha |
|----------|------------------|--------------|--------------|-----------------------|
| COBSWAIT | 7957347717cf04be2dc4f5be24aa94668cf780ab | 43655d729b50af9baf37f2c094adb2045cff2122 | 21e6845d3cfc70c1eca805f26f8f906faa42aea2 | cb93a7d6e6d142fbc0ffbc6a593d60dbb9d69f3d |
| COMEN01C | 222db83b1ae9c01ef521342199d0234a4abd152d | c83ffa146cec8db57d02b79e0e6c3cdd35f10a1b | 05273fcdbcd703f74635bc803818f19206157bb5 | 6ca7ace2930c88a8d8c5a3911d009712eb739a19 |
| CBCUS01C | ad4c512be0d7bd72a933966d299ea21fb31b6b5b | 74dd7e08b7d9fbc220f7490c0cb3cffe4768f140 | 0e2cbb702b607ea2159b6ed54b94c9361b2dd4fd | 541a17cd53daf163a869d47a2fd968e62a09723e |
| COSGN00C | 28e2061e3f0ec1fbde590b0cf2236e2919567aee | 7dd7e876c0b376bc730c9c4eec9dd4fab05c6a0c | b6a817685fafd67deb3e3306dbf1f85d4a082a77 | 979c9eb6c7648997909f6e0e33847b70583da9ad |
| CBTRN01C | 450bd63983e78e1cca8719e72cbdf7cfccfb9630 | 99adfa8d8339e7306ae1f9bab4dfb277a17d08ca | b9c318f223326ccddcab6d3f889fdb00253ead9e | 742e3d9eee54c652f0c22dfe7f88a0e50c36a7b9 |
| CBACT01C | e680f8e4239a85eb9f95f129f282aa28e165496a | a4e4de3a0d22d429e4cb98e5e173b4e3bc9c40f2 | 426f2c99bdd7fa325c62a2ff566aa68f2a6c5bf6 | ef76697a92cbb2aff93a976a9143e569678dfa9d |

## Source Path Map

| program  | source_cobol_path | cfg_json_path | markdown_path | validation_report_path |
|----------|-------------------|---------------|---------------|------------------------|
| COBSWAIT | app/cbl/COBSWAIT.cbl | validation/structure/COBSWAIT_cfg.json | translations/baseline/COBSWAIT.md | validation/reports/COBSWAIT_T02.json |
| COMEN01C | app/cbl/COMEN01C.cbl | validation/structure/COMEN01C_cfg.json | translations/baseline/COMEN01C.md | validation/reports/COMEN01C_T02.json |
| CBCUS01C | app/cbl/CBCUS01C.cbl | validation/structure/CBCUS01C_cfg.json | translations/baseline/CBCUS01C.md | validation/reports/CBCUS01C_T02.json |
| COSGN00C | app/cbl/COSGN00C.cbl | validation/structure/COSGN00C_cfg.json | translations/baseline/COSGN00C.md | validation/reports/COSGN00C_T02.json |
| CBTRN01C | app/cbl/CBTRN01C.cbl | validation/structure/CBTRN01C_cfg.json | translations/baseline/CBTRN01C.md | validation/reports/CBTRN01C_T02.json |
| CBACT01C | app/cbl/CBACT01C.cbl | validation/structure/CBACT01C_cfg.json | translations/baseline/CBACT01C.md | validation/reports/CBACT01C_T02.json |

## Verification

To verify any row, run:

```
git hash-object <path>
```

Output must match the corresponding column for that row.