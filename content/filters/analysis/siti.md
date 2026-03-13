+++
title = "siti"
description = "Calculate Spatial Information (SI) and Temporal Information (TI) complexity scores per frame as defined in ITU-T Rec. P.910."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "complexity", "quality"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["vmafmotion", "ssim", "psnr"]
parameters = ["print_summary"]
cohort = 3
+++

The `siti` filter computes SI and TI metrics from ITU-T Rec. P.910, which are standard measures of visual complexity used in video codec benchmarking and adaptive bitrate research. SI measures spatial detail (via a Sobel edge filter on each frame), while TI measures temporal motion (via frame differencing). Per-frame values are emitted as metadata; an optional summary prints the maximum SI, maximum TI, and mean values at the end of the stream.

## Quick Start

```sh
# Compute SI/TI and print summary
ffmpeg -i input.mp4 -vf "siti=print_summary=1" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| print_summary | bool | `0` | Print average and max SI/TI to the console at the end of the stream. |

## Examples

### Print SI/TI summary for a file

```sh
ffmpeg -i input.mp4 -vf "siti=print_summary=1" -f null -
```

### Export per-frame SI/TI values to a CSV

```sh
ffmpeg -i input.mp4 -vf "siti,metadata=print:file=siti.txt" -f null -
```

### Compare SI/TI of two encodes

```sh
for f in original.mp4 compressed.mp4; do
  echo "=== $f ===" && ffmpeg -i "$f" -vf "siti=print_summary=1" -f null - 2>&1 | grep -E "SI|TI"
done
```

## Notes

- **SI** (Spatial Information): Standard deviation of a Sobel-filtered frame. High SI = lots of edges/texture. Typical range: 10–120.
- **TI** (Temporal Information): Standard deviation of the frame difference. High TI = lots of motion. Typical range: 5–100.
- Content in the upper-right quadrant (high SI, high TI) is the hardest to compress efficiently.
- Note: this implementation follows the legacy P.910 (11/21) specification; the current standard is P.910 (07/22).
