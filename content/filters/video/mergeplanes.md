+++
title = "mergeplanes"
description = "Merge individual color plane streams from multiple inputs into a single multi-component video stream."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["planes", "channel", "utility"]

[extra]
filter_type = "video"
since = ""
see_also = ["extractplanes", "split"]
parameters = ["mapping", "format", "map0s", "map0p", "map1s", "map1p", "map2s", "map2p", "map3s", "map3p"]
cohort = 2
source_file = "libavfilter/vf_mergeplanes.c"
+++

The `mergeplanes` filter combines individual plane streams from up to 4 input streams into a single output pixel format. The `mapping` parameter is a hexadecimal bitmap specifying which input stream and plane feeds each output plane. It is the counterpart to `extractplanes`, and together they enable processing individual color components with arbitrary filter chains.

## Quick Start

```sh
# Merge 3 gray streams into yuv444p
ffmpeg -i y.mp4 -i u.mp4 -i v.mp4 \
  -filter_complex '[0][1][2]mergeplanes=0x001020:yuv444p' output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mapping | int | `0` | Hex bitmap: `0xAaBbCcDd`. Each byte: high nibble = input stream (0–3), low nibble = source plane (0–3). |
| format | pixel_fmt | `yuva444p` | Output pixel format. |
| map0s / map0p | int | `0` | Stream/plane mapping for output plane 0 (alternative to `mapping`). |
| map1s / map1p | int | `0` | Stream/plane mapping for output plane 1. |
| map2s / map2p | int | `0` | Stream/plane mapping for output plane 2. |
| map3s / map3p | int | `0` | Stream/plane mapping for output plane 3. |

## Examples

### Merge 3 gray streams into YUV444

```sh
ffmpeg -i y.mp4 -i u.mp4 -i v.mp4 \
  -filter_complex '[0][1][2]mergeplanes=0x001020:yuv444p' out.mp4
```

### Swap U and V planes in yuv420p

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'format=yuv420p,mergeplanes=0x000201:yuv420p' swapped.mp4
```

### Swap Y and Alpha in yuva444p

```sh
ffmpeg -i input.mov \
  -filter_complex 'format=yuva444p,mergeplanes=0x03010200:yuva444p' output.mov
```

### Cast RGB24 to YUV444 (plane reinterpretation, no color conversion)

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'format=rgb24,mergeplanes=0x000102:yuv444p' output.mp4
```

### Merge Y from stream 0, U/V from stream 1

```sh
ffmpeg -i sharpened_luma.mp4 -i original.mp4 \
  -filter_complex '[0][1]mergeplanes=0x001011:yuv444p' out.mp4
```

## Notes

- The `mapping` hex value encodes all plane sources at once: `0xAaBbCcDd` where `A`=stream for output plane 0, `a`=plane from that stream, etc.
- The alternative `map0s`/`map0p` … `map3s`/`map3p` parameters are easier to read for complex mappings.
- Inputs must all be the same width and height; pixel formats need not match.
- `mergeplanes` is commonly used after `extractplanes` to recombine independently processed planes.
