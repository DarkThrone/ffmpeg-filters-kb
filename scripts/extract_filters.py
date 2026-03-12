#!/usr/bin/env python3
"""
extract_filters.py — Read FFmpeg source and extract structured filter metadata.

Outputs: filter_data/{filter_name}.json

Usage:
    python scripts/extract_filters.py --ffmpeg-src /Users/gero/work/ffmpeg \
                                       --filters scale crop volume
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

FFMPEG_SRC = Path("/Users/gero/work/ffmpeg")
LIBAVFILTER = FFMPEG_SRC / "libavfilter"
FILTERS_TEXI = FFMPEG_SRC / "doc" / "filters.texi"
OUTPUT_DIR = Path("filter_data")

# Cohort 1 filter list
COHORT_1_FILTERS = {
    # video
    "scale", "crop", "overlay", "fade", "drawtext", "hflip", "vflip",
    "rotate", "transpose", "trim", "fps", "format", "setpts", "thumbnail",
    "split", "concat", "pad", "drawbox", "zoompan", "hstack", "vstack",
    "xstack", "setsar", "null", "select", "colorbalance", "hue", "eq",
    "palettegen", "paletteuse",
    # audio
    "volume", "amix", "aecho", "acompressor", "equalizer", "highpass",
    "lowpass", "pan", "atrim", "anull", "amerge", "aformat", "adelay",
    "silencedetect", "dynaudnorm", "afade", "atempo", "aresample", "apad",
    "asplit",
}

def find_filter_source(filter_name: str) -> Path | None:
    """Find the source file for a given filter name."""
    for prefix in ("vf_", "af_", "f_", "sf_", "avf_", ""):
        candidate = LIBAVFILTER / f"{prefix}{filter_name}.c"
        if candidate.exists():
            return candidate
    # Try searching by filter name inside files (varying whitespace alignment)
    pattern = re.compile(rf'\.p\.name\s*=\s*"{re.escape(filter_name)}"')
    for c_file in LIBAVFILTER.glob("*.c"):
        content = c_file.read_text(errors="ignore")
        if pattern.search(content):
            return c_file
    return None

def extract_avoptions(source_text: str) -> list[dict]:
    """Parse AVOption array from C source."""
    options = []
    # Match: { "name", "desc", OFFSET(...), AV_OPT_TYPE_XXX, {.xxx = val}, min, max, FLAGS }
    pattern = re.compile(
        r'\{\s*"([^"]+)"\s*,\s*"([^"]*)"'   # name, description
        r'[^,]*,[^,]*,\s*AV_OPT_TYPE_(\w+)'  # type
        r'.*?\}',
        re.DOTALL
    )
    for m in pattern.finditer(source_text):
        name, desc, opt_type = m.group(1), m.group(2), m.group(3)
        if name.startswith("_") or not desc or opt_type == "CONST":
            continue
        options.append({"name": name, "description": desc, "type": opt_type})
    return options

def extract_filter_description(source_text: str) -> str:
    """Extract the .p.description string from the FFFilter struct."""
    m = re.search(r'\.p\.description\s*=\s*NULL_IF_CONFIG_SMALL\("([^"]+)"\)', source_text)
    if m:
        return m.group(1)
    m = re.search(r'\.p\.description\s*=\s*"([^"]+)"', source_text)
    if m:
        return m.group(1)
    return ""

def extract_texi_section(filter_name: str) -> str:
    """Extract the section for a filter from doc/filters.texi."""
    if not FILTERS_TEXI.exists():
        return ""
    content = FILTERS_TEXI.read_text(errors="ignore")
    # Look for @section or @subsection with the filter name
    patterns = [
        rf'@subsection {re.escape(filter_name)}\b(.*?)(?=\n@subsection|\n@section|\Z)',
        rf'@section {re.escape(filter_name)}\b(.*?)(?=\n@section|\Z)',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.DOTALL | re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            # Strip Texinfo markup
            raw = re.sub(r'@\w+\{([^}]*)\}', r'\1', raw)
            raw = re.sub(r'@\w+', '', raw)
            return raw[:3000]  # cap at 3000 chars
    return ""

def determine_type(source_path: Path) -> str:
    name = source_path.name
    if name.startswith("vf_"):
        return "video"
    if name.startswith("af_"):
        return "audio"
    return "video"

def extract_filter(filter_name: str) -> dict | None:
    src = find_filter_source(filter_name)
    if not src:
        print(f"  WARNING: source not found for '{filter_name}'", file=sys.stderr)
        return None

    text = src.read_text(errors="ignore")
    description = extract_filter_description(text)
    options = extract_avoptions(text)
    texi_section = extract_texi_section(filter_name)
    filter_type = determine_type(src)

    return {
        "name": filter_name,
        "type": filter_type,
        "source_file": str(src.relative_to(FFMPEG_SRC)),
        "description": description,
        "options": options,
        "texi_section": texi_section,
    }

def main():
    parser = argparse.ArgumentParser(description="Extract FFmpeg filter metadata")
    parser.add_argument("--filters", nargs="*", help="Filter names (default: cohort 1)")
    parser.add_argument("--all-cohort-1", action="store_true", help="Extract all cohort 1 filters")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    target_filters = args.filters or list(COHORT_1_FILTERS)

    for filter_name in sorted(target_filters):
        print(f"Extracting: {filter_name}")
        data = extract_filter(filter_name)
        if data:
            out_path = OUTPUT_DIR / f"{filter_name}.json"
            out_path.write_text(json.dumps(data, indent=2))
            print(f"  -> {out_path}")

if __name__ == "__main__":
    main()
