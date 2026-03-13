+++
title = "overlay"
description = "Overlay a second video on top of the first at a specified position, supporting transparency and dynamic coordinates."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["overlay", "composite", "transform"]

[extra]
filter_type = "video"
since = ""
see_also = ["pad", "scale", "drawtext"]
parameters = ["x", "y", "eof_action", "eval", "shortest", "format", "repeatlast", "alpha"]
cohort = 1
source_file = "libavfilter/vf_overlay.c"
+++

The `overlay` filter composites two video streams together, placing the second input (the overlay) on top of the first input (the main video) at coordinates given by `x` and `y` expressions. Both inputs must be connected as separate streams using the filtergraph syntax. The filter supports alpha transparency, various output pixel formats, and dynamic position updates per frame, making it useful for watermarking, picture-in-picture, and logo placement.

## Quick Start

```sh
ffmpeg -i main.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | string (expr) | `0` | Horizontal position of the overlay's top-left corner on the main video. |
| y | string (expr) | `0` | Vertical position of the overlay's top-left corner on the main video. |
| eof_action | int | repeat | Action when the overlay input ends: `repeat` (last frame), `endall` (end output), `pass` (pass main through). |
| eval | int | frame | When to evaluate `x`/`y`: `init` (once) or `frame` (per frame). |
| shortest | bool | 0 | Terminate output when the shortest input ends. |
| format | int | yuv420 | Output pixel format: `yuv420`, `yuv444`, `rgb`, `gbrp`, `auto`, etc. |
| repeatlast | bool | 1 | Continue repeating the last overlay frame after its stream ends. |
| alpha | int | auto | Alpha compositing mode for the overlay: `straight`, `premultiplied`, or `auto`. |

## Expression Variables

The `x` and `y` options accept expressions with the following variables:

| Variable | Description |
|----------|-------------|
| `main_w` / `W` | Main (background) input width |
| `main_h` / `H` | Main (background) input height |
| `overlay_w` / `w` | Overlay input width |
| `overlay_h` / `h` | Overlay input height |
| `x` | Current computed x value |
| `y` | Current computed y value |
| `n` | Input frame number |
| `t` | Timestamp in seconds |
| `hsub` / `vsub` | Chroma subsample values of the output format |

## Examples

### Place a watermark in the bottom-right corner

Position a logo image 10 pixels from the right and bottom edges of the main video.

```sh
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  output.mp4
```

### Picture-in-picture (PiP)

Scale a second video to 320x180 and place it in the top-right corner.

```sh
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:180[pip]; [0:v][pip]overlay=main_w-320-10:10" \
  output.mp4
```

### Animated overlay that slides in from the left

Move the overlay from off-screen left to its final position over 2 seconds.

```sh
ffmpeg -i main.mp4 -i banner.png \
  -filter_complex "overlay=x='if(lt(t,2),t*200-overlay_w,200)':y=50" \
  output.mp4
```

### Overlay a semi-transparent PNG logo

Use a PNG with an alpha channel; the filter handles compositing automatically.

```sh
ffmpeg -i input.mp4 -i logo_alpha.png \
  -filter_complex "overlay=10:10:format=auto" \
  output.mp4
```

### Align two streams to the same start time

When inputs have different start timestamps, reset both to zero before overlaying to avoid sync issues.

```sh
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex \
    "[0:v]setpts=PTS-STARTPTS[bg]; \
     [1:v]setpts=PTS-STARTPTS[fg]; \
     [bg][fg]overlay=0:0" \
  output.mp4
```

## Notes

- Both inputs must be provided via the filtergraph; a single `-vf overlay` won't work — you need `-filter_complex` or `-lavfi`.
- When `eval=init`, the `t` and `n` variables evaluate to NaN; use `eval=frame` for time-dependent positioning.
- Output is in `yuv420` by default; use `format=auto` or `format=rgb` when the overlay contains full color information or alpha that yuv420 can't represent accurately.
- For static images used as overlays (e.g., logos), loop the image with `-loop 1` and use `shortest=1` or `eof_action=repeat` to keep it visible for the full duration of the main video.
