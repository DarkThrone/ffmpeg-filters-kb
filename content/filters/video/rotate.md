+++
title = "rotate"
description = "Rotate video frames by an arbitrary angle expressed in radians, with configurable output dimensions and fill color."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "rotate"]

[extra]
filter_type = "video"
since = ""
see_also = ["transpose", "hflip", "vflip"]
parameters = ["angle", "out_w", "out_h", "fillcolor", "bilinear"]
cohort = 1
source_file = "libavfilter/vf_rotate.c"
+++

The `rotate` filter rotates video frames clockwise by an arbitrary angle specified in radians. Unlike `transpose`, which only supports 90-degree increments, `rotate` handles any angle and can animate the rotation per frame using expressions. The output dimensions can be independently controlled, and any uncovered area is filled with a configurable color (or made transparent with `none`). Bilinear interpolation is enabled by default for smooth results.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "rotate=PI/4" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| angle (a) | string (expr) | `0` | Clockwise rotation angle in radians. Negative values rotate counter-clockwise. Evaluated per frame. |
| out_w (ow) | string (expr) | `iw` | Output frame width. Evaluated once at configuration time. |
| out_h (oh) | string (expr) | `ih` | Output frame height. Evaluated once at configuration time. |
| fillcolor (c) | string | `black` | Color used to fill areas not covered by the rotated frame. Use `none` for transparent. |
| bilinear | bool | `1` | Enable bilinear interpolation for smoother rotated output. |

## Expression Variables

The `angle`, `out_w`, and `out_h` options accept these constants:

| Variable | Description |
|----------|-------------|
| `n` | Sequential input frame number, starting from 0 |
| `t` | Time in seconds of the current frame |
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output width |
| `oh` / `out_h` | Output height |
| `hsub` / `vsub` | Chroma subsample values |
| `rotw(a)` | Minimum output width to fully contain the input rotated by `a` radians |
| `roth(a)` | Minimum output height to fully contain the input rotated by `a` radians |

## Examples

### Rotate 45 degrees clockwise

Convert the angle from degrees to radians by multiplying by `PI/180`.

```sh
ffmpeg -i input.mp4 -vf "rotate=45*PI/180" output.mp4
```

### Rotate 90 degrees counter-clockwise

Use a negative angle to go counter-clockwise.

```sh
ffmpeg -i input.mp4 -vf "rotate=-PI/2" output.mp4
```

### Expand canvas to show the full rotated frame

Use the `rotw`/`roth` helper functions to set the output size large enough to contain the entire rotated frame.

```sh
ffmpeg -i input.mp4 -vf "rotate=PI/6:ow=rotw(PI/6):oh=roth(PI/6)" output.mp4
```

### Animated continuous rotation

Rotate the video continuously, completing one full revolution every 5 seconds.

```sh
ffmpeg -i input.mp4 -vf "rotate=2*PI*t/5" output.mp4
```

### Oscillating wobble effect

Apply a sinusoidal rotation for a subtle wobble animation at 1 Hz with 5-degree amplitude.

```sh
ffmpeg -i input.mp4 -vf "rotate=5*PI/180*sin(2*PI*t)" output.mp4
```

## Notes

- Angles are in radians; multiply degrees by `PI/180` to convert.
- By default, the output canvas retains the input dimensions (`iw` x `ih`), which means corners of the rotated image will be clipped. Use `rotw`/`roth` to expand the canvas.
- Setting `fillcolor=none` produces transparent areas if the output format supports alpha (e.g., PNG); for opaque formats, `none` renders as black.
- `bilinear=0` disables interpolation for a faster but pixelated rotation — useful mainly for pixel art or debugging.
