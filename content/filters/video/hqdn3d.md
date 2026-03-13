+++
title = "hqdn3d"
description = "Apply a High Quality 3D Denoiser combining spatial and temporal filtering."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["denoise", "noise-reduction"]

[extra]
filter_type = "video"
since = ""
see_also = ["nlmeans", "atadenoise"]
parameters = ["luma_spatial", "chroma_spatial", "luma_tmp", "chroma_tmp"]
cohort = 2
source_file = "libavfilter/vf_hqdn3d.c"
+++

The `hqdn3d` filter applies a 3D denoiser that combines spatial (within-frame) and temporal (across-frame) lowpass filtering. It is one of the fastest high-quality denoisers in FFmpeg, making it suitable for real-time or near-real-time workflows. The spatial component blurs within each frame; the temporal component averages across consecutive frames to suppress flickering noise.

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "hqdn3d=4:3:6:4.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_spatial | double | `4.0` | Spatial luma denoising strength. Higher = more smoothing. |
| chroma_spatial | double | `3.0` | Spatial chroma denoising strength. |
| luma_tmp | double | `6.0` | Temporal luma strength. Higher = stronger frame-to-frame averaging. |
| chroma_tmp | double | `4.5` | Temporal chroma strength. |

## Examples

### Moderate denoising (default values)

```sh
ffmpeg -i noisy.mp4 -vf "hqdn3d" output.mp4
```

### Aggressive denoising

```sh
ffmpeg -i very_noisy.mp4 -vf "hqdn3d=8:6:12:9" output.mp4
```

### Temporal only (no spatial blur)

Reduce temporal flickering without blurring spatial detail.

```sh
ffmpeg -i input.mp4 -vf "hqdn3d=0:0:6:4" output.mp4
```

### Chroma-only denoising

Denoise only colour channels, leave luma sharp.

```sh
ffmpeg -i input.mp4 -vf "hqdn3d=0:3:0:4" output.mp4
```

## Notes

- The four parameters are positional: `luma_spatial:chroma_spatial:luma_tmp:chroma_tmp`. If only the first is given, it sets `luma_spatial`; if the second is omitted, it defaults to `luma_spatial * 2/3`.
- Temporal strength (`luma_tmp`) often matters more than spatial — start by increasing `luma_tmp` before `luma_spatial`.
- `hqdn3d` is much faster than `nlmeans` but produces more detail loss at high strengths. It is excellent for pre-processing before encoding to improve compression efficiency.
- High values on fast-moving content can cause ghost/smear artifacts in the temporal dimension; reduce `luma_tmp` in those cases.
