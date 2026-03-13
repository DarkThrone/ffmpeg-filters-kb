+++
title = "huesaturation"
description = "Apply hue, saturation, and intensity adjustments to specific color ranges in a video."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "hue", "saturation"]

[extra]
filter_type = "video"
since = ""
see_also = ["hue", "colorbalance"]
parameters = ["hue", "saturation", "intensity", "colors", "strength", "rw", "gw", "bw"]
cohort = 2
source_file = "libavfilter/vf_huesaturation.c"
+++

The `huesaturation` filter adjusts hue, saturation, and intensity of video, with optional filtering to target specific color ranges. Unlike the simpler `hue` filter, it allows selective adjustments — for example, shifting only skin tones (reds) or making greens more vibrant without affecting blues. It is closer to the HSL Hue Saturation panel in Lightroom or Photoshop.

## Quick Start

```sh
# Shift all hues +30° and boost saturation
ffmpeg -i input.mp4 -vf "huesaturation=hue=30:saturation=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hue | float | `0.0` | Hue shift in degrees. Range: -180–180. |
| saturation | float | `0.0` | Saturation adjustment. Range: -3–3. Positive=more saturated, negative=less. |
| intensity | float | `0.0` | Intensity (luminance) shift. Range: -1–1. |
| colors | flags | `all` | Target color range: `r` (reds), `y` (yellows), `g` (greens), `c` (cyans), `b` (blues), `m` (magentas), `a` (all). Combine: `r+y`. |
| strength | float | `1.0` | Filtering strength for selective color mode. Range: 0–1. |
| rw | float | `0.333` | Red weight for luminance calculation. |
| gw | float | `0.334` | Green weight for luminance calculation. |
| bw | float | `0.333` | Blue weight for luminance calculation. |

## Examples

### Boost overall saturation

```sh
ffmpeg -i input.mp4 -vf "huesaturation=saturation=1.5" output.mp4
```

### Shift only reds (skin tones and warm colours)

```sh
ffmpeg -i portrait.mp4 -vf "huesaturation=hue=10:colors=r:strength=0.8" output.mp4
```

### Desaturate greens for forest footage

```sh
ffmpeg -i forest.mp4 -vf "huesaturation=saturation=-1:colors=g" output.mp4
```

### Convert to warm golden hour tone

Shift yellows toward orange and lift intensity slightly.

```sh
ffmpeg -i input.mp4 -vf "huesaturation=hue=-15:saturation=0.5:intensity=0.1:colors=y+r" output.mp4
```

## Notes

- `hue` shifts the entire hue wheel; `colors` limits the effect to specific segments of the wheel.
- `saturation` range is -3 to 3; values of -2 or below approach grayscale; above 2 produces heavily oversaturated output.
- `strength` controls how narrowly the color range filter targets. High strength (1.0) = only target colors affected; low strength = broader effect with more bleed.
- For a full desaturation (grayscale), set `saturation=-3` or use `monochrome` for more control over the conversion tone.
