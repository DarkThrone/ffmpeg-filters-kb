+++
title = "hstack"
description = "Stack two or more video inputs side by side horizontally into a single output frame."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["stack", "composite", "layout"]

[extra]
filter_type = "video"
since = ""
see_also = ["vstack", "xstack", "overlay"]
parameters = ["inputs", "shortest"]
cohort = 1
source_file = "libavfilter/vf_stack.c"
+++

The `hstack` filter places multiple video streams side by side in a single row, producing a wider output frame. All input streams must share the same pixel format and the same height. It is faster than achieving the same result with `overlay` and `pad`, making it the preferred choice for side-by-side video comparisons, dual-camera layouts, and horizontal strip compositions.

## Quick Start

```sh
ffmpeg -i left.mp4 -i right.mp4 -filter_complex "hstack" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams to stack horizontally. |
| shortest | bool | `0` | When `1`, stop output when the shortest input ends. |

## Examples

### Side-by-side comparison of two videos

Place two videos of the same height next to each other for a direct comparison.

```sh
ffmpeg -i original.mp4 -i processed.mp4 \
  -filter_complex "hstack" comparison.mp4
```

### Normalize heights before stacking

Scale both inputs to the same height before stacking if they differ.

```sh
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v]scale=-1:480[l]; [1:v]scale=-1:480[r]; [l][r]hstack" \
  output.mp4
```

### Stack three inputs horizontally

Specify `inputs=3` to stack three streams in a row.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]hstack=inputs=3" \
  output.mp4
```

### Stop when the shorter stream ends

Use `shortest=1` to cut off the output when the first input finishes.

```sh
ffmpeg -i long.mp4 -i short.mp4 \
  -filter_complex "hstack=shortest=1" \
  output.mp4
```

## Notes

- All input streams must have the same height and the same pixel format. Use `scale` and `format` filters to normalize before stacking.
- The output width is the sum of all input widths; the output height equals the shared input height.
- For more than two inputs arranged in a custom grid, use `xstack` instead.
- `hstack` is faster than using `pad` + `overlay` to create the same layout because it does not require compositing.
