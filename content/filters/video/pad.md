+++
title = "pad"
description = "Add padding around the input video to reach a specified output size, placing the original frame at given coordinates."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "pad", "resize"]

[extra]
filter_type = "video"
since = ""
see_also = ["scale", "crop", "overlay"]
parameters = ["width", "height", "x", "y", "color", "eval", "aspect"]
cohort = 1
+++

The `pad` filter adds colored borders around the input video to produce a larger output canvas. You specify the desired output dimensions and the `(x, y)` offset at which the original frame is placed. All parameters accept arithmetic expressions, making it easy to center the input, create letterbox/pillarbox effects, or add exact pixel margins. The padding area is filled with a configurable color (default black).

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| width (w) | string (expr) | `0` (= input width) | Width of the output padded frame. |
| height (h) | string (expr) | `0` (= input height) | Height of the output padded frame. |
| x | string (expr) | `0` | Horizontal offset of the input frame within the padded canvas. Negative values center the input. |
| y | string (expr) | `0` | Vertical offset of the input frame within the padded canvas. Negative values center the input. |
| color | color | `black` | Fill color for the padded area. |
| eval | int | `init` | When to evaluate expressions: `init` (once) or `frame` (per frame). |
| aspect | rational | — | Pad to fit a given display aspect ratio instead of a fixed resolution. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output (padded) width |
| `oh` / `out_h` | Output (padded) height |
| `x` / `y` | Offset values (can reference each other) |
| `a` | Input aspect ratio (`iw/ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `hsub` / `vsub` | Chroma subsample values |

## Examples

### Letterbox to 16:9 (add black bars)

Take a 4:3 video and pad it to 16:9 by adding bars on the left and right sides.

```sh
ffmpeg -i input_4_3.mp4 -vf "pad=ih*16/9:ih:(ow-iw)/2:0" output.mp4
```

### Center video in a 1920x1080 canvas

Place the input at the center of a Full HD frame, regardless of its original size.

```sh
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### Add a uniform 20-pixel border

Extend each side by 20 pixels, placing the input at (20, 20).

```sh
ffmpeg -i input.mp4 -vf "pad=iw+40:ih+40:20:20" output.mp4
```

### Pad to 16:9 aspect ratio with white background

Use the `aspect` option with a custom fill color.

```sh
ffmpeg -i input.mp4 -vf "pad=aspect=16/9:color=white:x=(ow-iw)/2:y=(oh-ih)/2" output.mp4
```

### Pad for 9:16 portrait format

Add pillarbox bars to a landscape video for a vertical platform.

```sh
ffmpeg -i landscape.mp4 -vf "scale=-2:1920,pad=1080:1920:(ow-iw)/2:0" portrait.mp4
```

## Notes

- The `x` and `y` expressions can reference `ow`/`oh`, allowing centering math like `(ow-iw)/2` before the final dimensions are known.
- If `x` or `y` evaluates to a negative number, the filter automatically centers the input within the padded area.
- To add padding and then scale, chain `pad` before `scale`; to add padding to a scaled result, chain `scale` before `pad`.
- The `color` parameter accepts any FFmpeg color string including hex (`#RRGGBB`), named colors, and colors with alpha (`black@0.5`).
