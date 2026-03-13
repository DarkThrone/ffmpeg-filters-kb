+++
title = "hflip"
description = "Horizontally flip (mirror) each frame of the input video."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "flip"]

[extra]
filter_type = "video"
since = ""
see_also = ["vflip", "transpose", "rotate"]
parameters = []
cohort = 1
source_file = "libavfilter/vf_hflip.c"
+++

The `hflip` filter mirrors every frame of the input video along the vertical axis, producing a left-right reflection. It has no parameters and operates in-place without any quality loss. Common use cases include correcting footage shot with a mirror lens rig, fixing front-camera video captured on mobile devices, or creating stylistic mirror effects.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "hflip" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Basic horizontal flip

Mirror the video horizontally and re-encode with default settings.

```sh
ffmpeg -i input.mp4 -vf "hflip" output.mp4
```

### Flip and preserve audio

When only the video needs flipping, mux with the original audio stream without re-encoding it.

```sh
ffmpeg -i input.mp4 -vf "hflip" -c:a copy output.mp4
```

### Combine with vertical flip for 180-degree rotation

Apply both horizontal and vertical flips in a single pass to achieve a 180-degree rotation equivalent.

```sh
ffmpeg -i input.mp4 -vf "hflip,vflip" output.mp4
```

### Mirror comparison side-by-side

Use `hflip` in a filtergraph to show the original and its mirror image next to each other.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[a][b]; [b]hflip[bf]; [a][bf]hstack" \
  output.mp4
```

## Notes

- `hflip` performs a purely spatial transformation with no resampling, so there is no quality degradation from the flip itself.
- The filter does not alter timestamps, audio, or any metadata.
- To rotate 90 or 270 degrees, use `transpose` instead; for an arbitrary angle, use `rotate`.
- When combined with `vflip`, the result is equivalent to a 180-degree rotation.
