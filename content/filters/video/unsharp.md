+++
title = "unsharp"
description = "Sharpen or blur video using an unsharp mask applied to luma and chroma channels."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["sharpen", "blur", "enhancement"]

[extra]
filter_type = "video"
since = ""
see_also = ["gblur", "smartblur"]
parameters = ["luma_msize_x", "luma_msize_y", "luma_amount", "chroma_msize_x", "chroma_msize_y", "chroma_amount"]
cohort = 2
source_file = "libavfilter/vf_unsharp.c"
+++

The `unsharp` filter applies an unsharp mask to sharpen or blur the input video. Despite the name, positive `luma_amount` values sharpen the image by amplifying the difference between the original and a blurred copy, while negative values produce a net blur. It can operate on luma, chroma, or both channels independently.

## Quick Start

```sh
# Moderate sharpening
ffmpeg -i input.mp4 -vf "unsharp=5:5:1.0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_msize_x / lx | int | `5` | Luma matrix horizontal size (must be odd). Range: 3–23. |
| luma_msize_y / ly | int | `5` | Luma matrix vertical size (must be odd). Range: 3–23. |
| luma_amount / la | float | `1.0` | Luma sharpening strength. Positive=sharpen, negative=blur. Range: -1.5–1.5. |
| chroma_msize_x / cx | int | `5` | Chroma matrix horizontal size. |
| chroma_msize_y / cy | int | `5` | Chroma matrix vertical size. |
| chroma_amount / ca | float | `0.0` | Chroma sharpening strength. Default 0 leaves chroma unchanged. |
| alpha_msize_x / ax | int | `5` | Alpha matrix horizontal size. |
| alpha_msize_y / ay | int | `5` | Alpha matrix vertical size. |
| alpha_amount / aa | float | `0.0` | Alpha sharpening strength. |

## Examples

### Gentle sharpening

Useful for restoring detail after scaling or compression.

```sh
ffmpeg -i input.mp4 -vf "unsharp=5:5:0.5" output.mp4
```

### Strong sharpening

Aggressive sharpening for very soft or out-of-focus footage.

```sh
ffmpeg -i input.mp4 -vf "unsharp=7:7:1.5" output.mp4
```

### Blur both luma and chroma

Negative amounts produce a blur effect.

```sh
ffmpeg -i input.mp4 -vf "unsharp=5:5:-0.8:5:5:-0.5" output.mp4
```

### Sharpen luma only, leave chroma unchanged

Standard sharpening that avoids colour-noise amplification.

```sh
ffmpeg -i input.mp4 -vf "unsharp=lx=5:ly=5:la=1.0:ca=0.0" output.mp4
```

## Notes

- Matrix sizes must be odd numbers (3, 5, 7, …, 23). Larger matrices produce a wider blur before the difference is computed, affecting low-frequency detail.
- The default `luma_amount=1.0` is noticeable but not extreme; start with 0.5 and increase to taste.
- `chroma_amount=0` (the default) is usually correct: sharpening chroma can amplify colour noise, especially in skin tones.
- For edge-preserving sharpening that avoids amplifying noise, see `smartblur` with a negative `luma_strength`.
