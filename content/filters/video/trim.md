+++
title = "trim"
description = "Extract a continuous sub-section of the input video by specifying start and end points by time or frame number."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["timing", "trim", "cut"]

[extra]
filter_type = "video"
since = ""
see_also = ["setpts", "select", "concat"]
parameters = ["start", "end", "duration", "start_frame", "end_frame", "start_pts", "end_pts"]
cohort = 1
+++

The `trim` filter retains one continuous segment of the input video, discarding everything before the start point and everything after the end point. Unlike stream-level seeking (`-ss` / `-t`), `trim` operates at the filter level, which enables accurate frame-level trimming in complex filtergraphs. Note that `trim` does not reset timestamps — chain it with `setpts=PTS-STARTPTS` afterward if you need the output to start at time zero.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "trim=start=10:end=20,setpts=PTS-STARTPTS" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | duration | — | Timestamp of the first frame to keep. |
| end | duration | — | Timestamp of the first frame to drop (exclusive). |
| duration | duration | — | Maximum duration of the output section. |
| start_frame | int64 | — | Frame number (0-based) of the first frame to keep. |
| end_frame | int64 | — | Frame number of the first frame to drop. |
| start_pts | int64 | — | Start timestamp in timebase units. |
| end_pts | int64 | — | End timestamp in timebase units. |

## Examples

### Trim from 10 to 30 seconds

Keep only the segment between 10 and 30 seconds and reset timestamps to start at zero.

```sh
ffmpeg -i input.mp4 -vf "trim=start=10:end=30,setpts=PTS-STARTPTS" output.mp4
```

### Keep only the first 5 seconds

Use `duration` to specify an exact clip length starting from the beginning.

```sh
ffmpeg -i input.mp4 -vf "trim=duration=5,setpts=PTS-STARTPTS" output.mp4
```

### Trim to a specific minute

Equivalent to selecting the second minute of the input (60 to 120 seconds).

```sh
ffmpeg -i input.mp4 -vf "trim=60:120,setpts=PTS-STARTPTS" output.mp4
```

### Frame-accurate trim by frame number

Keep frames 100 through 299 (200 frames total) regardless of timestamps.

```sh
ffmpeg -i input.mp4 -vf "trim=start_frame=100:end_frame=300,setpts=PTS-STARTPTS" output.mp4
```

### Trim in a filtergraph alongside audio

When trimming both video and audio, use `atrim` for the audio stream and synchronize the start points.

```sh
ffmpeg -i input.mp4 \
  -filter_complex \
    "[0:v]trim=start=5:end=15,setpts=PTS-STARTPTS[v]; \
     [0:a]atrim=start=5:end=15,asetpts=PTS-STARTPTS[a]" \
  -map "[v]" -map "[a]" output.mp4
```

## Notes

- `trim` does not alter the PTS values of kept frames. Always chain `setpts=PTS-STARTPTS` after `trim` to produce output that starts at time zero, as many muxers and players expect this.
- When both time-based and frame-based start/end options are set simultaneously, the filter keeps frames that satisfy at least one of the constraints.
- The `end` point is exclusive: the frame with exactly `end` timestamp will not appear in the output.
- For simple segment extraction without filtergraph overhead, stream-level `-ss` and `-t` or `-to` options are faster since they can seek and avoid decoding discarded frames.
