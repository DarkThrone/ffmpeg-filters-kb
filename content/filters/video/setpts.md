+++
title = "setpts"
description = "Rewrite the presentation timestamps (PTS) of video frames using an arbitrary arithmetic expression."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["timing", "pts", "speed"]

[extra]
filter_type = "video"
since = ""
see_also = ["fps", "trim", "select"]
parameters = ["expr", "strip_fps"]
cohort = 1
source_file = "libavfilter/setpts.c"
+++

The `setpts` filter replaces the PTS (presentation timestamp) of each video frame with the result of a user-defined expression. This gives precise control over playback speed (fast motion / slow motion), timestamp normalization, fixed-rate output, and custom timing patterns. The audio equivalent is `asetpts`. Because `setpts` only modifies timestamps — not frame content — it is a zero-copy, lossless operation.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS-STARTPTS" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string (expr) | — | Expression evaluated for each frame to produce the new PTS value. |
| strip_fps | bool | `false` | If true, remove the framerate metadata. Recommended when sending to a VFR muxer. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | The current input frame's PTS in timebase units |
| `STARTPTS` | PTS of the very first frame |
| `TB` | The input timebase (e.g., `1/90000`) |
| `T` | Current frame time in seconds |
| `STARTT` | Time of the first frame in seconds |
| `N` | Sequential frame count starting from 0 |
| `FRAME_RATE` / `FR` | Input frame rate (only defined for CFR video) |
| `PREV_INPTS` | PTS of the previous input frame |
| `PREV_INT` | Time of the previous input frame in seconds |
| `PREV_OUTPTS` | PTS of the previous output frame |
| `PREV_OUTT` | Time of the previous output frame in seconds |
| `INTERLACED` | 1 if the current frame is interlaced |
| `T_CHANGE` | Time of the first frame after a runtime command was applied |

## Examples

### Reset timestamps to start at zero

Remove any initial timestamp offset so the output starts at PTS 0. This is almost always needed after `trim`.

```sh
ffmpeg -i input.mp4 -vf "trim=10:20,setpts=PTS-STARTPTS" output.mp4
```

### Slow motion (2x slower)

Double all PTS values to stretch the video to twice its original duration.

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" output.mp4
```

### Fast motion (4x faster)

Quarter the PTS values to compress the video to one-quarter its original duration.

```sh
ffmpeg -i input.mp4 -vf "setpts=0.25*PTS" output.mp4
```

### Force a fixed 25 fps rate from frame count

Generate synthetic PTS based on frame number, ignoring the original timestamps.

```sh
ffmpeg -i input.mp4 -vf "setpts=N/(25*TB)" output.mp4
```

### Add a 10-second delay to the video

Shift all timestamps forward by 10 seconds (in timebase units) without changing playback speed.

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS+10/TB" output.mp4
```

## Notes

- `setpts` modifies only PTS values; it does not insert or remove frames. To change the number of frames, use `fps` (to duplicate/drop) or `minterpolate` (to interpolate).
- For slow-motion that also needs extra frames inserted, combine `setpts` with `fps`: `setpts=2*PTS,fps=fps=50` stretches time and then fills in extra frames via duplication.
- The expression is evaluated in the timebase of the input; divide time-in-seconds values by `TB` to get the correct PTS units.
- For audio timestamps, use the `asetpts` filter instead. When doing speed changes, process both streams together to maintain sync.
