"""Public discovery metadata; never used as synthetic evaluation fixtures."""

import json
from pathlib import Path
from urllib.parse import urlparse

CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "discovery_catalog.json"


def load_discovery():
    items = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    ids = set()
    for item in items:
        if item["id"] in ids or not item["description_zh"] or not item["description_en"]:
            raise ValueError("Invalid discovery catalog identity or bilingual description")
        if urlparse(item["source"]).scheme != "https" or not urlparse(item["source"]).netloc:
            raise ValueError("Catalog sources must be official HTTPS links")
        ids.add(item["id"])
    return items


def filter_datasets(items, *, query="", task="all", data_type="all", access="all"):
    query = query.strip().casefold()
    return [
        item
        for item in items
        if (
            not query
            or query
            in " ".join(
                str(item[k]) for k in ("name", "name_zh", "description_zh", "description_en", "id")
            ).casefold()
        )
        and (task == "all" or item["task"] == task)
        and (data_type == "all" or item["type"] == data_type)
        and (access == "all" or item["access"] == access)
    ]
