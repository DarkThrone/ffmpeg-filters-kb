+++
title = "fps"
description = "Force a constant output frame rate by duplicating or dropping frames as needed."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["timing", "fps", "framerate"]

[extra]
filter_type = "video"
since = ""
see_also = ["setpts", "trim", "format"]
parameters = ["fps", "start_time", "round", "eof_action"]
cohort = 1
+++

The `fps` filter converts variable or mismatched frame rates to a specified constant frame rate. It achieves this by duplicating frames when the source rate is too low, and dropping frames when it is too high. This is commonly needed before encoding to a container that requires a fixed frame rate, or when you need to normalize frame rates before stacking or concatenating streams. The filter supports named rate constants such as `ntsc`, `pal`, and `film`.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "fps=fps=30" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | string | `25` | Desired output frame rate. Accepts a number, fraction (`30000/1001`), or named constant (`ntsc`, `pal`, `film`, `ntsc_film`). |
| start_time | double | (auto) | Assumed PTS of the first output frame in seconds. Useful for padding or trimming the stream start. |
| round | int | `near` | Timestamp rounding method: `zero`, `inf`, `down`, `up`, `near`. |
| eof_action | int | `round` | Behavior at end of input: `round` (apply normal rounding) or `pass` (pass last frame if duration not reached). |

### Named rate constants

| Constant | Value |
|----------|-------|
| `ntsc` | 30000/1001 (~29.97 fps) |
| `pal` | 25.0 fps |
| `film` | 24.0 fps |
| `ntsc_film` | 24000/1001 (~23.976 fps) |

## Examples

### Convert to 30 fps

Normalize any input to exactly 30 frames per second.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=30" output.mp4
```

### Convert to standard NTSC rate

Use the named constant for broadcast-safe NTSC frame rate.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=ntsc" output.mp4
```

### Convert to 24 fps film rate

Target a cinematic 24 fps output.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=film" output.mp4
```

### Pad stream start to time zero

Set `start_time=0` so that if the video stream begins after time zero, it is padded with duplicate frames from the first frame.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=25:start_time=0" output.mp4
```

### Combine with setpts for slow motion

Double the frame rate together with stretched PTS to produce a smoother slow-motion effect via frame duplication.

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS,fps=fps=60" output.mp4
```

## Notes

- `fps` produces a constant frame rate by duplicating or dropping frames; it does not interpolate new frames. For true slow-motion with new frames, use the `minterpolate` filter.
- When combining `fps` with `setpts`, apply `setpts` first to stretch/compress time, then `fps` to normalize the rate.
- The filter works on PTS values; if the input has no reliable PTS, results may be unpredictable. Pair with `setpts=PTS-STARTPTS` to reset timestamps beforehand.
- Container-level frame rate (`-r`) and the `fps` filter are different mechanisms; using the filter gives more control in complex filtergraphs.
