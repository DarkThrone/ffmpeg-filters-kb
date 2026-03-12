+++
title = "fade"
description = "Apply a fade-in or fade-out effect to video, transitioning from or to a solid color."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transition", "fade", "timing"]

[extra]
filter_type = "video"
since = ""
see_also = ["overlay", "trim", "setpts"]
parameters = ["type", "start_frame", "nb_frames", "start_time", "duration", "color", "alpha"]
cohort = 1
+++

The `fade` filter applies a gradual transparency transition, fading the video in from a solid color (fade-in) or out to a solid color (fade-out). You can target the effect by frame count or by timestamp, making it straightforward to add polished beginnings and endings to clips. When `alpha=1` is set, only the alpha channel is faded, which is useful for compositing workflows.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type (t) | int | `in` | Fade direction: `in` (black to video) or `out` (video to color). |
| start_frame (s) | int | `0` | Frame number at which the effect begins (frame-based mode). |
| nb_frames (n) | int | `25` | Number of frames over which the fade is applied (frame-based mode). |
| start_time (st) | duration | `0` | Timestamp (seconds) at which the effect begins (time-based mode). |
| duration (d) | duration | `0` | Duration of the fade in seconds (time-based mode). Overrides `nb_frames` when set. |
| color (c) | color | `black` | The solid color to fade to/from (e.g., `black`, `white`, `#FF0000`). |
| alpha | bool | `0` | When `1`, fade only the alpha channel if present, not the RGB values. |

## Examples

### Fade in over the first second

Fade from black to the video starting at t=0 and lasting 1 second.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1" output.mp4
```

### Fade out the last 2 seconds

For a 30-second clip, start the fade-out at 28 seconds and let it run to the end.

```sh
ffmpeg -i input.mp4 -vf "fade=t=out:st=28:d=2" output.mp4
```

### Both fade-in and fade-out in one pass

Chain two `fade` filters to apply a 1-second fade-in at the start and a 1-second fade-out at the end of a 10-second clip.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" output.mp4
```

### Fade in from white

Use `color=white` to create a bright flash intro effect instead of the default black.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=0.5:color=white" output.mp4
```

### Fade alpha channel only (for compositing)

When working in a pipeline that preserves alpha, fade only transparency without changing the underlying colors.

```sh
ffmpeg -i input.mp4 -vf "fade=t=out:st=5:d=1:alpha=1" output.mp4
```

## Notes

- If both `start_time`/`duration` and `start_frame`/`nb_frames` are set for the same fade, the time-based parameters take priority when `duration` is non-zero; otherwise frames are used.
- The fade effect applies to all frames that fall within the specified range; outside this range, the video passes through unchanged.
- When applying both fade-in and fade-out in a single `-vf`, chain them with a comma — the filters are applied in sequence.
- For very precise control at non-standard frame rates, prefer the time-based (`st`/`d`) parameters over the frame-count (`s`/`n`) ones.
