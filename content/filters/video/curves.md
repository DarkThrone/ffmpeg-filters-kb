+++
title = "curves"
description = "Adjust component curves using cubic splines with named presets or custom control points."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "grading", "tone"]

[extra]
filter_type = "video"
since = ""
see_also = ["eq", "colorbalance", "colorlevels"]
parameters = ["preset", "master", "red", "green", "blue", "all"]
cohort = 2
+++

The `curves` filter applies cubic spline tone curves to each color channel independently (or all together via `master`). It supports built-in presets for common looks and custom point lists for precise tonal control. It is the FFmpeg equivalent of the Curves tool in Photoshop or Lightroom.

## Quick Start

```sh
# Warm highlights, cool shadows
ffmpeg -i input.mp4 -vf "curves=r='0/0 0.5/0.56 1/1':b='0/0 0.5/0.44 1/1'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| preset | int | Named preset: `none`, `color_negative`, `cross_process`, `darker`, `increase_contrast`, `lighter`, `linear_contrast`, `medium_contrast`, `negative`, `strong_contrast`, `vintage`. |
| master / m | string | Master (applied to all channels) control points. Format: `x/y x/y ...` where each value is 0–1. |
| red / r | string | Red channel control points. |
| green / g | string | Green channel control points. |
| blue / b | string | Blue channel control points. |
| all | string | Alternative to `master`; sets all channels at once. |
| psfile | string | Path to a Photoshop `.acv` curves file. |

## Examples

### Apply a built-in vintage preset

```sh
ffmpeg -i input.mp4 -vf "curves=preset=vintage" output.mp4
```

### Increase contrast with S-curve

Lift shadows and push highlights apart for a contrast-boosting S-curve.

```sh
ffmpeg -i input.mp4 -vf "curves=master='0/0 0.25/0.18 0.5/0.5 0.75/0.82 1/1'" output.mp4
```

### Warm red/orange grade

Boost reds in highlights and reduce blues in shadows.

```sh
ffmpeg -i input.mp4 -vf "curves=r='0/0 0.5/0.55 1/1':b='0/0.05 0.5/0.45 1/0.9'" output.mp4
```

### Negative film look

Invert and adjust contrast for a film-negative effect.

```sh
ffmpeg -i input.mp4 -vf "curves=preset=color_negative" output.mp4
```

## Notes

- Control points are specified as space-separated `x/y` pairs, where `0/0` is the bottom-left (black) and `1/1` is the top-right (white). Points must be in ascending x order.
- At least 2 points are needed per curve; the curve is extrapolated outside the provided range.
- `preset` and custom per-channel points can be combined: the preset is applied first, then custom adjustments on top.
- For simple brightness/contrast/gamma, `eq` is faster. For full tonal sculpting, `curves` is more powerful.
