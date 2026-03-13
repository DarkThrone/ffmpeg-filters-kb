+++
title = "kerndeint"
description = "Deinterlace video using Donald Graft's adaptive kernel deinterlacer, which applies processing only to detected interlaced regions."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "deinterlace"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["yadif", "bwdif", "fieldmatch"]
parameters = ["thresh", "map", "order", "sharp", "twoway"]
cohort = 3
source_file = "libavfilter/vf_kerndeint.c"
+++

The `kerndeint` filter deinterlaces video using Donald Graft's adaptive kernel algorithm. Unlike simple field-drop deinterlacers, `kerndeint` detects which pixel rows are actually interlaced (show combing) and applies processing only there, preserving quality in non-interlaced areas. It can optionally apply sharpening to recovered regions. For most use cases, `yadif` or `bwdif` are preferred, but `kerndeint` can work well for specific content types.

## Quick Start

```sh
ffmpeg -i interlaced.ts -vf kerndeint output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| thresh | int | `10` | Threshold (0–255) for detecting interlaced pixels. `0` = process every pixel. |
| map | bool | `0` | Paint detected interlaced pixels white (useful for tuning thresh). |
| order | bool | `0` | Field order: `0` = normal, `1` = swap fields. |
| sharp | bool | `0` | Enable additional sharpening on processed pixels. |
| twoway | bool | `0` | Enable two-way sharpening (sharper result). |

## Examples

### Default deinterlacing

```sh
ffmpeg -i interlaced.ts -vf kerndeint output.mp4
```

### Visualize which pixels are processed (tuning thresh)

```sh
ffplay -i interlaced.ts -vf "kerndeint=map=1:thresh=15"
```

### With sharpening

```sh
ffmpeg -i interlaced.ts -vf "kerndeint=sharp=1" sharpened.mp4
```

### Process every pixel (thresh=0) with two-way sharpening

```sh
ffmpeg -i interlaced.ts -vf "kerndeint=thresh=0:twoway=1" output.mp4
```

## Notes

- Set `thresh` to balance between processing too few pixels (residual combing) and too many (unnecessary blurring).
- Use `map=1` to visualize the detection mask — white pixels will be processed; tune `thresh` until combing areas are fully covered.
- For broadcast-quality deinterlacing, `yadif` with `mode=1` (send_field) is generally preferred.
- `sharp=1` and `twoway=1` can recover some sharpness lost during deinterlacing but may introduce ringing on hard edges.
