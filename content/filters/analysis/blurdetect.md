+++
title = "blurdetect"
description = "Compute a no-reference blur metric for each video frame using Canny edge detection, attaching the result as frame metadata."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "blur", "quality"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["blockdetect", "blurdetect"]
parameters = ["low", "high", "radius", "block_pct", "block_width", "block_height", "planes"]
cohort = 3
source_file = "libavfilter/vf_blurdetect.c"
+++

The `blurdetect` filter computes a perceptual blur score for each frame without modifying the video. It is based on the Marziliano no-reference blur metric: it detects edges using Canny thresholding, then measures the spread of local maxima around each edge — wider spread indicates more blur. The score is attached as `lavfi.blur` frame metadata and can be used for automated quality control.

## Quick Start

```sh
# Print blur scores to stderr
ffmpeg -i input.mp4 -vf "blurdetect" -f null - 2>&1 | grep blur
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| low | float | `20/255 ≈ 0.078` | Low threshold for Canny edge detection (0–1). |
| high | float | `50/255 ≈ 0.196` | High threshold for Canny edge detection (0–1). `high` ≥ `low`. |
| radius | int | `50` | Search radius (pixels) around edge pixel for local maxima. |
| block_pct | int | `80` | Percentage of most significant blocks to include in blur score. |
| block_width | int | `-1` | Block width for block-based analysis; ≤0 disables block mode. |
| block_height | int | `-1` | Block height for block-based analysis; ≤0 disables block mode. |
| planes | int | `1` | Bitmask of planes to analyze (default: first plane only). |

## Examples

### Basic blur detection

```sh
ffmpeg -i input.mp4 -vf blurdetect -f null -
```

### Block-based analysis (32×32 blocks, top 80%)

```sh
ffmpeg -i input.mp4 -vf "blurdetect=block_width=32:block_height=32:block_pct=80" -f null -
```

### Inject metadata for select filter

```sh
ffmpeg -i input.mp4 \
  -vf "blurdetect,metadata=print:key=lavfi.blur:file=blur_scores.txt" \
  -f null -
```

### Adjust Canny thresholds for higher sensitivity

```sh
ffmpeg -i input.mp4 -vf "blurdetect=low=0.05:high=0.15" -f null -
```

## Notes

- `lavfi.blur` metadata value is the mean blur width — higher = more blurry.
- Use `metadata=print` after `blurdetect` to write per-frame scores to a file.
- Block-based mode (`block_width`/`block_height`) is faster and focuses on the sharpest regions.
- See `blockdetect` for detecting compression blocking artifacts (a different artifact type).
