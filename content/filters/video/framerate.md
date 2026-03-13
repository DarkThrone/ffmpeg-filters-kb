+++
title = "framerate"
description = "Change video frame rate by interpolating new frames from adjacent source frames, designed for progressive content."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["frame-rate", "interpolation", "conversion"]

[extra]
filter_type = "video"
since = ""
see_also = ["minterpolate", "fps", "mpdecimate"]
parameters = ["fps", "interp_start", "interp_end", "scene", "flags"]
cohort = 2
source_file = "libavfilter/vf_framerate.c"
+++

The `framerate` filter converts progressive video to a different frame rate by blending adjacent frames with configurable linear interpolation weights. Unlike `minterpolate`, it does not perform motion estimation — it simply cross-fades between frames, making it faster and more predictable. It detects scene changes to avoid blending across cuts. Designed exclusively for progressive content — deinterlace first if needed.

## Quick Start

```sh
# Convert 23.976fps to 25fps
ffmpeg -i film_24fps.mp4 -vf "framerate=fps=25" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | video_rate | `50` | Target output frame rate (e.g. `25`, `30000/1001`, `60`). |
| interp_start | int | `15` | Start of the blend range (0–255). Below this: copy source frame. |
| interp_end | int | `240` | End of the blend range. Above this: copy source frame. |
| scene | double | `8.2` | Scene change sensitivity (0–100). Higher = more scene changes detected. |
| flags | flags | `scd` | Flags: `scene_change_detect` / `scd` to enable scene change detection. |

## Examples

### 23.976fps to 25fps (PAL broadcast standard)

```sh
ffmpeg -i ntsc_film.mp4 -vf "framerate=fps=25" pal.mp4
```

### 25fps to 29.97fps (PAL to NTSC)

```sh
ffmpeg -i pal.mp4 -vf "framerate=fps=30000/1001" ntsc.mp4
```

### 60fps output without scene change detection

```sh
ffmpeg -i input.mp4 -vf "framerate=fps=60:flags=0" output.mp4
```

### Custom interpolation range

```sh
ffmpeg -i input.mp4 -vf "framerate=fps=50:interp_start=40:interp_end=200" output.mp4
```

## Notes

- `framerate` uses frame blending (cross-fade), not motion compensation. It is fast and artifact-free but can produce ghosting on fast motion.
- For more visually convincing interpolation at large fps multipliers (e.g. 24→60fps), use `minterpolate` instead.
- `framerate` is not designed for interlaced content — always deinterlace with `yadif` or `bwdif` first.
- Scene change detection (`scd` flag, enabled by default) prevents blending across hard cuts; disable it only if you experience false positives.
- `interp_start` and `interp_end` define a 0–255 range of blend amounts; frames at the boundaries of the conversion window get full copies of source frames.
