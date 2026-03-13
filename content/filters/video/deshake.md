+++
title = "deshake"
description = "Stabilize shaky video by detecting and compensating for small frame-to-frame motion."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["stabilize", "motion"]

[extra]
filter_type = "video"
since = ""
see_also = []
parameters = ["x", "y", "w", "h", "rx", "ry", "edge", "blocksize", "contrast", "search"]
cohort = 2
source_file = "libavfilter/vf_deshake.c"
+++

The `deshake` filter reduces camera shake by detecting the motion between consecutive frames within a search region and applying an inverse transformation. It operates entirely within a single pass and is straightforward to use, though for best results on heavily shaken footage, the two-pass `vidstabdetect`/`vidstabtransform` workflow (from the `vid.stab` library) provides superior quality.

## Quick Start

```sh
ffmpeg -i shaky.mp4 -vf "deshake" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | int | `-1` | Left edge of the analysis rectangle. -1 = auto (full width). |
| y | int | `-1` | Top edge of the analysis rectangle. |
| w | int | `-1` | Width of the analysis rectangle. -1 = use full frame width. |
| h | int | `-1` | Height of the analysis rectangle. |
| rx | int | `16` | Maximum horizontal search range in pixels. |
| ry | int | `16` | Maximum vertical search range in pixels. |
| edge | int | `mirror` | Edge fill method: `blank` (black border), `original`, `clamp`, `mirror`. |
| blocksize | int | `8` | Block size for motion estimation. Range: 4–128. |
| contrast | int | `125` | Minimum block contrast for motion estimation. Range: 1–255. |
| search | int | `exhaustive` | Search method: `exhaustive` or `less_exhaustive`. |

## Examples

### Basic stabilization

```sh
ffmpeg -i shaky.mp4 -vf "deshake" output.mp4
```

### Limit analysis to center of frame

Stabilize based on the center 50% of the frame (useful if edges have unrelated motion).

```sh
ffmpeg -i input.mp4 -vf "deshake=x=320:y=180:w=640:h=360" output.mp4
```

### Wider search range for heavily shaken footage

```sh
ffmpeg -i very_shaky.mp4 -vf "deshake=rx=32:ry=32" output.mp4
```

### Mirror edge fill (less distracting borders)

```sh
ffmpeg -i input.mp4 -vf "deshake=edge=mirror" output.mp4
```

## Notes

- `deshake` is a simple stabilizer suitable for handheld wobble. For complex motion (panning, zoom) or very heavy shake, use `vidstabdetect` + `vidstabtransform` (requires the `vid.stab` library).
- Edge fill artifacts are inevitable when compensating for motion; `edge=mirror` produces cleaner-looking results than `edge=blank` (black borders).
- `rx` and `ry` define the maximum allowed correction per frame. If the shake exceeds these values, the frame is only partially corrected.
- The filter operates in a single pass, so it cannot look ahead to smooth out slow drifts. `vidstabtransform` handles this better with its `smoothing` parameter.
