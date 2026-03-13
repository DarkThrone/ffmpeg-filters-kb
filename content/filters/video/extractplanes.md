+++
title = "extractplanes"
description = "Extract individual color plane components (Y, U, V, R, G, B, A) from a video stream as separate grayscale output streams."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["planes", "channel", "utility"]

[extra]
filter_type = "video"
since = ""
see_also = ["mergeplanes", "split", "alphaextract"]
parameters = ["planes"]
cohort = 2
+++

The `extractplanes` filter splits a multi-component video stream into separate single-plane grayscale streams — one per color component. This is useful for processing individual planes independently (e.g. applying different filters to Y and UV planes), analyzing specific channels, or as part of a processing pipeline where planes are later recombined with `mergeplanes`. It is a multiple-output filter and requires `-filter_complex`.

## Quick Start

```sh
# Extract Y, U, V planes into 3 separate files
ffmpeg -i input.mp4 -filter_complex 'extractplanes=y+u+v[y][u][v]' \
  -map '[y]' y.mp4 -map '[u]' u.mp4 -map '[v]' v.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| planes | flags | — | Planes to extract, combined with `+`: `y`, `u`, `v`, `a`, `r`, `g`, `b`. |

## Examples

### Extract all YUV planes

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'extractplanes=y+u+v[y][u][v]' \
  -map '[y]' luma.avi \
  -map '[u]' cb.avi \
  -map '[v]' cr.avi
```

### Extract luma only for analysis

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'extractplanes=y[y]' \
  -map '[y]' luma_only.mp4
```

### Extract RGB planes from an RGB source

```sh
ffmpeg -i input.png \
  -filter_complex 'extractplanes=r+g+b[r][g][b]' \
  -map '[r]' red.png \
  -map '[g]' green.png \
  -map '[b]' blue.png
```

### Extract alpha channel

```sh
ffmpeg -i input_with_alpha.mov \
  -filter_complex 'extractplanes=a[a]' \
  -map '[a]' alpha_mask.mp4
```

## Notes

- You cannot mix YUV and RGB planes in the same `extractplanes` call — they come from different pixel formats.
- The filter outputs one stream per plane, in the order they appear in the `planes` option.
- Use `mergeplanes` to recombine processed planes back into a single stream.
- `extractplanes=y` is roughly equivalent to `format=gray` but without any colorspace conversion.
