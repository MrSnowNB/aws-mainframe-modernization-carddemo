---
schema_version: "archive-provenance/1.0"
source_trees:
  - "translations/baseline-v1.2/"
  - "translations/gold/"
target_tree: "none — delete-only per Path 3"
migration_date: "2026-05-05"
migration_method: "Contents API DELETE only; content preserved in git object store"
source_head_before_migration: "524eabdd3288274e5a9d623ea129e1945c73bd26"
blob_sha_preserved: "N/A — Path 3 delete-only, blobs remain in git object store"
total_files: 8
total_bytes: 437581
---

# Translations Archive Provenance

This document records the original path, size, and blob SHA for every
file deleted from `translations/baseline-v1.2/` (OP-2-08) and
`translations/gold/` (OP-2-09) as part of Operation Tidy Step 2 Commit C.

**Path 3 — delete-only.** No content was copied to `archive/`.
All deleted blobs remain permanently in the git object store.
This document is the authoritative recovery bridge.

## OP-2-08 Inventory — translations/baseline-v1.2/

| old_path | size_bytes | blob_sha |
|---|---|---|
| `translations/baseline-v1.2/.gitkeep` | 0 | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `translations/baseline-v1.2/CBACT01C.md` | 83593 | `bb4594377248892c374cff4f0ee5cafe6c56993f` |
| `translations/baseline-v1.2/CBCUS01C.md` | 35932 | `45d1807cf9465f61f6a090d9fc92ceea7f561bda` |
| `translations/baseline-v1.2/CBTRN01C.md` | 80298 | `a864a80420064ee5f31c3f84bb4aad35929116d4` |
| `translations/baseline-v1.2/COBSWAIT.md` | 5776 | `cf9b2f4d8c9da6b338d4e5a467c7c684cb1563b1` |
| `translations/baseline-v1.2/COMEN01C.md` | 135924 | `25a6ab300da71e90fafd0906dc9bb30e5c584b11` |
| `translations/baseline-v1.2/COSGN00C.md` | 91429 | `e049b845ffb08fbaecdebd48dad58d440b8b5317` |

**Subtotal OP-2-08:** 7 files, 432,952 bytes

## OP-2-09 Supplementary Deletion — translations/gold/

The `translations/gold/` tier contained a single file, representing an
abandoned or incomplete promotion from `gold-candidate/`. Per M2 in the
tidy plan, this stub tier is archived rather than preserved in-tree.

| old_path | size_bytes | blob_sha |
|---|---|---|
| `translations/gold/COBSWAIT.md` | 4629 | `21e6845d3cfc70c1eca805f26f8f906faa42aea2` |

**Subtotal OP-2-09:** 1 file, 4,629 bytes

**Grand total:** 8 files, 437,581 bytes

## Content Recovery

All deleted blobs remain in the git object store. Recover any file via:

```
git show <blob_sha>
```

Examples:
- `.gitkeep` (empty): `git show e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`
- `CBACT01C.md` (first content file): `git show bb4594377248892c374cff4f0ee5cafe6c56993f`
- `COMEN01C.md` (largest, 135 KB): `git show 25a6ab300da71e90fafd0906dc9bb30e5c584b11`
- `translations/gold/COBSWAIT.md` (OP-2-09): `git show 21e6845d3cfc70c1eca805f26f8f906faa42aea2`

## Verification

- Source HEAD before deletions: `524eabdd3288274e5a9d623ea129e1945c73bd26`
- Active task `.clinerules/runs/T-2026-05-04-001/` tree SHA at migration start: `3ae40665f3da6d6dd03c5b32479fff5c7de5ca46`
- Total bytes deleted: 437,581 (matches inventory)
- No files excluded from deletion

## Rollback

If Commit C must be rolled back entirely:

```
git reset --hard <C-0 SHA>
git push --force-with-lease origin main
```

C-0 SHA: *(filled in by amendment after this commit is confirmed)*

This restores `translations/baseline-v1.2/` and `translations/gold/` to
their pre-delete state while preserving this provenance document.
