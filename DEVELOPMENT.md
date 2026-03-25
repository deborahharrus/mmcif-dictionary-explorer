# mmCIF dictionary explorer — development

A small static web app for exploring the PDBx/mmCIF dictionary or any other mmCIF dictionary or dictionary extension. It shows **categories** as an interactive graph linked by `_pdbx_item_linked_group_list` when available, otherwise by `_item_linked`, and shows **items** (data names) with types, descriptions, enumerations, and examples.

The published site loads **`app/data/mmcif_pdbx_v50.json`** by default; other built-in dictionaries are selectable in the app’s dictionary drop-down. See **[README.md](README.md)** for sources and `dictionary_version` values. Below are instructions on how to regenerate the JSON using `scripts/build_dictionary_json.py`.

## Prerequisites

- **Python 3** (3.10 or newer is fine).
- **gemmi** (needed to rebuild the JSON from the `.dic` file):

  ```bash
  pip install -r requirements.txt
  ```

Note: the upstream `.dic` files are not included in this published repo. Download them from [wwPDB mmCIF dictionary downloads](https://mmcif.wwpdb.org/dictionaries/downloads.html) and copy the needed `.dic` files into `dictionaries/` locally before running `scripts/build_dictionary_json.py` (e.g. `mmcif_pdbx_v50.dic`, `mmcif_pdbx_v5_next.dic`, `mmcif_investigation_ligscreen.dic`, `mmcif_ihm_ext.dic`).

## Build `*.json`

Regenerate whenever a dictionary file is updated, or to add another `.dic`:

```bash
python scripts/build_dictionary_json.py
```

Defaults:

- Input: `dictionaries/mmcif_pdbx_v50.dic`
- Output: `app/data/mmcif_pdbx_v50.json`

The script uses `_pdbx_item_linked_group_list` when present; if it is empty or missing (e.g. `mmcif_ihm_ext.dic`), it derives graph edges from `_item_linked`.

Custom paths:

```bash
python scripts/build_dictionary_json.py --dic path/to/your.dic --out app/data/your.json
```

Rebuild all shipped dictionaries (from `dictionaries/`):

```bash
python scripts/build_dictionary_json.py --dic dictionaries/mmcif_pdbx_v50.dic --out app/data/mmcif_pdbx_v50.json
python scripts/build_dictionary_json.py --dic dictionaries/mmcif_pdbx_v5_next.dic --out app/data/mmcif_pdbx_v5_next.json
python scripts/build_dictionary_json.py --dic dictionaries/mmcif_investigation_ligscreen.dic --out app/data/mmcif_investigation_ligscreen.json
python scripts/build_dictionary_json.py --dic dictionaries/mmcif_ihm_ext.dic --out app/data/mmcif_ihm_ext.json
```

### Compare PDBx link table vs `_item_linked`

For full PDBx dictionaries, the build uses `_pdbx_item_linked_group_list` when it exists; extensions may fall back to `_item_linked`. Those sources are **not identical**: the PDBx grouped list is richer (more category pairs and distinct `link_group_id` values), while the fallback collapses many item-level links into one synthetic group (`item_linked`) per `(parent_cat, child_cat)` key.

To see counts and pair-wise differences for any `.dic` you have locally:

```bash
python scripts/build_dictionary_json.py --compare-link-sources --dic dictionaries/mmcif_pdbx_v50.dic
```

## Run locally

The page loads JSON with `fetch()`, so it must be served over **HTTP** (opening `index.html` as `file://` will not work).

From the repository root:

```bash
cd app
python -m http.server 8765
```

Then open **http://127.0.0.1:8765/** in your browser (any free port is fine).

## Project layout

| Path | Purpose |
|------|--------|
| `dictionaries/*.dic` | Source of the dictionary files. |
| `scripts/build_dictionary_json.py` | Parses the `.dic` files with gemmi and writes JSON. |
| `app/index.html` | Single-page UI. |
| `app/data/*.json` | Data consumed by the UI. |

## License

This project’s source code is released under the [MIT License](LICENSE).

This repository **does not** include the upstream dictionary source **`.dic`** files. Only the derived **`app/data/*.json`** dictionary artifacts are distributed here. Follow the upstream licensing and citation requirements when sharing or reusing that dictionary content.

## Author

Deborah Harrus, Protein Data Bank in Europe (PDBe), EMBL-EBI

