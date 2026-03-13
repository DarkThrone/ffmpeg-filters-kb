+++
title = "bm3d"
description = "Denoise video using Block-Matching 3D filtering for high-quality noise suppression."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["denoise", "quality"]

[extra]
filter_type = "video"
since = ""
see_also = ["nlmeans", "hqdn3d"]
parameters = ["sigma", "block", "bstep", "group", "range", "mstep", "thmse", "hdthr", "estim", "ref", "planes"]
cohort = 2
+++

The `bm3d` filter implements Block-Matching 3D denoising, one of the highest-quality denoising algorithms. It works by finding similar blocks throughout the frame, stacking them into a 3D array, and applying collaborative filtering in the transform domain. It supports a two-pass mode: a fast `basic` estimate followed by a high-quality `final` pass that uses the first estimate as a reference for even better denoising.

## Quick Start

```sh
# Single-pass BM3D
ffmpeg -i noisy.mp4 -vf "bm3d=sigma=5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sigma | float | `1.0` | Denoising strength. Higher = stronger. Typical range: 1–20. |
| block | int | `16` | Local patch (block) size. Must be a power of 2. |
| bstep | int | `4` | Step between processed blocks. Smaller = better quality, slower. |
| group | int | `1` | Maximum number of similar blocks per group. |
| range | int | `9` | Block matching search range. |
| mstep | int | `1` | Step for block matching search. |
| thmse | float | `0.0` | Block matching threshold. 0 = auto. |
| hdthr | float | `2.7` | Hard threshold for 3D transform. |
| estim | int | `basic` | Estimation mode: `basic` or `final`. |
| ref | bool | `0` | If true, expects a reference stream (second input) for final estimation. |
| planes | int | `7` | Bitmask of planes to filter. |

## Examples

### Single-pass with moderate strength

```sh
ffmpeg -i input.mp4 -vf "bm3d=sigma=4" output.mp4
```

### Two-pass BM3D for best quality

**Step 1**: Generate basic estimate and save to a pipe-accessible stream.

```sh
ffmpeg -i noisy.mp4 \
  -filter_complex "[0:v]split[noisy1][noisy2];[noisy1]bm3d=sigma=6:estim=basic[basic];[noisy2][basic]bm3d=sigma=6:estim=final:ref=1[out]" \
  -map "[out]" output.mp4
```

### Light denoising to preserve film grain

```sh
ffmpeg -i film.mp4 -vf "bm3d=sigma=2:block=8" output.mp4
```

## Notes

- Two-pass mode (basic → final) produces significantly better results than single-pass: the `basic` estimate provides a reference that guides the `final` pass to be more accurate.
- `sigma` is the key quality knob: values of 3–6 work well for typical camera noise; 8–15 for strong noise (ISO 3200+ photography).
- `bstep=1` (overlap every pixel) gives best quality at the cost of much higher CPU usage. Default `bstep=4` is a practical compromise.
- BM3D is slower than `hqdn3d` or `atadenoise` but produces less smearing and better preservation of texture.
