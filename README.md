# mmCIF dictionary explorer

A small, client-side tool for browsing [PDBx/mmCIF](https://mmcif.wwpdb.org/) dictionary content. Categories appear as an interactive graph (linked by `_pdbx_item_linked_group_list`); selecting a category or item shows definitions, types, enumerations, examples, and cross-links.

No build step for the UI: it is plain HTML, CSS, and JavaScript, with data loaded from a single JSON file.

## Features

- **Graph** — Categories as nodes; size reflects how many dictionary link rows touch a category; colour reflects PDBx category group (see the in-app legend).
- **Details** — Per-category and per-item views with descriptions, keys, groups, incoming/outgoing links, and optional examples.
- **Filter** — Text filter narrows which nodes and edges are shown without changing the full category list.
- **Accessibility** — Keyboard-friendly category picker, skip link, and live region announcements for selections.

## Try it

If a demo is deployed from this repository, open the **`app/`** path on the host (for example, GitHub Pages serves it as `/repository-name/app/` on a project site).

## Run locally

The app must be served over HTTP (`fetch` will not work from `file://`).

```bash
cd app
python -m http.server 8765
```

Then visit `http://127.0.0.1:8765/` in your browser.

Runtime data lives in **`app/data/dictionary.json`**. To regenerate it from an mmCIF dictionary (`.dic`) with Python and [gemmi](https://github.com/project-gemmi/gemmi), see **[DEVELOPMENT.md](DEVELOPMENT.md)**. That document also describes hosting on GitHub Pages, project layout, and licensing of dictionary files.

## Licence

Use this project’s code on your own terms. The mmCIF dictionary is provided by wwPDB/PDBx; follow their terms when redistributing `.dic` or derived data.
