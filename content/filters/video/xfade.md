+++
title = "xfade"
description = "Apply a cross-fade transition effect between two video streams."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transition", "compositing", "fade"]

[extra]
filter_type = "video"
since = ""
see_also = ["fade", "blend"]
parameters = ["transition", "duration", "offset", "expr"]
cohort = 2
+++

The `xfade` filter creates smooth transition effects between two video streams. It takes two inputs and blends them using one of many built-in transition types (wipes, fades, slides, etc.) or a custom expression. The `offset` parameter controls when the transition starts relative to the first input, and `duration` controls how long it lasts.

## Quick Start

```sh
# Simple crossfade between two clips
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4" \
  output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transition | int | `fade` | Transition type. See the list below. |
| duration | duration | `1s` | Duration of the transition in seconds. |
| offset | duration | `0s` | Time offset (from the start of the first input) when the transition begins. |
| expr | string | — | Custom transition expression. Used when `transition=custom`. Variables: `X`, `Y`, `W`, `H`, `A`, `B`, `P` (progress 0–1). |

### Available transition types

`fade`, `fadeblack`, `fadewhite`, `fadegrays`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `wipetl`, `wipetr`, `wipebl`, `wipebr`, `slideleft`, `slideright`, `slideup`, `slidedown`, `smoothleft`, `smoothright`, `smoothup`, `smoothdown`, `circlecrop`, `rectcrop`, `circleopen`, `circleclose`, `vertopen`, `vertclose`, `horzopen`, `horzclose`, `dissolve`, `pixelize`, `diagtl`, `diagtr`, `diagbl`, `diagbr`, `hlslice`, `hrslice`, `vuslice`, `vdslice`, `hblur`, `radial`, `squeezeh`, `squeezev`, `zoomin`, `distance`, `fadefast`, `fadeslow`

## Examples

### Crossfade at 4-second mark of a 5-second clip

The transition starts 4 s into clip1, lasts 1 s.

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4" \
  output.mp4
```

### Wipe left transition

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=wipeleft:duration=0.5:offset=3" \
  output.mp4
```

### Chain multiple transitions between three clips

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v]xfade=fade:1:4[ab];[ab][2:v]xfade=wipeleft:1:8[out]" \
  -map "[out]" output.mp4
```

### Custom transition expression (horizontal wipe with easing)

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=custom:duration=1:offset=3:expr='if(gt(X/W,P),A,B)'" \
  output.mp4
```

## Notes

- `offset` is the timestamp in the first stream when the transition begins. Set it to `(duration_of_clip1 - transition_duration)` for the transition to finish exactly when clip1 ends.
- Both input streams must have the same frame size and pixel format. Use `scale` and `format` if needed.
- When chaining multiple clips with transitions, each `xfade` node in the `filter_complex` needs its own `offset` — account for the reduced duration due to previous transitions.
- The `expr` custom transition uses `P` (progress 0→1), `A` (first input pixel), `B` (second input pixel), `X`/`Y` (pixel coordinates), `W`/`H` (dimensions).
