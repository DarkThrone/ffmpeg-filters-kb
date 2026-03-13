+++
title = "tpad"
description = "Add padding frames at the start or end of a video stream — either solid-color frames or clones of the first/last frame."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["padding", "timing", "utility"]

[extra]
filter_type = "video"
since = ""
see_also = ["apad", "concat", "tile"]
parameters = ["start", "stop", "start_mode", "stop_mode", "start_duration", "stop_duration", "color"]
cohort = 2
source_file = "libavfilter/vf_tpad.c"
+++

The `tpad` filter adds temporal padding to a video stream — inserting extra frames at the beginning (to delay the start) or at the end (to extend it). It can add solid-color frames or clone the first/last frame, and supports both frame counts and duration-based specifications. This is useful for synchronizing streams, creating freeze frames, or adding holds before/after the content.

## Quick Start

```sh
# Add 30 black frames before the video
ffmpeg -i input.mp4 -vf "tpad=start=30" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | int | `0` | Number of frames to prepend. |
| stop | int | `0` | Number of frames to append (-1 = pad indefinitely). |
| start_mode | int | `add` | Mode for prepended frames: `add` (solid color) or `clone` (repeat first frame). |
| stop_mode | int | `add` | Mode for appended frames: `add` (solid color) or `clone` (repeat last frame). |
| start_duration | duration | `0` | Duration to prepend (overrides `start`). E.g. `1.5` or `00:00:01.500`. |
| stop_duration | duration | `0` | Duration to append (overrides `stop`). |
| color | color | `black` | Color for `add`-mode frames. |

## Examples

### Add 1 second of black before video

```sh
ffmpeg -i input.mp4 -vf "tpad=start_duration=1:color=black" output.mp4
```

### Freeze-frame hold: clone first frame for 2 seconds

```sh
ffmpeg -i input.mp4 -vf "tpad=start=48:start_mode=clone" output.mp4
```

### Hold last frame for 3 seconds at end

```sh
ffmpeg -i input.mp4 -vf "tpad=stop_duration=3:stop_mode=clone" output.mp4
```

### Pad both ends with white

```sh
ffmpeg -i input.mp4 -vf "tpad=start_duration=0.5:stop_duration=0.5:color=white" output.mp4
```

### Pad audio stream to match video length

```sh
ffmpeg -i input.mp4 -vf "tpad=stop=-1:stop_mode=clone" -af "apad" output.mp4
```

## Notes

- `stop=-1` pads indefinitely — useful when you need to synchronize video length with a longer audio track; always pair with a time limit (e.g. `-t` or `-to`).
- `clone` mode repeats the actual first/last frame content, creating a freeze-frame effect. `add` mode inserts a solid-color frame.
- `start_duration` and `stop_duration` override `start`/`stop` when non-zero, and accept FFmpeg's standard time duration syntax.
- For audio padding use the `apad` audio filter in the same pipeline.
