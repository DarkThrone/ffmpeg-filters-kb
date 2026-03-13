+++
title = "thumbnail"
description = "Select the most visually representative frame from each batch of N consecutive frames."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["thumbnail", "select", "frame"]

[extra]
filter_type = "video"
since = ""
see_also = ["select", "fps", "scale"]
parameters = ["n", "log"]
cohort = 1
source_file = "libavfilter/vf_thumbnail.c"
+++

The `thumbnail` filter analyzes batches of consecutive frames and selects the single most representative frame from each batch, discarding the rest. Representativeness is determined by histogram analysis — the frame whose histogram most closely resembles the mean of the batch is chosen. This makes it ideal for generating accurate thumbnails or preview images from video files. Combine it with `scale` and `-frames:v 1` to extract a single thumbnail image.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "thumbnail,scale=320:180" -frames:v 1 thumb.jpg
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| n | int | `100` | Number of frames per batch. One frame is selected per batch. |
| log | int | `info` | Logging level for displaying selected frame statistics. |

## Examples

### Extract a single representative thumbnail

Analyze the entire video (or at least the first batch of 100 frames) and save the best frame as a JPEG.

```sh
ffmpeg -i input.mp4 -vf "thumbnail,scale=320:180" -frames:v 1 thumb.jpg
```

### Finer-grained thumbnail grid (every 50 frames)

Set `n=50` to get a representative frame from each 50-frame window, producing more thumbnails for longer videos.

```sh
ffmpeg -i input.mp4 -vf "thumbnail=50,scale=160:90" -vsync vfr thumbs_%04d.jpg
```

### High-quality PNG thumbnail

Extract the representative frame at full resolution as a lossless PNG.

```sh
ffmpeg -i input.mp4 -vf "thumbnail=200" -frames:v 1 thumb.png
```

### Thumbnail with time offset

Start from 30 seconds into the video before running thumbnail selection to avoid opening-credit frames.

```sh
ffmpeg -ss 30 -i input.mp4 -vf "thumbnail=100,scale=640:360" -frames:v 1 thumb.jpg
```

## Notes

- Larger `n` values analyze more frames per batch, improving representativeness, but require proportionally more memory since all frames in the batch are buffered.
- When combined with `-frames:v 1`, only the first selected frame (from the first batch) is saved. Remove this flag to collect one thumbnail per batch across the whole video.
- The filter selects an existing frame, not an average; the output is always an actual decoded video frame.
- For fast, rough thumbnails, seeking to a fixed timestamp (`-ss`) is faster; `thumbnail` is better when you need a content-aware selection.
