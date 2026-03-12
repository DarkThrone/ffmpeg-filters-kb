#!/usr/bin/env python3
"""
index_algolia.py — Read Zola content Markdown files and push to Algolia.

Reads: content/filters/**/*.md
Pushes: one record per filter to the configured Algolia index

Environment variables required:
    ALGOLIA_APP_ID       — Algolia application ID
    ALGOLIA_ADMIN_KEY    — Admin API key (write access)
    ALGOLIA_INDEX        — Index name (default: ffmpeg_filters)

Usage:
    ALGOLIA_APP_ID=xxx ALGOLIA_ADMIN_KEY=yyy python scripts/index_algolia.py
"""
import os
import sys
import json
import tomllib
import frontmatter
from pathlib import Path
from algoliasearch.search_client import SearchClient

CONTENT_DIR = Path("content/filters")
INDEX_NAME  = os.environ.get("ALGOLIA_INDEX", "ffmpeg_filters")

def get_base_path() -> str:
    """Extract the URL path prefix from config.toml (e.g. '/ffmpeg-filters-kb')."""
    try:
        with open("config.toml", "rb") as f:
            config = tomllib.load(f)
        base_url = config.get("base_url", "").rstrip("/")
        # Extract just the path component (everything after the host)
        from urllib.parse import urlparse
        path = urlparse(base_url).path.rstrip("/")
        return path  # e.g. "/ffmpeg-filters-kb" or ""
    except Exception:
        return ""

def load_records() -> list[dict]:
    base_path = get_base_path()
    records = []
    for md_file in sorted(CONTENT_DIR.glob("**/*.md")):
        if md_file.name.startswith("_"):
            continue
        post = frontmatter.load(md_file)
        meta = post.metadata
        name = meta.get("title", md_file.stem)
        category_list = meta.get("taxonomies", {}).get("category", [])
        category = category_list[0] if category_list else "video"
        tags = meta.get("taxonomies", {}).get("tags", [])
        params = meta.get("extra", {}).get("parameters", [])
        description = meta.get("description", "")
        # Build URL from path: content/filters/video/scale.md -> /ffmpeg-filters-kb/filters/video/scale/
        rel = md_file.relative_to(Path("content"))
        url = base_path + "/" + str(rel.with_suffix("")).replace("\\", "/") + "/"

        records.append({
            "objectID": f"{category}-{name}",
            "name": name,
            "category": category,
            "description": description,
            "parameters": params,
            "tags": tags,
            "cohort": meta.get("extra", {}).get("cohort", 99),
            "url": url,
        })
    return records

def main():
    app_id  = os.environ.get("ALGOLIA_APP_ID")
    api_key = os.environ.get("ALGOLIA_ADMIN_KEY")

    if not app_id or not api_key:
        print("ERROR: ALGOLIA_APP_ID and ALGOLIA_ADMIN_KEY must be set", file=sys.stderr)
        sys.exit(1)

    records = load_records()
    print(f"Loaded {len(records)} filter records")

    client = SearchClient.create(app_id, api_key)
    index  = client.init_index(INDEX_NAME)

    # Atomic replace: saves, then moves
    index.replace_all_objects(records)
    print(f"Pushed {len(records)} records to Algolia index '{INDEX_NAME}'")

    # Configure index settings
    index.set_settings({
        "searchableAttributes": [
            "unordered(name)",
            "unordered(description)",
            "unordered(parameters)",
            "tags",
        ],
        "attributesForFaceting": ["category", "cohort"],
        "ranking": ["typo", "geo", "words", "filters", "proximity", "attribute", "exact", "custom"],
        "customRanking": ["asc(cohort)"],
    })
    print("Index settings configured")

if __name__ == "__main__":
    main()
