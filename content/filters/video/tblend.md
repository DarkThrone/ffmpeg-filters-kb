+++
title = "tblend"
description = "Blend consecutive video frames together using compositing modes for motion blur and temporal effects."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["blend", "temporal", "composite"]

[extra]
filter_type = "video"
since = ""
see_also = ["blend"]
parameters = ["all_mode", "all_opacity", "all_expr", "c0_mode", "c1_mode", "c2_mode", "c3_mode"]
cohort = 2
+++

The `tblend` filter is the temporal variant of `blend`: it blends each frame with the previous frame from the same stream. This creates motion blur, ghosting, or temporal smoothing effects without requiring a second input. It accepts the same modes as `blend`.

## Quick Start

```sh
# Temporal frame blending (motion blur effect)
ffmpeg -i input.mp4 -vf "tblend=all_mode=average:all_opacity=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_mode | int | `normal` | Blend mode applied to all components. See `blend` for the full mode list. |
| all_opacity | float | `1.0` | Opacity of the blend. 0=show only current frame, 1=fully blended with previous. |
| all_expr | string | — | Custom expression. Variables include `A` (current frame) and `B` (previous frame). |
| c0_mode | int | — | Mode for component 0. |
| c1_mode | int | — | Mode for component 1. |
| c2_mode | int | — | Mode for component 2. |

### Available blend modes

Same as `blend`: `normal`, `addition`, `average`, `burn`, `darken`, `difference`, `divide`, `dodge`, `exclusion`, `hardlight`, `hardmix`, `lighten`, `linearlight`, `multiply`, `negation`, `or`, `overlay`, `pinlight`, `reflect`, `screen`, `softlight`, `subtract`, `vividlight`, `xor`, and others.

## Examples

### Smooth motion blur (average of current and previous frame)

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=average" output.mp4
```

### Ghost/smear effect with overlay mode

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=overlay:all_opacity=0.4" output.mp4
```

### Temporal difference (highlight changed pixels)

Produces a motion-detection-style output where still areas are black.

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=difference" output.mp4
```

### Reduce flicker with soft temporal averaging

```sh
ffmpeg -i flickery.mp4 -vf "tblend=all_mode=average:all_opacity=0.3" output.mp4
```

## Notes

- `tblend` operates on a single stream; `blend` composites two separate streams. They share the same mode options.
- `all_mode=average` is the most useful for motion blur: each output pixel is the mean of the current and previous frame pixel at the same location.
- `all_opacity` controls how much of the previous frame contributes. At 0.5 with `normal` mode, you get a 50/50 mix; at 1.0, the previous frame completely replaces the current.
- For high-quality frame interpolation (not simple blending), see `minterpolate`.
