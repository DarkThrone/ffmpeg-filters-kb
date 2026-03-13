+++
title = "boxblur"
description = "Apply a box (average) blur to video with separate radius and power settings per plane."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["blur"]

[extra]
filter_type = "video"
since = ""
see_also = ["gblur", "smartblur"]
parameters = ["luma_radius", "luma_power", "chroma_radius", "chroma_power", "alpha_radius", "alpha_power"]
cohort = 2
+++

The `boxblur` filter blurs video by averaging each pixel with its rectangular neighbourhood (a box blur). It applies the blur `power` times for each plane, with separate `radius` and `power` settings for luma, chroma, and alpha. Radii can be expressions referencing video dimensions.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "boxblur=2:1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_radius / lr | string | `2` | Luma blur radius in pixels. Can be an expression using `w`, `h`, `min(w,h)`, etc. |
| luma_power / lp | int | `2` | Number of times the box blur is applied to the luma plane. |
| chroma_radius / cr | string | — | Chroma blur radius. Defaults to `luma_radius`. |
| chroma_power / cp | int | — | Chroma blur iterations. Defaults to `luma_power`. |
| alpha_radius / ar | string | — | Alpha blur radius. Defaults to `luma_radius`. |
| alpha_power / ap | int | — | Alpha blur iterations. Defaults to `luma_power`. |

## Examples

### Gentle blur

```sh
ffmpeg -i input.mp4 -vf "boxblur=1:1" output.mp4
```

### Radius proportional to video size

Use 2% of the smaller dimension as the blur radius.

```sh
ffmpeg -i input.mp4 -vf "boxblur=lr='min(w,h)*0.02':lp=1" output.mp4
```

### Blur chroma more than luma

Smooth colour noise while keeping sharpness.

```sh
ffmpeg -i input.mp4 -vf "boxblur=lr=1:lp=1:cr=3:cp=2" output.mp4
```

### Heavy blur for background defocus

```sh
ffmpeg -i input.mp4 -vf "boxblur=5:3" output.mp4
```

## Notes

- A box blur applied once is fast but produces visible square artifacts. Increasing `power` (applying the blur multiple times) approximates a Gaussian blur.
- Radius expressions can use `iw`/`ih` (input width/height), `ow`/`oh` (output width/height), and `min(iw,ih)`.
- For a smoother, more natural blur, `gblur` (Gaussian) is generally preferred; `boxblur` is faster for large radii.
- Setting `chroma_power=0` skips chroma blurring entirely, leaving colour saturation fully sharp.
