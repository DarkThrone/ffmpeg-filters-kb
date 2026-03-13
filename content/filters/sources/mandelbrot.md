+++
title = "mandelbrot"
description = "Render an animated Mandelbrot set fractal that progressively zooms toward a configurable point."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "fractal", "generative", "art"]

[extra]
filter_type = "source"
since = ""
see_also = ["cellauto", "life"]
parameters = ["size", "rate", "start_x", "start_y", "start_scale", "end_scale", "end_pts", "maxiter", "inner", "outer"]
cohort = 3
+++

The `mandelbrot` source renders the Mandelbrot set fractal and animates a smooth zoom toward a configurable complex-plane point. Both inner (set interior) and outer (escape time) coloring modes are configurable. The zoom is logarithmic from `start_scale` to `end_scale` over `end_pts` frames.

## Quick Start

```sh
ffplay -f lavfi "mandelbrot=size=800x600:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `640x480` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| start_x | double | `-0.7436...` | Initial real-axis position (zoom target). |
| start_y | double | `-0.1318...` | Initial imaginary-axis position. |
| start_scale | double | `3.0` | Initial scale (zoom out). |
| end_scale | double | `0.3` | Terminal scale (zoom in). |
| end_pts | double | `400` | Frame number at which zoom ends. |
| maxiter | int | `7189` | Maximum iterations per pixel (higher = sharper boundaries). |
| bailout | double | `10.0` | Escape radius. |
| inner | int | `mincol` | Interior coloring: `black`, `period`, `convergence`, `mincol`. |
| outer | int | `normalized_iteration_count` | Exterior coloring: `iteration_count`, `normalized_iteration_count`. |

## Examples

### Default zoom into the Seahorse Valley

```sh
ffplay -f lavfi "mandelbrot=size=800x600:rate=25"
```

### Zoom into the elephant valley

```sh
ffplay -f lavfi "mandelbrot=size=800x600:start_x=0.3:start_y=0.0:start_scale=0.5:end_scale=0.001"
```

### High-detail render

```sh
ffmpeg -f lavfi -i "mandelbrot=size=1920x1080:rate=25:maxiter=20000" -t 16 fractal.mp4
```

### Black interior, slower zoom

```sh
ffplay -f lavfi "mandelbrot=size=800x600:inner=black:end_pts=800"
```

## Notes

- The default zoom target (`start_x`, `start_y`) is the tip of the Seahorse Valley, a famous fractal detail region.
- Increase `maxiter` for sharper, more detailed boundaries — but each doubling roughly doubles render time.
- `normalized_iteration_count` outer coloring produces smooth color gradients; `iteration_count` produces banded coloring.
- The zoom is exponential — `end_scale / start_scale` gives the total zoom factor.
