+++
title = "selectivecolor"
description = "Adjust CMYK values selectively for specific color ranges such as reds, greens, blues, and neutrals."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "grading", "color-correction"]

[extra]
filter_type = "video"
since = ""
see_also = ["huesaturation", "curves"]
parameters = ["correction_method", "reds", "yellows", "greens", "cyans", "blues", "magentas", "whites", "neutrals", "blacks"]
cohort = 2
+++

The `selectivecolor` filter applies CMYK (Cyan, Magenta, Yellow, Black) color adjustments to specific color families in the image, similar to the Selective Color tool in Photoshop. You can independently adjust cyan/magenta/yellow/black components in nine color ranges: reds, yellows, greens, cyans, blues, magentas, whites, neutrals, and blacks.

## Quick Start

```sh
# Add cyan to blues for a cool, film-like look
ffmpeg -i input.mp4 -vf "selectivecolor=blues=0.1:-0.05:0:0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| correction_method | int | `absolute` | `absolute` (fixed adjustment) or `relative` (proportional to existing value). |
| reds | string | — | Adjustment for red tones: `cyan:magenta:yellow:black` (each -1 to 1). |
| yellows | string | — | Adjustment for yellow tones. |
| greens | string | — | Adjustment for green tones. |
| cyans | string | — | Adjustment for cyan tones. |
| blues | string | — | Adjustment for blue tones. |
| magentas | string | — | Adjustment for magenta tones. |
| whites | string | — | Adjustment for highlight tones. |
| neutrals | string | — | Adjustment for midtone neutral tones. |
| blacks | string | — | Adjustment for shadow/dark tones. |

## Examples

### Warm up reds (reduce cyan in reds)

```sh
ffmpeg -i portrait.mp4 -vf "selectivecolor=reds=-0.1:0:0.1:0" output.mp4
```

### Make greens more vibrant

```sh
ffmpeg -i landscape.mp4 -vf "selectivecolor=greens=-0.1:-0.05:0.15:0" output.mp4
```

### Add density to blacks (shadow lift)

```sh
ffmpeg -i input.mp4 -vf "selectivecolor=blacks=0:0:0:0.1" output.mp4
```

### Cool highlight look

```sh
ffmpeg -i input.mp4 -vf "selectivecolor=whites=0.05:-0.05:-0.1:0" output.mp4
```

## Notes

- Each color range takes four values in order: `cyan:magenta:yellow:black`. Positive cyan = more cyan (cooler/more blue-green); negative cyan = less cyan (warmer/more red).
- In `absolute` mode, the value is added directly; in `relative` mode, it is scaled by the existing component amount.
- Values outside the range of -1 to 1 will be clamped. Subtle adjustments of 0.05–0.15 are usually sufficient.
- Selective color gives finer control than `colorbalance` because it targets specific color families rather than tonal regions (shadows/midtones/highlights).
