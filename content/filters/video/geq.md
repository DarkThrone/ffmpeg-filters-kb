+++
title = "geq"
description = "Apply a generic equation to each pixel using mathematical expressions for creative and corrective effects."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["pixel-manipulation", "expression", "creative"]

[extra]
filter_type = "video"
since = ""
see_also = ["lut"]
parameters = ["lum_expr", "cb_expr", "cr_expr", "r_expr", "g_expr", "b_expr", "a_expr", "interpolation"]
cohort = 2
source_file = "libavfilter/vf_geq.c"
+++

The `geq` filter evaluates a mathematical expression for every pixel in the frame, allowing completely custom per-pixel transformations. Unlike `lut` (which operates on a single channel's value), `geq` expressions can reference neighbouring pixels, the current coordinates, frame timing, and samples from any channel — enabling effects like custom blurs, edge detection, coordinate warping, and procedural patterns.

## Quick Start

```sh
# Simple luma inversion
ffmpeg -i input.mp4 -vf "geq=lum='maxval-lum(X,Y)'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| lum_expr / lum | string | Expression for luma (Y). |
| cb_expr / cb | string | Expression for Cb (U/blue-difference chroma). |
| cr_expr / cr | string | Expression for Cr (V/red-difference chroma). |
| r_expr / r | string | Expression for red (RGB input). |
| g_expr / g | string | Expression for green. |
| b_expr / b | string | Expression for blue. |
| a_expr / a | string | Expression for alpha. |
| interpolation | int | Interpolation for pixel sample functions: `nearest` or `bilinear`. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `X` | Current pixel x-coordinate. |
| `Y` | Current pixel y-coordinate. |
| `W` | Frame width in pixels. |
| `H` | Frame height in pixels. |
| `N` | Frame number (0-based). |
| `T` | Timestamp in seconds. |
| `SW` | Component horizontal scale factor (1 for luma, 0.5 for Cb/Cr on YUV 4:2:0). |
| `SH` | Component vertical scale factor. |
| `lum(x, y)` | Luma sample at coordinate (x, y). |
| `cb(x, y)` | Cb sample at coordinate (x, y). |
| `cr(x, y)` | Cr sample at coordinate (x, y). |
| `r(x, y)` | Red sample at (x, y). |
| `g(x, y)` | Green sample at (x, y). |
| `b(x, y)` | Blue sample at (x, y). |
| `alpha(x, y)` | Alpha sample at (x, y). |
| `maxval` | Maximum value for this component's bit depth (255 for 8-bit). |
| `minval` | Minimum value. |
| `negval` | `maxval - val` |

## Examples

### Horizontal flip

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(W-1-X,Y)':cb='cb((W-1-X)*SW,Y*SH)':cr='cr((W-1-X)*SW,Y*SH)'" output.mp4
```

### Brighten the left half only

```sh
ffmpeg -i input.mp4 -vf "geq=lum='if(lt(X,W/2),min(lum(X,Y)*1.5,maxval),lum(X,Y))'" output.mp4
```

### Pixelation effect

Round X and Y to a grid to create a pixelated look.

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(floor(X/16)*16,floor(Y/16)*16)':cb='cb(floor(X/16)*16*SW,floor(Y/16)*16*SH)':cr='cr(floor(X/16)*16*SW,floor(Y/16)*16*SH)'" output.mp4
```

### Vignette using distance from center

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(X,Y)*(1-hypot((X-W/2)/(W/2),(Y-H/2)/(H/2))*0.5)'" output.mp4
```

## Notes

- `geq` is evaluated per-pixel, per-frame, making it very flexible but relatively slow compared to dedicated filters. For simple LUT-style operations, use `lut`.
- The `p(x, y)` functions (or `lum(x,y)`, `r(x,y)`, etc.) allow accessing pixels at arbitrary coordinates, enabling convolution-style effects and warping.
- Expressions are parsed by the libavutil expression evaluator, which supports standard math functions: `sin`, `cos`, `sqrt`, `abs`, `min`, `max`, `gt`, `lt`, `eq`, `if`, `floor`, `ceil`, `hypot`, etc.
- For chroma planes on YUV 4:2:0 video, coordinates are scaled by `SW`/`SH` (0.5). Always multiply x by `SW` and y by `SH` when sampling chroma planes.
