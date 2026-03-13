+++
title = "minterpolate"
description = "Convert video to a higher or lower frame rate using motion-compensated interpolation to synthesize intermediate frames."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["frame-rate", "motion", "interpolation"]

[extra]
filter_type = "video"
since = ""
see_also = ["framerate", "mpdecimate", "yadif"]
parameters = ["fps", "mi_mode", "mc_mode", "me_mode", "me", "mb_size", "search_param", "scd"]
cohort = 2
source_file = "libavfilter/vf_minterpolate.c"
+++

The `minterpolate` filter converts video to a target frame rate by synthesizing intermediate frames using motion estimation and compensation — the "motion smoothing" effect seen on modern TVs (sometimes called the "soap opera effect"). It supports multiple motion estimation algorithms and can degrade gracefully at scene changes by detecting them automatically.

## Quick Start

```sh
# Convert 24fps to 60fps with motion interpolation
ffmpeg -i input.mp4 -vf "minterpolate=fps=60" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | video_rate | `60` | Target output frame rate. Frames are dropped if fps < source fps. |
| mi_mode | int | `mci` | Motion interpolation mode: `dup` (duplicate), `blend` (blend frames), `mci` (motion-compensated). |
| mc_mode | int | `obmc` | Motion compensation mode: `obmc` (overlapped block) or `aobmc` (adaptive). Requires `mci`. |
| me_mode | int | `bilat` | Motion estimation mode: `bidir` (bidirectional) or `bilat` (bilateral). |
| me | int | `epzs` | ME algorithm: `esa`, `tss`, `tdls`, `ntss`, `fss`, `ds`, `hexbs`, `epzs`, `umh`. |
| mb_size | int | `16` | Macroblock size in pixels. |
| search_param | int | `32` | Search parameter for motion estimation. |
| vsbmc | int | `0` | Enable variable-size block motion compensation at object boundaries. |
| scd | int | `fdiff` | Scene change detection: `none` or `fdiff` (frame difference). |
| scd_threshold | double | `10.0` | Scene change detection threshold. |

## Examples

### Convert 24fps film to 60fps (smooth motion)

```sh
ffmpeg -i film_24fps.mp4 -vf "minterpolate=fps=60:mi_mode=mci" output.mp4
```

### Simple frame blending (less artifacts, less smoothness)

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=blend" output.mp4
```

### Slow motion: 120fps target from 30fps source

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc" slow.mp4
```

### Disable scene change detection

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:scd=none" output.mp4
```

## Notes

- `mci` (motion-compensated) mode produces the smoothest results but is computationally expensive.
- `blend` mode is fast and artifact-free but only produces a smooth crossfade between frames, not true motion interpolation.
- Scene change detection (`scd`) prevents motion vectors from crossing cuts — disable if you experience false positives with `scd=none`.
- For broadcast standards conversion (e.g. 23.976→25fps), the simpler `framerate` filter is usually preferred as it produces fewer artifacts.
- Very fast motion (action scenes, sports) will produce ghosting/warping artifacts with any interpolation method.
