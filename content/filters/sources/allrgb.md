+++
title = "allrgb"
description = "Generate a 4096×4096 frame containing every possible 24-bit RGB color exactly once."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "source", "color", "debug"]

[extra]
filter_type = "source"
since = ""
see_also = ["allyuv", "testsrc"]
parameters = ["rate", "duration"]
cohort = 3
+++

The `allrgb` source generates a single 4096×4096 frame (16 million pixels) containing every possible 24-bit RGB color exactly once. It is a mathematically complete color space visualization, useful for testing LUT (Look Up Table) filters, color transforms, and any processing that needs to operate on the entire RGB gamut simultaneously. Output size is fixed at 4096×4096 and cannot be changed.

## Quick Start

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 allrgb.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Frames per second (for animated output). |
| duration / d | duration | infinite | Total duration. |

## Examples

### Export single frame as PNG

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 allrgb.png
```

### Apply a LUT and verify it covers all colors

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 -vf "lut3d=lut_file.cube" allrgb_graded.png
```

### Generate a short animated clip

```sh
ffmpeg -f lavfi -i "allrgb" -t 1 allrgb.mp4
```

## Notes

- Output is always 4096×4096 pixels — this cannot be resized with the `size` parameter (unlike other test sources).
- Each of the 16,777,216 pixels has a unique RGB value; the arrangement is space-filling curve order.
- `allyuv` is the YUV equivalent, generating all possible YUV color combinations.
- The output file will be large (~50 MB as lossless PNG); use with care.
