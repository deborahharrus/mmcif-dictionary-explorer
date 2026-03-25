"""
Parse mmcif_pdbx dictionary .dic (STAR/CIF with save frames) and emit JSON for the explorer UI.
Requires: gemmi
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import gemmi


def clean_value(raw: str | None) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if s in (".", "?", ""):
        return None
    if s.startswith(";"):
        s = s[1:]
    if s.endswith(";"):
        s = s[:-1]
    s = s.strip().replace("\r\n", "\n").replace("\r", "\n")
    return s or None


def quoted_token(s: str) -> str:
    """Normalize a data name like '\"_foo.bar\"' -> _foo.bar"""
    s = s.strip()
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        s = s[1:-1]
    return s.strip()


def load_category_groups(block: gemmi.cif.Block) -> list[dict[str, str | None]]:
    tab = block.find_mmcif_category("_category_group_list")
    if tab is None or len(tab) == 0:
        return []
    out = []
    for r in range(len(tab)):
        row = tab[r]
        out.append(
            {
                "id": str(row[0]).strip(),
                "parent_id": None if str(row[1]).strip() in (".", "?", "") else str(row[1]).strip(),
                "description": clean_value(str(row[2])) if tab.width() > 2 else None,
            }
        )
    return out


def load_item_links(block: gemmi.cif.Block) -> list[dict[str, str]]:
    tab = block.find_mmcif_category("_pdbx_item_linked_group_list")
    if tab is None:
        return []
    links = []
    for r in range(len(tab)):
        row = tab[r]
        links.append(
            {
                "child_category_id": str(row[0]).strip(),
                "link_group_id": str(row[1]).strip(),
                "child_name": quoted_token(str(row[2])),
                "parent_name": quoted_token(str(row[3])),
                "parent_category_id": str(row[4]).strip(),
            }
        )
    return links


def build_json(dic_path: Path) -> dict:
    doc = gemmi.cif.read(str(dic_path))
    block = doc.sole_block()
    version = clean_value(block.find_value("_dictionary.version")) or ""

    category_groups = load_category_groups(block)
    raw_links = load_item_links(block)

    categories: dict[str, dict] = {}
    items: dict[str, dict] = {}

    for it in block:
        fr = it.frame
        if not fr:
            continue
        name = fr.name
        if name.startswith("_"):
            iname_raw = fr.find_value("_item.name")
            if not iname_raw:
                continue
            item_name = quoted_token(str(iname_raw))
            cat_id = fr.find_value("_item.category_id")
            if cat_id:
                cat_id = str(cat_id).strip()
            row: dict = {
                "name": item_name,
                "category_id": cat_id,
                "mandatory_code": clean_value(fr.find_value("_item.mandatory_code")),
                "type_code": clean_value(fr.find_value("_item_type.code")),
                "description": clean_value(fr.find_value("_item_description.description")),
            }
            ex_tab = fr.find_mmcif_category("_item_examples")
            if ex_tab and len(ex_tab):
                cases = []
                for r in range(len(ex_tab)):
                    cases.append(clean_value(str(ex_tab[r][0])) or "")
                row["examples"] = [c for c in cases if c]
            en_tab = fr.find_mmcif_category("_item_enumeration")
            if en_tab and len(en_tab):
                row["enumeration"] = []
                for r in range(len(en_tab)):
                    row["enumeration"].append(
                        {
                            "value": clean_value(str(en_tab[r][0])) or str(en_tab[r][0]),
                            "detail": clean_value(str(en_tab[r][1])) if en_tab.width() > 1 else None,
                        }
                    )
            items[item_name] = row
            if cat_id:
                categories.setdefault(cat_id, {"id": cat_id, "item_names": []})
                categories[cat_id]["item_names"].append(item_name)
        else:
            cid = fr.find_value("_category.id")
            if not cid:
                continue
            cid = str(cid).strip()
            cat: dict = {
                "id": cid,
                "description": clean_value(fr.find_value("_category.description")),
                "mandatory_code": clean_value(fr.find_value("_category.mandatory_code")),
            }
            ck = fr.find_mmcif_category("_category_key")
            if ck and len(ck):
                keys = []
                for r in range(len(ck)):
                    cell = str(ck[r][0])
                    keys.append(quoted_token(cell))
                cat["category_keys"] = keys
            cg = fr.find_mmcif_category("_category_group")
            if cg and len(cg):
                gids = []
                for r in range(len(cg)):
                    for c in range(cg.width()):
                        v = str(cg[r][c]).strip()
                        if v and v not in (".", "?"):
                            gids.append(v)
                cat["category_groups"] = gids
            ex = fr.find_mmcif_category("_category_examples")
            examples = []
            if ex and len(ex):
                for r in range(len(ex)):
                    detail = ex.width() > 0 and clean_value(str(ex[r][0]))
                    case = ex.width() > 1 and clean_value(str(ex[r][1]))
                    if detail or case:
                        examples.append({"detail": detail, "case": case})
            if examples:
                cat["examples"] = examples

            existing = categories.get(cid, {})
            merged = {**existing, **cat}
            if "item_names" not in merged:
                merged["item_names"] = existing.get("item_names", [])
            categories[cid] = merged

    for cid, c in categories.items():
        c["item_names"] = sorted(set(c.get("item_names") or []))

    edge_set: set[tuple[str, str, str]] = set()
    summarized_edges: list[dict] = []
    for L in raw_links:
        pc, cc = L["parent_category_id"], L["child_category_id"]
        key = (pc, cc, L["link_group_id"])
        if key in edge_set:
            continue
        edge_set.add(key)
        summarized_edges.append(
            {
                "parent": pc,
                "child": cc,
                "link_group_id": L["link_group_id"],
                "parent_item": L["parent_name"],
                "child_item": L["child_name"],
            }
        )

    by_parent: dict[str, list[dict]] = defaultdict(list)
    for e in summarized_edges:
        by_parent[e["parent"]].append(e)

    return {
        "dictionary_version": version,
        "dictionary_file": dic_path.name,
        "category_group_list": category_groups,
        "categories": categories,
        "items": items,
        "category_links": summarized_edges,
        "links_by_parent": {k: v for k, v in by_parent.items()},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Build dictionary JSON for mmCIF explorer")
    ap.add_argument(
        "--dic",
        type=Path,
        # Default to the local dictionary filename; the embedded `dictionary_version`
        # is read from the dictionary content itself.
        default=Path(__file__).resolve().parent.parent / "dictionaries" / "mmcif_pdbx_v50.dic",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "app" / "data" / "mmcif_pdbx_v50.json",
    )
    args = ap.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    data = build_json(args.dic)
    args.out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {args.out} ({args.out.stat().st_size // 1024} KiB)")
    print(
        f"Categories: {len(data['categories'])}, items: {len(data['items'])}, link rows: {len(data['category_links'])}"
    )


if __name__ == "__main__":
    main()
