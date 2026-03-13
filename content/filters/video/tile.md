+++
title = "tile"
description = "Arrange consecutive video frames into a tiled grid layout in a single output frame."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["tile", "mosaic", "layout"]

[extra]
filter_type = "video"
since = ""
see_also = ["hstack", "vstack"]
parameters = ["layout", "nb_frames", "margin", "padding", "color", "overlap", "init_padding"]
cohort = 2
source_file = "libavfilter/vf_tile.c"
+++

The `tile` filter arranges consecutive input frames into a grid, producing a single output frame that contains a mosaic of multiple frames. It is useful for creating contact sheets, thumbnail previews, or visualizing temporal information across multiple frames at once.

## Quick Start

```sh
# Create a 4x3 grid of frames
ffmpeg -i input.mp4 -vf "tile=4x3" -frames:v 1 thumbnail.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| layout | image_size | `6x5` | Grid dimensions as `columns x rows`. |
| nb_frames | int | `0` | Total number of frames to tile. 0 = columns × rows. |
| margin | int | `0` | Outer border in pixels around the entire grid. |
| padding | int | `0` | Spacing between individual tiles in pixels. |
| color | color | `black` | Fill colour for unused grid cells and padding/margin. |
| overlap | int | `0` | Number of tiles to overlap (reuse) from the previous frame. |
| init_padding | int | `0` | Number of empty tiles to add at the start. |

## Examples

### One-frame contact sheet (4×3 grid)

Sample one frame every N frames to get 12 evenly-spaced thumbnails.

```sh
ffmpeg -i input.mp4 -vf "fps=1/10,tile=4x3" -frames:v 1 sheet.png
```

### Animated tile showing every 4 frames

Update the grid every 4 frames.

```sh
ffmpeg -i input.mp4 -vf "tile=2x2" output.mp4
```

### Add padding and margin

```sh
ffmpeg -i input.mp4 -vf "fps=1,tile=3x3:margin=5:padding=3:color=white" -frames:v 1 sheet.jpg
```

### Thumbnail strip for video scrubbing

One row of 10 thumbnails.

```sh
ffmpeg -i input.mp4 -vf "fps=1/5,scale=160:-1,tile=10x1" -frames:v 1 strip.png
```

## Notes

- `tile` collects input frames and outputs one grid frame after every `nb_frames` input frames. With `nb_frames=12` (4×3), it emits one grid output for every 12 input frames.
- Combine with `fps=1/N` or `select` to extract evenly-spaced frames before tiling, rather than tiling every frame.
- The output frame size is `(input_width × columns) + (padding × (columns-1)) + (margin × 2)` — watch for very large output sizes with high-resolution inputs.
- Use `-frames:v 1` to extract just one grid image from the start of the stream.
