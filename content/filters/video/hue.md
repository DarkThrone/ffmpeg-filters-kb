+++
title = "hue"
description = "Adjust the hue angle and saturation of the input video, with optional brightness control and per-frame expression support."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "hue", "saturation", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["eq", "colorbalance", "curves"]
parameters = ["h", "H", "s", "b"]
cohort = 1
source_file = "libavfilter/vf_hue.c"
+++

The `hue` filter modifies the hue rotation and saturation of a video in the YCbCr color space, operating on the chroma channels while leaving luma (brightness) largely intact. The hue angle can be specified in degrees (`h`) or radians (`H`), and all parameters accept per-frame expressions, enabling animated color effects like cycling hues or time-based saturation fades. A brightness adjustment (`b`) is also available for simple luma tweaks.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "hue=h=30:s=1.2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| h | string (expr) | `0` | Hue rotation angle in degrees. Accepts expressions. Mutually exclusive with `H`. |
| H | string (expr) | `0` | Hue rotation angle in radians. Mutually exclusive with `h`. |
| s | string (expr) | `1` | Saturation multiplier. Range: [-10, 10]. `0` = grayscale, `1` = original, `>1` = more saturated. |
| b | string (expr) | `0` | Brightness adjustment. Range: [-10, 10]. `0` = no change. |

### Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Frame count of the input frame, starting from 0 |
| `pts` | Presentation timestamp in timebase units |
| `r` | Input frame rate |
| `t` | Timestamp in seconds |
| `tb` | Input video timebase |

## Examples

### Rotate hue by 90 degrees (green to cyan-blue shift)

Shift the color wheel by 90 degrees for a stylistic color transformation.

```sh
ffmpeg -i input.mp4 -vf "hue=h=90" output.mp4
```

### Convert to grayscale

Set saturation to 0 to remove all color information.

```sh
ffmpeg -i input.mp4 -vf "hue=s=0" output.mp4
```

### Boost saturation for vivid colors

Increase saturation to make colors more vivid and punchy.

```sh
ffmpeg -i input.mp4 -vf "hue=s=1.5" output.mp4
```

### Animated rainbow hue cycling

Rotate the hue continuously over time for a psychedelic color-cycling effect.

```sh
ffmpeg -i input.mp4 -vf "hue=H='2*PI*t/10'" output.mp4
```

### Saturation fade-in over 3 seconds

Animate from grayscale to full color over the first 3 seconds.

```sh
ffmpeg -i input.mp4 -vf "hue=s='min(t/3,1)'" output.mp4
```

## Notes

- `h` and `H` are mutually exclusive — specifying both causes an error. Use `h` for degrees (more intuitive) or `H` for radians.
- The saturation range is [-10, 10], but values below 0 invert the colors while also desaturating; typically keep `s` between 0 and 2 for natural looks.
- `hue` operates on the YCbCr Cb and Cr channels, so it does not affect the luma (brightness) of the image when only `h` or `s` are changed.
- The filter supports runtime commands for `h`, `H`, `s`, and `b`, enabling live parameter adjustment during streaming.
