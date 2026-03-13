+++
title = "median"
description = "Apply a median filter to remove salt-and-pepper noise by replacing each pixel with the median value from its neighborhood."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["denoise", "median", "noise-removal"]

[extra]
filter_type = "video"
since = ""
see_also = ["smartblur", "gblur", "nlmeans"]
parameters = ["radius", "radiusV", "percentile", "planes"]
cohort = 2
+++

The `median` filter replaces each pixel with the median value from a rectangular neighborhood, making it highly effective at removing impulse noise (salt-and-pepper noise) while preserving edges better than a Gaussian blur. The `percentile` option generalizes the filter — set it below 0.5 for an erosion-like effect (pick minimum) or above 0.5 for dilation (pick maximum).

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "median=radius=2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | int | `1` | Horizontal radius. Range: 1–127. Window width = 2*radius+1. |
| radiusV | int | `0` | Vertical radius. Range: 0–127. If 0, uses horizontal radius. |
| percentile | float | `0.5` | Percentile to select (0=min, 0.5=median, 1=max). |
| planes | int | `15` | Bitmask of planes to filter (15 = all). |

## Examples

### Remove salt-and-pepper noise

```sh
ffmpeg -i noisy.mp4 -vf "median=radius=1" output.mp4
```

### Stronger denoising with radius 3

```sh
ffmpeg -i input.mp4 -vf "median=radius=3" output.mp4
```

### Asymmetric window (wide horizontal, narrow vertical)

```sh
ffmpeg -i input.mp4 -vf "median=radius=3:radiusV=1" output.mp4
```

### Dilation effect (select maximum)

```sh
ffmpeg -i input.mp4 -vf "median=radius=2:percentile=1.0" output.mp4
```

### Filter only luma plane

```sh
ffmpeg -i input.mp4 -vf "median=radius=2:planes=1" output.mp4
```

## Notes

- `median` is ideal for removing isolated pixel noise (dust, scan artifacts) because the median is resistant to outliers.
- Larger radius = stronger filtering but slower processing and more blurring.
- `percentile=0.5` is true median; `percentile=0` picks minimum (erosion); `percentile=1` picks maximum (dilation).
- For temporal noise (noise that changes frame to frame), `atadenoise` or `hqdn3d` are more effective.
