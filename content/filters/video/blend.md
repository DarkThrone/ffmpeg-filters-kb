+++
title = "blend"
description = "Blend two video inputs together using compositing modes such as overlay, screen, multiply, and more."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["composite", "blend", "merge"]

[extra]
filter_type = "video"
since = ""
see_also = ["tblend", "overlay"]
parameters = ["all_mode", "all_opacity", "all_expr", "c0_mode", "c1_mode", "c2_mode", "c3_mode"]
cohort = 2
source_file = "libavfilter/vf_blend.c"
+++

The `blend` filter composites two video streams using Photoshop-style blending modes. It takes two inputs and applies a per-pixel blend operation to combine them. Each component can have a separate mode and opacity, or all components can share a single `all_mode`. This enables creative effects, colour grading, diffusion glow, and light leaks.

## Quick Start

```sh
# Overlay second video on first
ffmpeg -i base.mp4 -i overlay.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=overlay" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_mode | int | `normal` | Blend mode for all components. See mode list below. |
| all_opacity | float | `1.0` | Opacity of the blend (0=first input only, 1=fully blended). |
| all_expr | string | — | Custom blend expression per pixel. Variables: `X`, `Y`, `W`, `H`, `N`, `T`, `A` (top), `B` (bottom). |
| c0_mode | int | — | Blend mode for component 0 only. |
| c1_mode | int | — | Blend mode for component 1 only. |
| c2_mode | int | — | Blend mode for component 2 only. |
| c3_mode | int | — | Blend mode for component 3 (alpha) only. |

### Available blend modes

`normal`, `addition`, `grainmerge`, `and`, `average`, `burn`, `darken`, `difference`, `grainextract`, `divide`, `dodge`, `reflect`, `exclusion`, `extremity`, `freeze`, `glow`, `hardlight`, `hardmix`, `heat`, `lighten`, `linearlight`, `negation`, `or`, `overlay`, `phoenix`, `pinlight`, `softlight`, `screen`, `subtract`, `vividlight`, `xor`, `softdifference`, `geometric`, `harmonic`, `bleach`

## Examples

### Screen blend for glow effect

```sh
ffmpeg -i base.mp4 -i glow.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=screen:all_opacity=0.6" output.mp4
```

### Multiply blend for dark overlay

```sh
ffmpeg -i base.mp4 -i texture.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=multiply" output.mp4
```

### Difference blend for motion detection

Pixels that haven't changed appear black; changed pixels appear bright.

```sh
ffmpeg -i frame_a.mp4 -i frame_b.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=difference" output.mp4
```

### Custom expression blend

Blend only the bright parts of the second stream.

```sh
ffmpeg -i base.mp4 -i overlay.mp4 \
  -filter_complex "[0:v][1:v]blend=all_expr='if(gt(B,128),B,A)'" output.mp4
```

## Notes

- `blend` requires two inputs in the same size and format. Use `scale` and `format` to match them before blending.
- `all_mode=normal:all_opacity=0.5` is equivalent to a 50% crossfade between the two streams.
- For per-frame temporal blending (blending consecutive frames of the same stream), use `tblend`.
- The `all_expr` custom mode supports the same FFmpeg expression syntax as `geq`, with `A` = top layer pixel and `B` = bottom layer pixel.
