+++
title = "allyuv"
description = "Generate a 4096×4096 frame containing every possible YUV color combination exactly once."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "source", "yuv", "debug"]

[extra]
filter_type = "source"
since = ""
see_also = ["allrgb", "testsrc"]
parameters = ["rate", "duration"]
cohort = 3
+++

The `allyuv` source generates a single 4096×4096 frame containing every possible YUV color combination exactly once — the YUV equivalent of `allrgb`. It is useful for testing color conversions, LUT filters, and chroma subsampling effects across the full YUV gamut. Output size is fixed at 4096×4096.

## Quick Start

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 allyuv.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |

## Examples

### Export as PNG

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 allyuv.png
```

### Apply YUV color grading and export

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 -vf "colorbalance=rs=0.1" allyuv_graded.png
```

## Notes

- Output is always fixed at 4096×4096 — the `size` parameter has no effect.
- Useful for verifying that color conversion filters preserve the full YUV gamut without clipping or banding.
- `allrgb` is the RGB-space equivalent.
