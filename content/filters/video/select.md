+++
title = "select"
description = "Select or filter video frames based on an expression, passing only frames that match specified criteria."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["select", "filter", "frame", "timing"]

[extra]
filter_type = "video"
since = ""
see_also = ["setpts", "trim", "thumbnail"]
parameters = ["expr", "outputs"]
cohort = 1
source_file = "libavfilter/f_select.c"
+++

The `select` filter evaluates an expression for each input frame and passes or discards the frame based on the result. Frames for which the expression evaluates to zero are dropped; non-zero values route the frame to an output (the integer ceiling of the result minus 1 determines which output index for multi-output use). This enables precise frame selection based on timestamp, frame type (I/P/B), scene change score, key frame status, or any arithmetic combination of these variables.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframes_%04d.jpg
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr (e) | string | — | Expression evaluated for each frame. Non-zero = pass; zero = discard. |
| outputs (n) | int | `1` | Number of output streams. Frames are routed to output `ceil(result)-1`. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Sequential frame number, starting from 0 |
| `selected_n` | Sequential number of selected frames |
| `prev_selected_n` | Frame number of the previously selected frame |
| `t` | Frame timestamp in seconds |
| `pts` | Frame PTS in timebase units |
| `prev_pts` | PTS of the previously filtered frame |
| `prev_selected_pts` | PTS of the previously selected frame |
| `prev_selected_t` | Timestamp of the previously selected frame in seconds |
| `start_pts` | PTS of the first non-NaN frame |
| `start_t` | Timestamp of the first frame in seconds |
| `pict_type` | Frame type: `I`, `P`, `B`, `S`, `SI`, `SP`, `BI` |
| `key` | `1` if the frame is a keyframe, `0` otherwise |
| `scene` | Scene change score (0.0 to 1.0); higher = more likely a new scene |
| `interlace_type` | `PROGRESSIVE`, `TOPFIRST`, or `BOTTOMFIRST` |
| `TB` | Input timebase |
| `concatdec_select` | Used with the concat demuxer to filter in/out points |

## Examples

### Extract only keyframes

Select only I-frames (keyframes) and save them as images.

```sh
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframes_%04d.jpg
```

### Extract one frame per second

Use the timestamp to select one frame at each whole second.

```sh
ffmpeg -i input.mp4 -vf "select='isnan(prev_selected_t)+gte(t-prev_selected_t,1)'" -vsync vfr fps1_%04d.jpg
```

### Detect scene changes

Select frames where the scene change score exceeds a threshold, useful for finding cut points.

```sh
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)',showinfo" -f null -
```

### Split frames into two outputs by type

Route I-frames to one output and all other frames to a second output for different processing.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]select='if(eq(pict_type,I),1,2)':outputs=2[iframes][others]" \
  -map "[iframes]" iframes.mp4 \
  -map "[others]" others.mp4
```

### Select every Nth frame

Keep every 10th frame to create a time-lapse effect.

```sh
ffmpeg -i input.mp4 -vf "select='not(mod(n,10))'" -vsync vfr timelapse.mp4
```

## Notes

- When using `select` to extract frames as images, always add `-vsync vfr` (or `-fps_mode vfr`) to prevent FFmpeg from duplicating frames to maintain a constant output rate.
- The `scene` variable requires prior scene detection; use `select=scene` alongside `showinfo` or `metadata` filters to inspect scores before choosing a threshold.
- For simple time-based trimming, `trim` is more efficient than `select` because `trim` avoids evaluating the expression for every frame.
- When routing to multiple outputs with `outputs=N`, a result of `0` drops the frame entirely; results `1` through `N` route to outputs 0 through N-1.
