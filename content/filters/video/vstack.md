+++
title = "vstack"
description = "Stack two or more video inputs vertically into a single output frame."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["stack", "composite", "layout"]

[extra]
filter_type = "video"
since = ""
see_also = ["hstack", "xstack", "overlay"]
parameters = ["inputs", "shortest"]
cohort = 1
source_file = "libavfilter/vf_stack.c"
+++

The `vstack` filter places multiple video streams one above the other in a single column, producing a taller output frame. All input streams must share the same pixel format and the same width. It is faster than achieving the same result with `overlay` and `pad`, making it the preferred choice for vertical video strip compositions, top-and-bottom comparisons, and stacked camera layouts.

## Quick Start

```sh
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex "vstack" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams to stack vertically. |
| shortest | bool | `0` | When `1`, stop output when the shortest input ends. |

## Examples

### Stack two videos vertically

Place two videos of the same width one above the other.

```sh
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "vstack" output.mp4
```

### Normalize widths before stacking

Scale both inputs to the same width before stacking if they differ.

```sh
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "[0:v]scale=1280:-1[t]; [1:v]scale=1280:-1[b]; [t][b]vstack" \
  output.mp4
```

### Create a reflection effect

Stack the original video on top of a vertically flipped copy to simulate a surface reflection.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][copy]; [copy]vflip[flipped]; [orig][flipped]vstack" \
  output.mp4
```

### Stack three inputs vertically

Specify `inputs=3` to stack three streams in a column.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]vstack=inputs=3" \
  output.mp4
```

## Notes

- All input streams must have the same width and the same pixel format. Use `scale` and `format` filters to normalize before stacking.
- The output height is the sum of all input heights; the output width equals the shared input width.
- For more than two inputs arranged in a custom grid, use `xstack` instead.
- `vstack` is faster than using `pad` + `overlay` to create the same layout because it does not require compositing.
