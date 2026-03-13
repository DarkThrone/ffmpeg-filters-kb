+++
title = "loop"
description = "Loop a segment of video frames a specified number of times or infinitely."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "loop", "timing"]

[extra]
filter_type = "utility"
since = ""
see_also = ["aloop", "reverse", "setpts"]
parameters = ["loop", "size", "start", "time"]
cohort = 3
source_file = "libavfilter/f_loop.c"
+++

The `loop` filter repeats a segment of video frames N times. By buffering a specified number of frames and replaying them, it can create a seamless loop from any segment of a video. This is useful for creating looping backgrounds, extending short clips, or generating infinite loops for displays.

## Quick Start

```sh
# Loop the first 30 frames 5 times
ffmpeg -i input.mp4 -vf "loop=loop=5:size=30:start=0" looped.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| loop | int | `0` | Number of loop iterations. `0` = no looping; `-1` = infinite. |
| size | int64 | `0` | Maximum number of frames to buffer for the loop segment. |
| start | int64 | `0` | Frame number where the loop segment starts. |
| time | duration | — | Loop start time in seconds (used instead of `start` when `start=-1`). |

## Examples

### Loop first 30 frames 5 times

```sh
ffmpeg -i short_clip.mp4 -vf "loop=loop=5:size=30:start=0" extended.mp4
```

### Infinite loop of first frame (static image from video)

```sh
ffmpeg -i input.mp4 -vf "loop=loop=-1:size=1:start=0" -t 30 static.mp4
```

### Loop a specific 60-frame segment starting at frame 100

```sh
ffmpeg -i input.mp4 -vf "loop=loop=3:size=60:start=100" looped.mp4
```

### Loop from a time offset

```sh
ffmpeg -i input.mp4 -vf "loop=loop=10:size=25:start=-1:time=5.0" output.mp4
```

## Notes

- `size` sets the buffer size — it must be at least as large as the segment you want to loop.
- Memory usage scales with `size` × frame dimensions × pixel format.
- For audio looping, use `aloop` with the same `loop`/`size`/`start` logic applied to samples.
- Combine with `trim` to extract exactly the segment you want to loop first.
