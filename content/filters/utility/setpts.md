+++
title = "setpts"
description = "Recompute the presentation timestamps (PTS) of video frames using a configurable expression, enabling speed changes, timestamp fixes, and creative timing effects."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "timing", "pts", "speed"]

[extra]
filter_type = "utility"
since = ""
see_also = ["asetpts", "fps", "trim"]
parameters = ["expr"]
cohort = 3
source_file = "libavfilter/setpts.c"
+++

The `setpts` filter recomputes the PTS (Presentation Timestamp) of each video frame using a mathematical expression. This is the primary way to change video speed, fix broken timestamps, generate synthetic timestamps, or apply custom timing curves. The expression has access to the current PTS, frame number, timebase, and other variables.

## Quick Start

```sh
# Double the playback speed (2×)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" fast.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string | `PTS` | Expression evaluated per frame to set the output PTS. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | Current input PTS. |
| `N` | Frame number (starts at 0). |
| `T` | Time in seconds of current frame. |
| `TB` | Timebase of input. |
| `STARTPTS` | PTS of the first frame. |
| `STARTT` | Time in seconds of the first frame. |
| `FRAME_RATE` / `FR` | Framerate (only for CFR video). |
| `PREV_INPTS` / `PREV_OUTT` | Previous input/output PTS. |
| `INTERLACED` | Whether current frame is interlaced. |

## Examples

### 2× speed (half duration)

```sh
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" fast.mp4
```

### 0.5× speed (double duration, slow motion)

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" slow.mp4
```

### Reset timestamps to start from zero

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS-STARTPTS" fixed.mp4
```

### Force constant 25fps timestamps (fix VFR input)

```sh
ffmpeg -i vfr_input.mp4 -vf "setpts=N/(25*TB)" cfr_25fps.mp4
```

### Add 10-second offset to timestamps

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS+10/TB" offset.mp4
```

## Notes

- When changing speed with `setpts`, the audio is not affected — use `atempo` or `asetpts` to sync audio.
- `setpts=PTS-STARTPTS` is the standard fix for clips that start at a non-zero PTS (e.g., after `trim`).
- Combine `setpts=0.5*PTS` with `-r 60` to create smooth slow motion from high-fps source.
- The expression is evaluated per frame using FFmpeg's `av_expr_eval` — you can use any math function.
