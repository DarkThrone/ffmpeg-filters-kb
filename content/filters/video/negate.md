+++
title = "negate"
description = "Invert the colors of a video by negating each pixel's component values."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "invert"]

[extra]
filter_type = "video"
since = ""
see_also = ["lut", "colorbalance"]
parameters = ["components"]
cohort = 2
source_file = "libavfilter/vf_negate.c"
+++

The `negate` filter inverts the color of each pixel by subtracting each component value from the maximum value (`maxval - val`). Applied to all channels it produces a photographic negative. Individual channels can be selectively negated using the `components` parameter, enabling effects like luma inversion while preserving hue.

## Quick Start

```sh
# Full colour inversion (photographic negative)
ffmpeg -i input.mp4 -vf "negate" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| components | flags | `7` | Bitmask of components to negate: 1=Y/R, 2=Cb/U/G, 4=Cr/V/B, 8=Alpha. Default 7 negates Y, Cb, Cr (all chroma, full inversion). |

## Examples

### Full colour inversion

```sh
ffmpeg -i input.mp4 -vf "negate" output.mp4
```

### Invert only luminance (solarize-like effect)

Negate only the Y channel to produce a light-on-dark effect with original hues.

```sh
ffmpeg -i input.mp4 -vf "negate=components=1" output.mp4
```

### Invert luma and alpha (for overlay effects)

```sh
ffmpeg -i input.mp4 -vf "negate=components=9" output.mp4
```

## Notes

- With no arguments, `negate` inverts all three colour planes (Y, Cb, Cr for YUV or R, G, B for RGB), producing a traditional photographic negative.
- The `components` bitmask uses: 1=first plane (Y/R), 2=second plane (Cb/U/G), 4=third plane (Cr/V/B), 8=alpha. Sum the values to combine, e.g. `components=5` negates Y and Cr.
- Negation is equivalent to `lut=y='negval'` but faster and more readable.
- On YUV input, negating only chroma (components=6) produces a complementary colour-shifted image with unchanged brightness.
