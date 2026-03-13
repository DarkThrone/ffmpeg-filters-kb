+++
title = "lut"
description = "Apply a per-pixel lookup table transformation using mathematical expressions per channel."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "lut", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["lut3d", "haldclut", "geq"]
parameters = ["c0", "c1", "c2", "c3", "y", "u", "v", "r", "g", "b", "a"]
cohort = 2
source_file = "libavfilter/vf_lut.c"
+++

The `lut` filter applies a mathematical expression to every pixel of each channel independently, computed once and stored in a lookup table (LUT) for fast evaluation. It supports both YCbCr (`y`, `u`, `v`) and RGB (`r`, `g`, `b`, `a`) addressing, making it suitable for channel inversions, gamma corrections, clamping, and simple color grading effects.

## Quick Start

```sh
# Boost luminance by 20%
ffmpeg -i input.mp4 -vf "lut=y='val*1.2'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| c0 | string | Expression for component 0 (Y or R depending on pixel format). |
| c1 | string | Expression for component 1 (Cb/U or G). |
| c2 | string | Expression for component 2 (Cr/V or B). |
| c3 | string | Expression for component 3 (alpha). |
| y | string | Luminance (Y) expression — alias for c0 on YUV input. |
| u | string | Cb/U expression — alias for c1. |
| v | string | Cr/V expression — alias for c2. |
| r | string | Red expression — alias for c0 on RGB input. |
| g | string | Green expression — alias for c1. |
| b | string | Blue expression — alias for c2. |
| a | string | Alpha expression — alias for c3. |

### Expression variables

Within each expression, the following variables are available:

| Variable | Description |
|----------|-------------|
| `val` | Current input pixel value. |
| `maxval` | Maximum value for the component's bit depth (e.g. 255 for 8-bit). |
| `minval` | Minimum value (typically 0). |
| `negval` | `maxval - val` (inverted value). |
| `clipval` | `val` clamped to `[minval, maxval]`. |
| `w` / `h` | Video width / height. |
| `n` | Frame number (0-based). |
| `t` | Timestamp in seconds. |

## Examples

### Invert the luma channel (negative)

```sh
ffmpeg -i input.mp4 -vf "lut=y='negval'" output.mp4
```

### Increase luminance with clipping

```sh
ffmpeg -i input.mp4 -vf "lut=y='min(val*1.3, maxval)'" output.mp4
```

### Desaturate by zeroing chroma

```sh
ffmpeg -i input.mp4 -vf "lut=u='128':v='128'" output.mp4
```

### Increase red and reduce blue (RGB input)

Requires the input to be in RGB format (use `format=rgb24` first).

```sh
ffmpeg -i input.mp4 -vf "format=rgb24,lut=r='min(val*1.2, maxval)':b='val*0.8'" output.mp4
```

## Notes

- `lut` works on individual channels; for 3D color interactions (where R affects G output, etc.), use `lut3d` or `colorchannelmixer`.
- The expression is evaluated once per unique input value at filter initialisation, not per pixel, so it is very fast even on high-resolution video.
- For YUV inputs, chroma values range from 0–255 with neutral at 128. Setting `u` or `v` to `'128'` removes all chroma (desaturates).
- `lutyuv` is an alias for `lut` on YUV inputs; `lutrgb` is an alias for RGB inputs — both are equivalent to `lut`.
