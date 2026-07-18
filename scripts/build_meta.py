#!/usr/bin/env python3
"""Helper for refreshing the meta snapshot.

Pulls the live MasterDuelMeta top-deck list (best effort) and prints it so
you can update `data/meta/tier_list.json`. The **threat tags** are curated,
not in the API, so this assists a manual edit rather than replacing it.

Usage:  python scripts/build_meta.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ygo_advisor import meta  # noqa: E402


def main() -> int:
    records = meta.refresh_from_web()
    if not records:
        print("Could not fetch live tier list (API shape may have changed).")
        print("Edit data/meta/tier_list.json by hand; keep the 'threats' tags.")
        return 1
    print(f"Fetched {len(records)} records. Sample keys:", list(records[0].keys())[:12])
    for r in records[:15]:
        name = r.get("name") or r.get("deckType") or r.get("title") or "?"
        print(" -", name)
    print("\nMerge names/shares into data/meta/tier_list.json and set threat tags.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
