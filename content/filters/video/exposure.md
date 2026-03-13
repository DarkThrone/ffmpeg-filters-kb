+++
title = "exposure"
description = "Adjust the exposure and black level of video in EV stops."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "exposure", "brightness"]

[extra]
filter_type = "video"
since = ""
see_also = ["eq", "curves"]
parameters = ["exposure", "black"]
cohort = 2
+++

The `exposure` filter adjusts the overall brightness of video using an exposure compensation value expressed in EV (exposure value) stops, similar to the exposure slider in photo editing applications. Positive values brighten; negative values darken. The `black` parameter independently lifts or lowers the black point.

## Quick Start

```sh
# Increase exposure by 1 stop
ffmpeg -i input.mp4 -vf "exposure=exposure=1.0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exposure | float | `0.0` | Exposure correction in EV stops. Range: -3.0–3.0. Each stop doubles/halves the brightness. |
| black | float | `0.0` | Black level correction. Range: -1.0–1.0. Positive lifts shadows, negative crushes blacks. |

## Examples

### Recover underexposed footage (+1 stop)

```sh
ffmpeg -i dark.mp4 -vf "exposure=exposure=1.0" output.mp4
```

### Slightly darken overexposed video

```sh
ffmpeg -i bright.mp4 -vf "exposure=exposure=-0.5" output.mp4
```

### Lift blacks for a fade/matte effect

```sh
ffmpeg -i input.mp4 -vf "exposure=black=0.05" output.mp4
```

### Combine exposure correction with black point lift

```sh
ffmpeg -i input.mp4 -vf "exposure=exposure=0.5:black=0.02" output.mp4
```

## Notes

- Each EV stop doubles the brightness: +1 EV = 2× brighter, +2 EV = 4× brighter, -1 EV = half as bright.
- `exposure` operates in linear light, making it more perceptually uniform than a simple multiply (e.g. `eq=brightness`).
- For non-linear brightness adjustment (S-curves, contrast), `eq` or `curves` provide more control.
- On HDR content, `exposure` can be combined with `tonemap` for HDR-to-SDR workflows.
