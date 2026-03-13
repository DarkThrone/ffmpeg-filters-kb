+++
title = "smartblur"
description = "Blur video without affecting edges and outlines, with separate control over luma, chroma, and alpha planes."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["blur", "denoise", "sharpening"]

[extra]
filter_type = "video"
since = ""
see_also = ["gblur", "boxblur", "unsharp"]
parameters = ["luma_radius", "luma_strength", "luma_threshold", "chroma_radius", "chroma_strength", "chroma_threshold"]
cohort = 2
source_file = "libavfilter/vf_smartblur.c"
+++

The `smartblur` filter blurs video while intelligently preserving edges and outlines. Unlike a simple Gaussian blur, it uses a threshold to selectively blur flat areas while leaving edges sharp — or, with negative strength values, sharpen detail. Separate parameters control the luma and chroma planes independently.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "smartblur=luma_radius=1.5:luma_strength=0.8" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_radius / lr | float | `1.0` | Gaussian blur radius for luma (Y). Range: 0.1–5.0. Larger = slower. |
| luma_strength / ls | float | `1.0` | Luma blur strength. 0–1 blurs, -1–0 sharpens. |
| luma_threshold / lt | int | `0` | Luma threshold (-30–30). 0 = filter all; positive = flat areas only; negative = edges only. |
| chroma_radius / cr | float | (luma_radius) | Gaussian blur radius for chroma. Defaults to luma_radius. |
| chroma_strength / cs | float | (luma_strength) | Chroma blur strength. Defaults to luma_strength. |
| chroma_threshold / ct | int | (luma_threshold) | Chroma threshold. Defaults to luma_threshold. |
| alpha_radius / ar | float | (luma_radius) | Gaussian blur radius for alpha plane. |
| alpha_strength / as | float | (luma_strength) | Alpha blur strength. |
| alpha_threshold / at | int | (luma_threshold) | Alpha threshold. |

## Examples

### Gentle content-aware blur (skin smoothing)

Blur flat areas while keeping edges crisp.

```sh
ffmpeg -i portrait.mp4 -vf "smartblur=lr=1.5:ls=0.8:lt=10" output.mp4
```

### Sharpen detail while blurring noise

Negative luma strength sharpens edges; threshold focuses on edges.

```sh
ffmpeg -i soft.mp4 -vf "smartblur=lr=1.0:ls=-0.5:lt=-3" output.mp4
```

### Blur only chroma (reduce color noise)

Keep luma sharp, blur only color channels.

```sh
ffmpeg -i noisy.mp4 -vf "smartblur=lr=0:ls=0:cr=2.0:cs=0.8" output.mp4
```

### Strong denoise for flat areas only

Threshold of 20 means only very flat areas get blurred.

```sh
ffmpeg -i input.mp4 -vf "smartblur=lr=3.0:ls=1.0:lt=20" output.mp4
```

## Notes

- `luma_strength` in [0.0, 1.0] blurs; in [-1.0, 0.0] sharpens. Values outside these ranges are clamped.
- `luma_threshold` = 0 applies blur everywhere; positive values target flat areas (good for noise reduction); negative values target edges (good for sharpening).
- If chroma/alpha options are not set, they inherit the corresponding luma value.
- For pure sharpening use `unsharp` which gives more control; `smartblur` excels at content-aware noise reduction.
