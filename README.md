# mmCIF dictionary explorer

A small, client-side tool for browsing [PDBx/mmCIF](https://mmcif.wwpdb.org/) dictionary content by default, while also accommodating other mmCIF dictionaries and dictionary extensions. Categories appear as an interactive graph (linked by `_pdbx_item_linked_group_list`); selecting a category or item shows definitions, types, enumerations, examples, and cross-links.

No build step for the UI: it is plain HTML, CSS, and JavaScript, with data loaded from a pre-built JSON file for the selected dictionary (switchable in the UI).

## Features

- **Graph** — Categories as nodes; size reflects how many dictionary link rows touch a category; colour reflects PDBx category group (see the in-app legend).
- **Details** — Per-category and per-item views with descriptions, keys, groups, incoming/outgoing links, and optional examples.
- **Filter** — Text filter narrows which nodes and edges are shown without changing the full category list.
- **Accessibility** — Keyboard-friendly category picker, skip link, and live region announcements for selections.

## Use it

<a href="https://deborahharrus.github.io/mmcif-dictionary-explorer/app/" style="display:inline-block;padding:12px 18px;background:#c9a227;color:#12151a;border-radius:10px;font-weight:700;text-decoration:none;letter-spacing:0.01em;font-size:1.05rem;">
  Launch the mmCIF dictionary explorer
</a>

Tip: after launching, use the dictionary drop-down in the header to switch between the built-in JSON dictionaries.

### Dictionary JSON sources

The JSON files under `app/data/` are derived from the upstream `.dic` dictionaries they were downloaded from or built from:

- **`app/data/mmcif_pdbx_v50.json`** — from wwPDB/PDBx `mmcif_pdbx_v50.dic` (`Index`): https://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v50.dic/Index/ (current `dictionary_version` in repo: `5.411`)
- **`app/data/mmcif_ihm_ext.json`** — from the IHMCIF `mmcif_ihm_ext.dic`: https://github.com/ihmwg/IHMCIF/blob/master/dist/mmcif_ihm_ext.dic (current `dictionary_version` in repo: `1.28`)
- **`app/data/mmcif_investigation.json`** — from the InvestigationCIF `mmcif_investigation.dic`: https://github.com/PDBeurope/InvestigationCIF/blob/main/dist/mmcif_investigation.dic (current `dictionary_version` in repo: `1.0.6.1`)

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

## Run locally

The app uses `fetch`, so it must be served over HTTP (not `file://`).

```bash
cd app
python -m http.server 8765
```

Then visit `http://127.0.0.1:8765/` in your browser.

Dictionary data comes from the pre-built JSON files in `app/data/` (switch dictionaries using the drop-down in the header). To regenerate them from upstream mmCIF dictionaries (`.dic`) with Python and [gemmi](https://github.com/project-gemmi/gemmi), see **[DEVELOPMENT.md](DEVELOPMENT.md)**.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project’s source code is released under the [MIT License](LICENSE).

This repository **does not** include the upstream dictionary source **`.dic`** files. Only the derived **`app/data/*.json`** dictionary artifacts are distributed here. Follow the upstream licensing and citation requirements when sharing or reusing that dictionary content.

## Author

Deborah Harrus, Protein Data Bank in Europe (PDBe), EMBL-EBI
