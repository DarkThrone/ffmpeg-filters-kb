+++
title = "vflip"
description = "Vertically flip (mirror) each frame of the input video."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "flip"]

[extra]
filter_type = "video"
since = ""
see_also = ["hflip", "transpose", "rotate"]
parameters = []
cohort = 1
source_file = "libavfilter/vf_vflip.c"
+++

The `vflip` filter mirrors every frame of the input video along the horizontal axis, producing an upside-down reflection. It has no parameters and is lossless. Common use cases include correcting footage shot with an upside-down camera mount, creating reflection effects, or compositing where a flipped stream is required.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Basic vertical flip

Flip the video upside down and re-encode.

```sh
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

### Flip with audio copy

Flip the video while passing the audio through without re-encoding.

```sh
ffmpeg -i input.mp4 -vf "vflip" -c:a copy output.mp4
```

### Create a ground reflection effect

Stack the original video on top of a vertically-flipped copy to simulate a reflection.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[top][bot]; [bot]vflip[flipped]; [top][flipped]vstack" \
  output.mp4
```

### Combine with hflip for 180-degree rotation

Applying both `vflip` and `hflip` is equivalent to a 180-degree rotation.

```sh
ffmpeg -i input.mp4 -vf "vflip,hflip" output.mp4
```

## Notes

- `vflip` is a spatial-only transformation with no resampling, so there is no quality loss from the operation itself.
- Timestamps, audio, and metadata are not modified by this filter.
- For 90-degree rotations use `transpose`; for arbitrary angles use `rotate`.
- When chained with `hflip`, the order does not matter — both combinations produce an identical 180-degree result.
