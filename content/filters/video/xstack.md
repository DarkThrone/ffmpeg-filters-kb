+++
title = "xstack"
description = "Stack multiple video inputs into a custom 2D grid or layout within a single output frame."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["stack", "composite", "layout", "grid"]

[extra]
filter_type = "video"
since = ""
see_also = ["hstack", "vstack", "overlay"]
parameters = ["inputs", "layout", "grid", "shortest", "fill"]
cohort = 1
+++

The `xstack` filter arranges multiple video streams into a freely configurable 2D layout within a single output frame. Unlike `hstack` and `vstack`, which only support single rows or columns, `xstack` can create grids, irregular arrangements, and any combination of positions using a coordinate-based layout syntax. For two inputs the default is a 2x1 side-by-side layout; for all other counts a `layout` or `grid` must be explicitly specified.

## Quick Start

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:grid=2x2" \
  output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams. Overridden by `grid` when `grid` is set. |
| layout | string | — | Custom position specification for each input, pipe-separated. Format: `col_expr_row_expr` (e.g., `0_0\|w0_0\|0_h0\|w0_h0`). |
| grid | image_size | — | Fixed grid size in `COLUMNSxROWS` format (e.g., `2x2`). Mutually exclusive with `layout`. |
| shortest | bool | `0` | Terminate when the shortest input ends. |
| fill | string | `none` | Color used for unused pixels in the output frame. Default `none` leaves them undefined. |

### Layout syntax

In the `layout` option, each input's position is `col_expr_row_expr` where expressions can use:
- `wN` — width of input N
- `hN` — height of input N
- `+` to sum multiple values (e.g., `w0+w1`)

## Examples

### 2x2 grid from four inputs

Arrange four streams in a 2-column, 2-row grid.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:grid=2x2" \
  output.mp4
```

### Custom layout (manual positions)

Place four inputs in a 2x2 arrangement using explicit layout coordinates.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" \
  output.mp4
```

### 3x3 grid for nine camera feeds

Create a 3-column, 3-row surveillance-style monitor layout.

```sh
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -i 5.mp4 -i 6.mp4 -i 7.mp4 -i 8.mp4 -i 9.mp4 \
  -filter_complex \
    "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v][8:v]xstack=inputs=9:grid=3x3" \
  output.mp4
```

### Vertical strip (1x4)

Stack four streams in a single column using a custom layout.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex \
    "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2" \
  output.mp4
```

## Notes

- All inputs must share the same pixel format; normalize with `format` if needed. For `grid`, inputs within each row must also share the same height, and all rows must share the same width.
- Use `fill=black` (or any color) to fill gaps that appear when inputs have different sizes.
- `layout` and `grid` are mutually exclusive — specifying both results in an error.
- For simple two-input side-by-side or top-bottom layouts, `hstack` and `vstack` are simpler alternatives and have the same performance.
