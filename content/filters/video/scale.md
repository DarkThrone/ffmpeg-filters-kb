+++
title = "scale"
description = "Scale the input video size and/or convert the image format."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "resize", "format"]

[extra]
filter_type = "video"
since = ""
see_also = ["crop", "pad", "setsar"]
parameters = ["w", "h", "flags", "interl", "force_original_aspect_ratio", "force_divisible_by", "in_color_matrix", "out_color_matrix", "eval"]
cohort = 1
+++

The `scale` filter resizes video frames to the specified width and height, delegating the actual scaling to the libswscale library. It preserves the display aspect ratio by adjusting the sample aspect ratio, and can also convert between pixel formats as needed by the downstream filter chain. Use it whenever you need to change resolution, fit a video into a target size, or normalize dimensions before encoding.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| w (width) | string (expr) | input width | Output width expression. Use `-1` to preserve aspect ratio based on height. |
| h (height) | string (expr) | input height | Output height expression. Use `-1` to preserve aspect ratio based on width. |
| flags | string | (libswscale default) | Scaling algorithm flags passed to libswscale (e.g., `bilinear`, `bicubic`, `lanczos`). |
| interl | bool | 0 | Interlacing mode: `1` forces interlaced-aware scaling, `-1` auto-detects from frame flags. |
| force_original_aspect_ratio | int | 0 | `1` = decrease dimensions to fit, `2` = increase dimensions to fit, preserving the original AR. |
| force_divisible_by | int | 1 | When using `force_original_aspect_ratio`, ensure the output dimensions are divisible by this value. |
| in_color_matrix | int | auto | Input YCbCr color matrix (e.g., `bt709`, `bt601`). |
| out_color_matrix | int | auto | Output YCbCr color matrix. |
| eval | int | init | When to evaluate expressions: `init` (once) or `frame` (per frame). |

## Expression Variables

The `w` and `h` options accept arithmetic expressions with the following variables:

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output width (can reference `oh`) |
| `oh` / `out_h` | Output height (can reference `ow`) |
| `a` | Input aspect ratio (`iw / ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `n` | Input frame number |
| `t` | Input frame timestamp in seconds |

## Examples

### Scale to 720p keeping aspect ratio

Scale the width to 1280 and let FFmpeg calculate the height automatically to preserve the input aspect ratio. The `-1` value means "compute from the other dimension."

```sh
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4
```

### Scale to height, ensure width is divisible by 2

Use `-2` instead of `-1` to also guarantee the computed dimension is even — required by many codecs.

```sh
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4
```

### Halve the resolution

Use expressions relative to the input dimensions to produce output at half the original size.

```sh
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4
```

### Scale to fit within 1280x720 without upscaling

Use `force_original_aspect_ratio=decrease` to scale down a video so it fits within the target box while preserving AR.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease" output.mp4
```

### High-quality downscale with Lanczos

Use the `lanczos` flag for sharper results when downscaling, at a higher CPU cost.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720:flags=lanczos" output.mp4
```

## Notes

- When one dimension is set to `-1`, the filter computes the other to maintain the input AR. Use `-2` to also ensure the result is even (required by most YUV codecs).
- If both `w` and `h` are `0`, the input dimensions are passed through unchanged.
- The `flags` parameter controls the scaling algorithm quality; common values are `bilinear` (fast, lower quality), `bicubic` (balanced), and `lanczos` (high quality, slow).
- When chaining `scale` after `crop` or `pad`, order matters: scaling after cropping reduces work; scaling before can improve quality if the source is much larger than the crop target.
