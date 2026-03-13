+++
title = "atadenoise"
description = "Adaptive Temporal Averaging Denoiser that reduces video noise by averaging across multiple frames using adaptive thresholds."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["denoise", "temporal", "noise-reduction"]

[extra]
filter_type = "video"
since = ""
see_also = ["hqdn3d", "nlmeans", "bm3d"]
parameters = ["0a", "0b", "1a", "1b", "2a", "2b", "s", "p", "a"]
cohort = 2
+++

The `atadenoise` filter reduces noise by averaging pixel values across multiple frames, adapting to scene content to avoid blurring in-motion areas. Per-plane thresholds (`a` and `b`) control sensitivity: threshold A reacts to abrupt changes (scene cuts, fast motion), while threshold B handles slow continuous changes (grain, sensor noise).

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "atadenoise" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| 0a | float | `0.02` | Threshold A for 1st plane (abrupt change sensitivity). Range: 0–0.3. |
| 0b | float | `0.04` | Threshold B for 1st plane (continuous change sensitivity). Range: 0–5. |
| 1a | float | `0.02` | Threshold A for 2nd plane. |
| 1b | float | `0.04` | Threshold B for 2nd plane. |
| 2a | float | `0.02` | Threshold A for 3rd plane. |
| 2b | float | `0.04` | Threshold B for 3rd plane. |
| s | int | `9` | Number of frames to average (must be odd, range 5–129). |
| p | flags | all | Planes to filter. |
| a | int | `parallel` | Algorithm variant: `parallel` or `serial`. |
| 0s / 1s / 2s | float | `32767` | Per-plane spatial sigma (pixel weight). 0 disables filtering. |

## Examples

### Mild denoising (default parameters)

```sh
ffmpeg -i grainy.mp4 -vf "atadenoise" output.mp4
```

### Stronger temporal denoising over 15 frames

```sh
ffmpeg -i film_grain.mp4 -vf "atadenoise=s=15:0a=0.05:0b=0.08" output.mp4
```

### Denoise only luma plane

```sh
ffmpeg -i input.mp4 -vf "atadenoise=p=1" output.mp4
```

### Higher thresholds for very noisy footage

```sh
ffmpeg -i vhs.mp4 -vf "atadenoise=0a=0.1:0b=0.2:1a=0.05:1b=0.1:s=9" output.mp4
```

## Notes

- Larger `s` (more frames) gives stronger denoising but requires more memory and can cause ghosting in fast-motion scenes.
- Threshold A controls sensitivity to sudden changes (fast motion, cuts) — keep it low to avoid motion blur artifacts.
- Threshold B controls sensitivity to slow drift (sensor noise, flicker) — increase it to remove more continuous noise.
- `parallel` mode is generally faster than `serial`, but `serial` can produce slightly better results by evaluating both sides of the frame window.
