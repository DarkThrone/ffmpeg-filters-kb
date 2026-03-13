+++
title = "a3dscope"
description = "Render audio samples as a 3D waveform scope video, displaying amplitude over time in a 3D rotating view."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "scope", "3d", "waveform"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "aphasemeter", "abitscope"]
parameters = ["rate", "size", "fov", "roll", "pitch", "yaw", "xzoom", "yzoom", "zzoom", "xpos", "ypos", "zpos", "length"]
cohort = 3
+++

The `a3dscope` filter converts audio into a 3D waveform visualization rendered as a video stream. The audio waveform is displayed in three dimensions with configurable camera angles, field of view, and zoom. The result is an animated 3D scope view that rotates through samples over time — primarily used for artistic audio visualizations.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,a3dscope"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `800x600` | Output video size. |
| fov | float | `90.0` | Field of view (degrees). |
| roll | float | `0.0` | Camera roll angle (degrees). |
| pitch | float | `0.0` | Camera pitch angle (degrees). |
| yaw | float | `0.0` | Camera yaw angle (degrees). |
| xzoom | float | `1.0` | Zoom on X axis. |
| yzoom | float | `1.0` | Zoom on Y axis. |
| zzoom | float | `1.0` | Zoom on Z axis. |
| xpos | float | `0.0` | X position offset. |
| ypos | float | `0.0` | Y position offset. |
| zpos | float | `0.0` | Z position offset. |
| length | int | `15` | Number of audio segments to render. |

## Examples

### Basic 3D scope

```sh
ffplay -f lavfi "amovie=music.mp3,a3dscope=size=800x600"
```

### Angled view

```sh
ffplay -f lavfi "amovie=music.mp3,a3dscope=pitch=30:yaw=45"
```

### Save 3D scope video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]a3dscope=size=1280x720[v]" \
  -map "[v]" scope3d.mp4
```

## Notes

- `a3dscope` is primarily artistic — for technical audio analysis, use `showwaves`, `showfreqs`, or `aphasemeter`.
- Adjust `fov` (default 90°) to widen or narrow the perspective; higher values give a more dramatic effect.
- `length` controls how many past audio segments are visible — higher values show more history.
