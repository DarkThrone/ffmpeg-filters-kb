+++
title = "colorize"
description = "Overlay a solid color tint on video while preserving the original luminance."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["hue", "colorbalance"]
parameters = ["hue", "saturation", "lightness", "mix"]
cohort = 2
+++

The `colorize` filter applies a colored tint to video, similar to the duotone or colorize feature in Photoshop. It maps the video luminance through a specified hue and saturation, replacing all color information while keeping the lightness structure of the original. The `mix` parameter blends between the original and the colorized result.

## Quick Start

```sh
# Sepia-like warm orange tint
ffmpeg -i input.mp4 -vf "colorize=hue=30:saturation=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hue | float | `0.0` | Target hue in degrees. Range: 0–360. 0=red, 60=yellow, 120=green, 180=cyan, 240=blue, 300=magenta. |
| saturation | float | `0.5` | Saturation of the colorize effect. Range: 0–1. 0=grayscale, 1=fully colored. |
| lightness | float | `0.0` | Lightness shift. Range: -1–1. |
| mix | float | `1.0` | Blend between original (0) and fully colorized (1). |

## Examples

### Sepia tone

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=30:saturation=0.4:lightness=0.1" output.mp4
```

### Cold blue tint

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=210:saturation=0.5" output.mp4
```

### Subtle green tint (night vision feel)

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=120:saturation=0.3:mix=0.7" output.mp4
```

### 50% blend for soft color wash

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=45:saturation=0.6:mix=0.5" output.mp4
```

## Notes

- `hue=0` (red) with `saturation=0.4` and `lightness=0.05` produces a classic sepia look.
- `saturation=0` is equivalent to desaturation — full grayscale with no tint.
- Unlike `hue` (which rotates existing colors), `colorize` replaces ALL chroma with a single uniform hue.
- `mix=0.5` is often more appealing than a full 1.0 colorize, as it retains some of the original color character.
