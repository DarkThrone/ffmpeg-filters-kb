+++
title = "mpdecimate"
description = "Drop near-duplicate frames to reduce frame rate, useful for very low-bitrate encoding or fixing inverse-telecine artifacts."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["frame-rate", "duplicate", "telecine"]

[extra]
filter_type = "video"
since = ""
see_also = ["minterpolate", "idet", "framerate"]
parameters = ["max", "keep", "hi", "lo", "frac"]
cohort = 2
+++

The `mpdecimate` filter removes frames that are nearly identical to the previous frame, reducing the effective frame rate without re-encoding. Its primary use is for extremely low-bitrate streaming, but it also helps fix incorrectly inverse-telecined video (where duplicate fields create judder). The `hi`/`lo`/`frac` thresholds control how similar a frame must be to be considered a duplicate.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "mpdecimate" -vsync vfr output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| max | int | `0` | Max consecutive dropped frames (positive) or min interval between drops (negative). 0 = no limit. |
| keep | int | `0` | Max consecutive similar frames to keep before dropping. 0 = drop immediately. |
| hi | int | `768` (64×12) | High threshold per 8×8 block (pixel difference). |
| lo | int | `320` (64×5) | Low threshold per 8×8 block. |
| frac | float | `0.33` | Maximum fraction of blocks that may differ by more than `lo` (1.0 = whole image). |

## Examples

### Basic duplicate frame removal

```sh
ffmpeg -i input.mp4 -vf "mpdecimate" -vsync vfr output.mp4
```

### Limit to at most 2 consecutive dropped frames

```sh
ffmpeg -i input.mp4 -vf "mpdecimate=max=2" -vsync vfr output.mp4
```

### Strict deduplication (only exact duplicates)

```sh
ffmpeg -i input.mp4 -vf "mpdecimate=hi=64:lo=64:frac=0.1" -vsync vfr output.mp4
```

### Loose deduplication (drop near-duplicates aggressively)

```sh
ffmpeg -i talking_head.mp4 -vf "mpdecimate=hi=1024:lo=512:frac=0.5" -vsync vfr output.mp4
```

## Notes

- Always use `-vsync vfr` (or `-fps_mode vfr`) when outputting to a container to preserve correct timestamps after frame drops.
- A frame is dropped if no 8×8 block differs by more than `hi`, AND no more than `frac` of blocks differ by more than `lo`.
- Values for `hi` and `lo` represent pixel difference per 8×8 block: 64 = 1 unit per pixel on average within the block.
- `mpdecimate` is commonly used to detect and remove the duplicate frames left by a bad 3:2 pulldown telecine conversion.
