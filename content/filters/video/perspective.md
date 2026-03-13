+++
title = "perspective"
description = "Correct or apply perspective distortion by mapping four corner points to new positions."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "geometry", "correction"]

[extra]
filter_type = "video"
since = ""
see_also = ["lenscorrection"]
parameters = ["x0", "y0", "x1", "y1", "x2", "y2", "x3", "y3", "interpolation", "sense"]
cohort = 2
+++

The `perspective` filter applies a perspective transformation by mapping four corner points of the input frame to new positions. It can be used to correct keystoning (when a projector or camera is not perpendicular to the subject), or to warp video to match a surface's perspective. The corners are numbered 0 (top-left), 1 (top-right), 2 (bottom-left), 3 (bottom-right).

## Quick Start

```sh
# Correct slight trapezoidal distortion
ffmpeg -i input.mp4 -vf "perspective=x0=30:y0=0:x1=1890:y1=0:x2=0:y2=1080:x3=1920:y3=1080" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x0 | string | `0` | X-coordinate of top-left corner. Expression, can use `iw`/`ih`. |
| y0 | string | `0` | Y-coordinate of top-left corner. |
| x1 | string | `iw` | X-coordinate of top-right corner. |
| y1 | string | `0` | Y-coordinate of top-right corner. |
| x2 | string | `0` | X-coordinate of bottom-left corner. |
| y2 | string | `ih` | Y-coordinate of bottom-left corner. |
| x3 | string | `iw` | X-coordinate of bottom-right corner. |
| y3 | string | `ih` | Y-coordinate of bottom-right corner. |
| interpolation | int | `linear` | Interpolation: `linear` or `cubic`. |
| sense | int | `source` | Interpretation: `source` (corners in input) or `destination` (corners in output). |

## Examples

### Correct trapezoid (top is narrower than bottom)

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=80:y0=0:x1=1840:y1=0:x2=0:y2=1080:x3=1920:y3=1080:sense=source" output.mp4
```

### Map video onto a tilted surface

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=100:y0=50:x1=1820:y1=30:x2=50:y2=1050:x3=1870:y3=1070" output.mp4
```

### Cubic interpolation for better quality

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=50:y0=0:x1=1870:y1=0:x2=0:y2=1080:x3=1920:y3=1080:interpolation=cubic" output.mp4
```

## Notes

- Corner coordinates are (x0,y0)=top-left, (x1,y1)=top-right, (x2,y2)=bottom-left, (x3,y3)=bottom-right.
- With `sense=source`, the coordinates specify where the input corners *are* (the filter maps them to a rectangle). With `sense=destination`, the coordinates specify where the corners should *go*.
- `cubic` interpolation gives better quality at the cost of speed; use it for final output.
- For barrel/pincushion lens correction (radial distortion), use `lenscorrection` instead.
