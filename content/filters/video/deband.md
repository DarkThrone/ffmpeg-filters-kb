+++
title = "deband"
description = "Remove banding artifacts from video caused by insufficient bit depth or heavy compression."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["banding", "quality", "artifact-removal"]

[extra]
filter_type = "video"
since = ""
see_also = []
parameters = ["1thr", "2thr", "3thr", "4thr", "range", "direction", "blur", "coupling"]
cohort = 2
source_file = "libavfilter/vf_deband.c"
+++

The `deband` filter removes banding artifacts — visible color steps or bands in smooth gradients — that result from insufficient bit depth, aggressive lossy compression, or converting from 10-bit to 8-bit. It works by detecting areas where neighboring pixels have a similar value and smoothing them, replacing hard boundaries with gradual transitions.

## Quick Start

```sh
ffmpeg -i banded.mp4 -vf "deband" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| 1thr | float | `0.02` | Threshold for plane 1 (Y/luma). Lower = more aggressive. Range: 0.00003–0.5. |
| 2thr | float | `0.02` | Threshold for plane 2 (Cb/U). |
| 3thr | float | `0.02` | Threshold for plane 3 (Cr/V). |
| 4thr | float | `0.02` | Threshold for plane 4 (alpha). |
| range | int | `16` | Sampling range. Larger = catches more distant banding but slower. Range: 1–64. |
| direction | float | `6.28` | LFO direction sweep angle in radians. Default 6.28 (full 360°) = random directions. |
| blur | bool | `true` | Apply a blur to the detected banding areas for smooth transitions. |
| coupling | bool | `false` | If true, deband all planes together based on the luma plane decision. |

## Examples

### Remove banding from 8-bit SDR content

```sh
ffmpeg -i banded.mp4 -vf "deband" output.mp4
```

### Aggressive debanding (for heavy banding)

```sh
ffmpeg -i heavily_banded.mp4 -vf "deband=1thr=0.04:2thr=0.04:3thr=0.04" output.mp4
```

### Large range for wide, smooth gradients

```sh
ffmpeg -i sky_gradient.mp4 -vf "deband=range=32" output.mp4
```

### Deband before re-encoding to prevent banding propagation

```sh
ffmpeg -i input.mp4 -vf "deband" -c:v libx264 -crf 18 output.mp4
```

## Notes

- The thresholds (`1thr`–`4thr`) control sensitivity: lower values debands more aggressively but may smear fine detail. `0.02` is a safe default; increase to `0.04`–`0.06` for severe banding.
- `range` controls how far apart the comparison pixels are sampled. Wider gradients benefit from larger ranges (16–32).
- `blur=true` (default) applies smoothing to the banded regions — disable it to see only the banding detection result.
- Dithering before encoding can prevent banding from occurring in the first place; `deband` fixes it after the fact.
