# mmCIF dictionary explorer — development

A small static web app for exploring the PDBx/mmCIF dictionary. It shows **categories** as an interactive graph linked by `_pdbx_item_linked_group_list` relationships, and shows **items** (data names) with types, descriptions, enumerations, and examples.

The published site loads **`app/data/dictionary.json`**. You can commit a pre-built file (typical for GitHub Pages) or regenerate it locally with the script below.

## Prerequisites

- **Python 3** (3.10 or newer is fine).
- **gemmi** (only needed to rebuild the JSON from the `.dic` file):

  ```bash
  pip install -r requirements.txt
  ```

## Build `dictionary.json`

Regenerate whenever you change the dictionary file or want to point at another `.dic`:

```bash
python scripts/build_dictionary_json.py
```

Defaults:

- Input: `dictionaries/mmcif_pdbx_v50[5.411].dic`
- Output: `app/data/dictionary.json`

Custom paths:

```bash
python scripts/build_dictionary_json.py --dic path/to/your.dic --out app/data/dictionary.json
```

## Run locally

The page loads JSON with `fetch()`, so it must be served over **HTTP** (opening `index.html` as `file://` will not work).

From the repository root:

```bash
cd app
python -m http.server 8765
```

Then open **http://127.0.0.1:8765/** in your browser (any free port is fine).

## How to use the UI

### Graph

- Each **dot** is a dictionary **category**.
- **Size** reflects how many link rows in `_pdbx_item_linked_group_list` involve that category (see the legend for the exact scaling note).
- **Colour** reflects the category’s primary PDBx **group** (first `_category_group` value that is not `inclusive_group`).
- **Click a node** to open that category in the details panel.

### Graph legend

The legend above the graph explains **size** and **colour**, lists each group with a **swatch** and **how many categories** belong to it, and states the **range of link counts** in the loaded dictionary. Use **Hide** / **Show** next to the title to collapse or expand the legend body and free vertical space for the graph.

### Filter the graph

Use **Filter the graph** in the header to hide nodes and edges that do not match your text. Matching uses the category id, its description, and all item names in that category. The filter does **not** change the category drop-down (that list always stays complete).

### Open category (menu)

**Open category** is a standard HTML **`select`** with every category. It is the most reliable path for **keyboard** and **screen reader** use. Choosing a category updates the details panel and focuses the graph on that node.

### Details panel

The right-hand panel can be **collapsed** or **expanded** with the arrow control on its inner edge (narrow strip when collapsed so you can open it again).

For a **category**, the panel shows, in order: description; the list of **items**; optional **category examples**; **category keys**; PDBx **category groups**; and incoming and outgoing category links (with item names).

For an **item**, it shows mandatory flag, **type** (`_item_type.code`), description, allowed values if enumerated, examples, and a link back to the parent category.

### Accessibility

- **Skip to details** appears when you tab from the top of the page.
- Choosing a category from the **Open category** menu moves focus into the **details** region when appropriate.
- Live announcements summarize the selected category or item.
- Item lists in the panel use **buttons** for each data name so they are easy to activate with keyboard assistive tech.

## Project layout

| Path | Purpose |
|------|--------|
| `dictionaries/*.dic` | Source mmCIF/PDBx dictionary (STAR/CIF). |
| `scripts/build_dictionary_json.py` | Parses the `.dic` with gemmi and writes JSON. |
| `app/index.html` | Single-page UI. |
| `app/data/dictionary.json` | Data consumed by the UI (commit a pre-built copy for hosting). |

## Licence

The explorer code is yours to use under your own terms. The mmCIF dictionary file is distributed by the wwPDB/PDBx project; respect their licensing and citation requirements when redistributing dictionary files.
