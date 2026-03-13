+++
title = "deflicker"
description = "Reduce temporal luminance flickering in video by smoothing per-frame brightness variations over a moving window."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "flicker", "stabilization"]

[extra]
filter_type = "utility"
since = ""
see_also = ["dejudder", "deshake"]
parameters = ["size", "mode", "bypass"]
cohort = 3
+++

The `deflicker` filter reduces temporal luminance flickering — rapid frame-to-frame brightness variation caused by fluorescent lighting, high-speed cameras shooting at certain shutter speeds, or digitized analog sources. It computes a moving-window average of frame brightness (using one of several averaging modes) and normalizes each frame toward that average. The video content is otherwise unmodified.

## Quick Start

```sh
ffmpeg -i flickery.mp4 -vf deflicker output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | int | `5` | Window size in frames (2–129). Larger = smoother but more blur across brightness changes. |
| mode / m | int | `am` | Averaging mode: `am` (arithmetic), `gm` (geometric), `hm` (harmonic), `qm` (quadratic), `cm` (cubic), `pm` (power), `median`. |
| bypass | bool | `0` | Don't modify frames, only attach metadata (useful for analysis). |

## Examples

### Default deflicker

```sh
ffmpeg -i flickery_timelapse.mp4 -vf deflicker stabilized.mp4
```

### Larger window for slower, steadier correction

```sh
ffmpeg -i flickery.mp4 -vf "deflicker=size=15" output.mp4
```

### Median mode (robust to outlier bright/dark frames)

```sh
ffmpeg -i input.mp4 -vf "deflicker=mode=median:size=9" output.mp4
```

### Analysis only (metadata without modification)

```sh
ffmpeg -i input.mp4 -vf "deflicker=bypass=1" -f null -
```

## Notes

- Arithmetic mean (`am`) is a good default for most content.
- `median` mode is more robust against frames that are extreme outliers (e.g., a single very bright flash), which could skew a mean-based correction.
- For timelapse footage, a larger window (10–30) and `gm` (geometric mean) typically produces the smoothest results.
- `bypass=1` attaches `lavfi.deflicker.scale` metadata without changing the video — useful to inspect the correction magnitude.
