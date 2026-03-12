+++
title = "drawbox"
description = "Draw a colored rectangle (box) onto the input video, with configurable position, size, thickness, and color."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["annotation", "overlay", "debug"]

[extra]
filter_type = "video"
since = ""
see_also = ["drawtext", "overlay", "crop"]
parameters = ["x", "y", "width", "height", "color", "thickness", "replace"]
cohort = 1
+++

The `drawbox` filter draws a rectangle border (or a filled rectangle) directly onto video frames. It is frequently used for debugging bounding boxes from detection pipelines, highlighting regions of interest, adding visual framing to clips, or creating simple graphic overlays. All geometry parameters accept arithmetic expressions evaluated per frame, enabling animated boxes.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=50:w=200:h=150:color=red:t=3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | string (expr) | `0` | Horizontal position of the left edge of the box. |
| y | string (expr) | `0` | Vertical position of the top edge of the box. |
| width (w) | string (expr) | `0` (= input width) | Width of the box. |
| height (h) | string (expr) | `0` (= input height) | Height of the box. |
| color (c) | string | `black` | Box color. Supports `color@alpha` notation and the special value `invert`. |
| thickness (t) | string (expr) | `3` | Thickness of the box border in pixels. Use `fill` for a solid filled box. |
| replace | bool | `0` | When `1`, overwrite video pixels including alpha. Default composites over the video. |
| box_source | string | — | Use bounding box from frame side-data (e.g., `side_data_detection_bboxes`) instead of manual parameters. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `x` / `y` | Current box position |
| `w` / `h` | Current box dimensions |
| `t` | Box border thickness |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `hsub` / `vsub` | Chroma subsample values |

## Examples

### Draw a red border box

Outline a region with a 3-pixel red border.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=50:w=200:h=150:color=red:t=3" output.mp4
```

### Draw a semi-transparent filled box

Create a translucent highlight rectangle by using `t=fill` and `@alpha` on the color.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=10:y=10:w=300:h=100:color=yellow@0.5:t=fill" output.mp4
```

### Black border around the entire frame

Draw a box that traces the frame edge — useful for adding a clean visual border.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black:t=4" output.mp4
```

### Inverted color box

Use `invert` as the color to draw a box whose color is the complement of the video content underneath.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=50:y=50:w=100:h=100:color=invert:t=2" output.mp4
```

### Animated box tracking position over time

Move the box diagonally across the frame as a function of the frame timestamp.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=t*30:y=t*20:w=100:h=60:color=lime:t=2" output.mp4
```

## Notes

- The `color` parameter accepts any FFmpeg color string, including hex codes (`#FF0000`), named colors, and alpha suffixes (`red@0.3`).
- Setting `t=fill` creates a filled rectangle; any numeric value draws only the border at that pixel thickness.
- When `box_source=side_data_detection_bboxes` is set, the `x`, `y`, `w`, and `h` parameters are ignored in favor of bounding box data embedded in the frame side-data by detection filters.
- For multiple boxes at different positions, chain multiple `drawbox` filters separated by commas.
