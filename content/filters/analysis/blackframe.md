+++
title = "blackframe"
description = "Detect video frames that are almost entirely black, logging frame number, percentage of black pixels, and timestamp."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "detection", "scene"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["freezedetect", "silencedetect", "scdet"]
parameters = ["amount", "threshold"]
cohort = 3
+++

The `blackframe` filter scans each video frame and reports frames where the majority of pixels fall below a configurable luminance threshold. It is commonly used to detect chapter boundaries, bumpers, or commercial breaks — transitions that are often signaled by a black frame. The filter passes video through unchanged and logs detections to stderr.

## Quick Start

```sh
# Detect black frames in a video file
ffmpeg -i input.mp4 -vf blackframe -f null - 2>&1 | grep blackframe
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| amount | int | `98` | Percentage of pixels that must be below the threshold to flag the frame (0–100). |
| threshold / thresh | int | `32` | Pixel luma value (0–255) below which a pixel is considered black. |

## Examples

### Default black frame detection

```sh
ffmpeg -i movie.mkv -vf blackframe -f null - 2>&1 | grep blackframe
```

### Stricter detection (100% of pixels must be black)

```sh
ffmpeg -i input.mp4 -vf "blackframe=amount=100:threshold=16" -f null -
```

### Log to file for post-processing

```sh
ffmpeg -i input.mp4 -vf blackframe -f null - 2>&1 | grep blackframe > black_frames.txt
```

### Find chapter transitions (relaxed threshold)

```sh
ffmpeg -i movie.mkv -vf "blackframe=amount=90:thresh=40" -f null - 2>&1 | grep blackframe
```

## Notes

- Output format: `blackframe:pblack:N pblack:PCT pos:FILEPOS pts:PTS t:TIME_SECONDS`
- The filter also exports `lavfi.blackframe.pblack` frame metadata with the percentage.
- Lower `threshold` (e.g., 16) reduces false positives from slightly-off-black frames.
- For detecting scene cuts rather than pure black frames, see `scdet`.
