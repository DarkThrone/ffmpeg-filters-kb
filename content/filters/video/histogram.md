+++
title = "histogram"
description = "Compute and display a color histogram showing the distribution of pixel values for each color component."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["analysis", "histogram", "broadcast"]

[extra]
filter_type = "video"
since = ""
see_also = ["waveform", "vectorscope", "signalstats"]
parameters = ["display_mode", "levels_mode", "components", "level_height", "scale_height", "fgopacity", "bgopacity"]
cohort = 2
source_file = "libavfilter/vf_histogram.c"
+++

The `histogram` filter renders a real-time color histogram for each frame, showing how pixel values are distributed across the 0–255 range for each color component. This is useful for exposure checking, detecting clipping or crushing, and verifying color balance. It supports stacked, parade, and overlay display modes, and linear or logarithmic scaling.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "histogram" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| display_mode / d | int | `stack` | Layout: `stack` (components below each other), `parade` (side by side), `overlay` (superimposed). |
| levels_mode / m | int | `linear` | Scale mode: `linear` or `logarithmic`. |
| components / c | int | `7` | Bitmask of components to display (1=Y/R, 2=U/G, 4=V/B, 7=all three). |
| level_height | int | `200` | Height of each histogram graph. Range: 50–2048. |
| scale_height | int | `12` | Height of the color scale below each graph. Range: 0–40. |
| fgopacity / f | float | `0.7` | Foreground (bars) opacity. |
| bgopacity / b | float | `0.5` | Background opacity. |
| colors_mode / l | int | `whiteonblack` | Color scheme: `whiteonblack`, `coloronblack`, `colorongray`, etc. |
| envelope / e | bool | `0` | Show peak envelope overlay. |
| ecolor / ec | color | `gold` | Color of the envelope. |

## Examples

### Basic histogram

```sh
ffmpeg -i input.mp4 -vf "histogram" output.mp4
```

### Parade mode (R/G/B side by side)

```sh
ffmpeg -i input.mp4 -vf "histogram=display_mode=parade:components=7" output.mp4
```

### Logarithmic scale for dark-heavy footage

```sh
ffmpeg -i night.mp4 -vf "histogram=levels_mode=logarithmic" output.mp4
```

### Show only luma channel

```sh
ffmpeg -i input.mp4 -vf "histogram=components=1" output.mp4
```

### Histogram beside original video

```sh
ffmpeg -i input.mp4 -vf "split[a][b];[a]histogram[h];[b][h]hstack" output.mp4
```

## Notes

- `stack` mode places component histograms vertically; `parade` places them side by side for easy comparison; `overlay` superimposes all components for compact display.
- `logarithmic` mode is useful for footage with many dark or near-black pixels (e.g. night scenes) where the linear scale makes highlights invisible.
- `components=7` shows all three components; use bitmask to select specific planes (e.g. `1` for Y-only in YUV, `7` for R+G+B).
- For broadcast monitoring, use `histogram` alongside `waveform` (for precise level checking) and `vectorscope` (for chroma/hue).
