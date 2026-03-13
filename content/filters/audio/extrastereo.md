+++
title = "extrastereo"
description = "Widen or narrow the stereo image by linearly scaling the difference between left and right channels."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["stereo", "width", "effects"]

[extra]
filter_type = "audio"
since = ""
see_also = ["stereotools", "channelmap"]
parameters = ["m", "c"]
cohort = 2
source_file = "libavfilter/af_extrastereo.c"
+++

The `extrastereo` filter widens or narrows the stereo field by scaling the difference between the left and right channels. A value above 1.0 exaggerates the stereo separation (wider), 1.0 is unchanged, 0.0 collapses to mono, and negative values swap or invert the channels. It is a simple and effective tool for adding perceived "width" or "air" to a stereo mix.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "extrastereo=m=2.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| m | float | `2.5` | Difference coefficient. 0 = mono, 1 = unchanged, >1 = wider, -1 = swap L/R. |
| c | bool | `1` | Enable clipping (prevent signal exceeding ±1.0). |

## Examples

### Wide stereo effect

```sh
ffmpeg -i stereo.mp3 -af "extrastereo=m=3.0" wide.mp3
```

### Mono collapse (m=0)

```sh
ffmpeg -i stereo.mp3 -af "extrastereo=m=0" mono.mp3
```

### Subtle widening

```sh
ffmpeg -i music.mp3 -af "extrastereo=m=1.5" wider.mp3
```

### Swap left and right channels

```sh
ffmpeg -i input.mp3 -af "extrastereo=m=-1" swapped.mp3
```

## Notes

- `m=0.0` averages both channels (mono); `m=1.0` passes audio unchanged; `m=2.5` (default) is a noticeably wider image.
- Very high values (>3.0) can cause clipping and phase issues — use with clipping enabled (`c=1`) to prevent distortion.
- For more control over stereo processing (M/S, balance, delay), use `stereotools` instead.
- This filter supports runtime commands for all options, allowing dynamic stereo width automation.
