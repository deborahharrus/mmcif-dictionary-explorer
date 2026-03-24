# mmCIF dictionary explorer

A small, client-side tool for browsing [PDBx/mmCIF](https://mmcif.wwpdb.org/) dictionary content. Categories appear as an interactive graph (linked by `_pdbx_item_linked_group_list`); selecting a category or item shows definitions, types, enumerations, examples, and cross-links.

No build step for the UI: it is plain HTML, CSS, and JavaScript, with data loaded from a single JSON file.

## Features

- **Graph** — Categories as nodes; size reflects how many dictionary link rows touch a category; colour reflects PDBx category group (see the in-app legend).
- **Details** — Per-category and per-item views with descriptions, keys, groups, incoming/outgoing links, and optional examples.
- **Filter** — Text filter narrows which nodes and edges are shown without changing the full category list.
- **Accessibility** — Keyboard-friendly category picker, skip link, and live region announcements for selections.

## Try it

**[Live demo (GitHub Pages)](https://deborahharrus.github.io/mmcif-dictionary-explorer/app/)**

## Run locally

The app must be served over HTTP (`fetch` will not work from `file://`).

```bash
cd app
python -m http.server 8765
```

Then visit `http://127.0.0.1:8765/` in your browser.

Runtime data lives in **`app/data/dictionary.json`**. To regenerate it from an mmCIF dictionary (`.dic`) with Python and [gemmi](https://github.com/project-gemmi/gemmi), see **[DEVELOPMENT.md](DEVELOPMENT.md)**.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project’s source code is released under the [MIT License](LICENSE).

This repository **does not** include the PDBx/mmCIF source **`.dic`** file; only the derived **`app/data/dictionary.json`** is distributed here. That JSON still reflects [wwPDB/PDBx](https://mmcif.wwpdb.org/) dictionary content—follow their licensing and citation requirements when sharing or reusing that data.

## Author

Deborah Harrus, Protein Data Bank in Europe (PDBe), EMBL-EBI
