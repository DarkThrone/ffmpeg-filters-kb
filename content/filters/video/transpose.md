+++
title = "transpose"
description = "Transpose rows and columns in the input video to rotate 90 degrees and optionally flip."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "rotate", "flip"]

[extra]
filter_type = "video"
since = ""
see_also = ["rotate", "hflip", "vflip"]
parameters = ["dir", "passthrough"]
cohort = 1
+++

The `transpose` filter swaps the rows and columns of each video frame to achieve 90-degree rotations combined with optional flipping. It is the preferred method for rotating video by exactly 90 or 270 degrees because it operates as a simple pixel rearrangement with no interpolation, unlike the general `rotate` filter. The `passthrough` option lets you skip the operation when the input is already in the desired orientation.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dir | int | `0` (cclock_flip) | Transposition direction (see values below). |
| passthrough | int | `none` | Skip transposition if input geometry matches: `none`, `portrait`, or `landscape`. |

### `dir` values

| Value | Name | Effect |
|-------|------|--------|
| `0` / `cclock_flip` | Counter-clockwise + vertical flip | 90° CCW then flip vertically |
| `1` / `clock` | Clockwise | 90° clockwise |
| `2` / `cclock` | Counter-clockwise | 90° counter-clockwise |
| `3` / `clock_flip` | Clockwise + vertical flip | 90° CW then flip vertically |

## Examples

### Rotate 90 degrees clockwise

Correct portrait video shot on a phone that was held sideways.

```sh
ffmpeg -i input.mp4 -vf "transpose=clock" output.mp4
```

### Rotate 90 degrees counter-clockwise

Undo a clockwise rotation or correct the opposite orientation.

```sh
ffmpeg -i input.mp4 -vf "transpose=cclock" output.mp4
```

### Rotate 180 degrees

Apply `transpose` twice — each clockwise — to achieve a 180-degree rotation.

```sh
ffmpeg -i input.mp4 -vf "transpose=clock,transpose=clock" output.mp4
```

### Rotate only landscape videos, pass portrait through

Use `passthrough=landscape` to skip rotation when the video is already in portrait orientation.

```sh
ffmpeg -i input.mp4 -vf "transpose=dir=clock:passthrough=landscape" output.mp4
```

## Notes

- `transpose` is a pixel-copy operation with no interpolation, so it introduces no quality loss beyond the output encoding.
- The output dimensions are swapped: a 1920x1080 input becomes 1080x1920 after any 90-degree transpose.
- For arbitrary angles, use the `rotate` filter instead.
- On some hardware-accelerated pipelines (e.g., VAAPI, VideoToolbox), there are dedicated rotation options on the encoder that may be faster than software `transpose`.
