+++
title = "crop"
description = "Crop the input video to a specified rectangular region."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "crop", "resize"]

[extra]
filter_type = "video"
since = ""
see_also = ["scale", "pad", "overlay"]
parameters = ["w", "h", "x", "y", "keep_aspect", "exact"]
cohort = 1
+++

The `crop` filter extracts a rectangular sub-region from each video frame by specifying the output width, height, and the top-left corner coordinates within the input frame. Width and height default to the full input dimensions, and coordinates default to the center, so you only need to specify what you want to change. All parameters accept arithmetic expressions evaluated either once at init or per-frame, enabling dynamic panning crops.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "crop=1280:720:0:0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| w (out_w) | string (expr) | `iw` | Width of the cropped output area. |
| h (out_h) | string (expr) | `ih` | Height of the cropped output area. |
| x | string (expr) | `(iw-ow)/2` | Horizontal position of the top-left corner. Evaluated per frame. |
| y | string (expr) | `(ih-oh)/2` | Vertical position of the top-left corner. Evaluated per frame. |
| keep_aspect | bool | 0 | Preserve the input display aspect ratio by adjusting the sample AR. |
| exact | bool | 0 | Enable exact cropping for subsampled formats instead of rounding to the nearest subsample boundary. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output (cropped) width |
| `oh` / `out_h` | Output (cropped) height |
| `x` | Current computed x offset |
| `y` | Current computed y offset |
| `a` | Input aspect ratio (`iw/ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `n` | Frame number, starting from 0 |
| `t` | Timestamp in seconds |

## Examples

### Crop a fixed region

Extract a 640x480 rectangle starting at column 100, row 50.

```sh
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4
```

### Center crop to square

Crop the largest centered square from any video by using the shorter dimension as both width and height.

```sh
ffmpeg -i input.mp4 -vf "crop=in_h:in_h" output.mp4
```

### Crop to 16:9 from center

Remove letterbox or pillarbox bars by cropping to a specific aspect ratio without knowing the exact pixel offset.

```sh
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4
```

### Animated pan crop (left to right)

Move the crop window from left to right across the frame over time, creating a horizontal pan effect.

```sh
ffmpeg -i input.mp4 -vf "crop=640:480:t*100:0" output.mp4
```

### Remove 10-pixel border from all sides

Trim an even border by shrinking width and height by 20 pixels each and placing the origin at (10, 10).

```sh
ffmpeg -i input.mp4 -vf "crop=iw-20:ih-20:10:10" output.mp4
```

## Notes

- The `x` and `y` expressions are evaluated per frame and can reference each other and the current timestamp `t`, enabling panning crops.
- If the evaluated `x` or `y` would push the crop region outside the input frame, FFmpeg clamps it to the nearest valid value automatically.
- For YUV formats with chroma subsampling, crop coordinates are rounded to subsample boundaries unless `exact=1` is set.
- `w` and `h` expressions are evaluated only once at init (or on command), not per frame; use `x`/`y` for animation.
