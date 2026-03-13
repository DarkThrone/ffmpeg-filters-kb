+++
title = "noise"
description = "Add noise or grain to video with configurable strength, type, and per-component settings."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["noise", "grain", "effect"]

[extra]
filter_type = "video"
since = ""
see_also = []
parameters = ["all_seed", "all_strength", "all_flags", "c0_seed", "c0_strength", "c0_flags"]
cohort = 2
+++

The `noise` filter adds noise or grain to video frames. It can generate uniform, Gaussian, or temporally-correlated noise on any combination of color planes. Common uses include adding film grain for aesthetic purposes, simulating film stock, or reducing banding by dithering smooth gradients.

## Quick Start

```sh
# Add moderate grain to luma only
ffmpeg -i input.mp4 -vf "noise=alls=15:allf=t+u" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_seed / alls | int | `123457` | Random seed for all components. |
| all_strength / alls | int | `0` | Noise strength for all components. Range: 0–100. |
| all_flags / allf | flags | `0` | Noise type flags for all components. See below. |
| c0_seed | int | — | Seed for component 0 (Y/R). |
| c0_strength / c0s | int | `0` | Noise strength for component 0. |
| c0_flags / c0f | flags | `0` | Noise type for component 0. |
| c1_*/c2_*/c3_* | — | — | Per-component variants for planes 1, 2, and 3. |

### Flag values

| Flag | Description |
|------|-------------|
| `a` | Averaged noise (averages multiple noise samples, smoother). |
| `p` | Planar processing. |
| `s` | Saturation (apply noise only to saturated areas). |
| `u` | Uniform distribution noise. |
| `t` | Temporal noise (same noise pattern across frames, reduces flickering). |

## Examples

### Add film-grain-style noise (luma only)

```sh
ffmpeg -i input.mp4 -vf "noise=c0s=20:c0f=t+u" output.mp4
```

### Add grain to all planes

```sh
ffmpeg -i input.mp4 -vf "noise=alls=15:allf=t+u" output.mp4
```

### Anti-banding dithering noise

Very light noise to break up gradient banding.

```sh
ffmpeg -i gradient.mp4 -vf "noise=alls=4:allf=u" output.mp4
```

### Heavy noise for stylized effect

```sh
ffmpeg -i input.mp4 -vf "noise=alls=50:allf=u" output.mp4
```

## Notes

- Combine `t` (temporal) and `u` (uniform) flags: `allf=t+u` adds consistent, film-grain-like noise that doesn't flicker frame to frame.
- `all_strength` (or `alls`) is the main control: 5–10 for subtle grain, 20–40 for heavy grain, 50+ for extreme effect.
- Adding noise before encoding can actually *improve* compression efficiency on content with banding, because the noise gives the encoder more variation to quantize.
- Per-component flags (`c0f`, `c1f`, etc.) allow separate behavior: e.g., noisy luma but smooth chroma.
