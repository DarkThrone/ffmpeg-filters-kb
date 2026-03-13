+++
title = "blockdetect"
description = "Detect DCT-based blocking artifacts in compressed video frames and attach a blockiness score as frame metadata."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "quality", "compression"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["blurdetect", "deblock"]
parameters = ["period_min", "period_max", "planes"]
cohort = 3
source_file = "libavfilter/vf_blockdetect.c"
+++

The `blockdetect` filter measures the severity of DCT blocking artifacts in compressed video without modifying the stream. It is based on the Muijs–Kirenko no-reference blocking artifact measure: it looks for periodic pixel grid patterns at the block boundaries typical of heavy MPEG/H.264 quantization. The score is attached as `lavfi.block` frame metadata and can drive automated quality reports or `select` filter decisions.

## Quick Start

```sh
# Print per-frame blockiness scores
ffmpeg -i input.mp4 -vf blockdetect -f null - 2>&1 | grep block
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_min | int | `3` | Minimum pixel grid period to search for. |
| period_max | int | `24` | Maximum pixel grid period to search for. |
| planes | int | `1` | Bitmask of planes to analyze (default: first plane only). |

## Examples

### Default blockiness detection

```sh
ffmpeg -i compressed.mp4 -vf blockdetect -f null -
```

### Search for H.264 typical 8×8 and 16×16 block periods

```sh
ffmpeg -i input.mp4 -vf "blockdetect=period_min=8:period_max=16" -f null -
```

### Save per-frame scores to a file

```sh
ffmpeg -i input.mp4 \
  -vf "blockdetect,metadata=print:key=lavfi.block:file=block_scores.txt" \
  -f null -
```

### Combine with blurdetect for full quality report

```sh
ffmpeg -i input.mp4 -vf "blockdetect,blurdetect" -f null - 2>&1 | grep "lavfi\."
```

## Notes

- `lavfi.block` metadata value increases with artifact severity; perfectly clean frames score near 0.
- The default period range [3, 24] covers common block sizes (4×4 up to 24×24); adjust for the codec under test.
- Use after decoding compressed video; does not apply meaningfully to lossless or raw sources.
- Pair with `deblock` to both detect and reduce blocking in a single pipeline.
