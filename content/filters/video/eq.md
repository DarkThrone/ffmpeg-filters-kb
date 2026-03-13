+++
title = "eq"
description = "Adjust brightness, contrast, saturation, and gamma of the input video with per-channel gamma support."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "color-correction", "grading", "brightness"]

[extra]
filter_type = "video"
since = ""
see_also = ["hue", "colorbalance", "curves"]
parameters = ["brightness", "contrast", "saturation", "gamma", "gamma_r", "gamma_g", "gamma_b", "gamma_weight", "eval"]
cohort = 1
source_file = "libavfilter/vf_eq.c"
+++

The `eq` filter provides traditional video equalizer controls: brightness, contrast, saturation, and gamma. It supports per-channel gamma adjustments (red, green, blue) for fine-grained color grading, and all parameters accept arithmetic expressions, enabling dynamic changes per frame. The filter can be applied once at initialization or reevaluated every frame depending on the `eval` setting.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| brightness | string (expr) | `0` | Brightness offset. Range: [-1.0, 1.0]. `0` = no change. |
| contrast | string (expr) | `1` | Contrast multiplier. Range: [-1000.0, 1000.0]. `1` = no change. |
| saturation | string (expr) | `1` | Saturation multiplier. Range: [0.0, 3.0]. `1` = no change, `0` = grayscale. |
| gamma | string (expr) | `1` | Overall gamma correction. Range: [0.1, 10.0]. `1` = no change. |
| gamma_r | string (expr) | `1` | Gamma correction for the red channel. Range: [0.1, 10.0]. |
| gamma_g | string (expr) | `1` | Gamma correction for the green channel. Range: [0.1, 10.0]. |
| gamma_b | string (expr) | `1` | Gamma correction for the blue channel. Range: [0.1, 10.0]. |
| gamma_weight | string (expr) | `1` | Reduces gamma effect on bright areas. Range: [0.0, 1.0]. `0` = no gamma, `1` = full gamma. |
| eval | int | `init` | When to evaluate expressions: `init` (once) or `frame` (per frame). |

### Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Frame count, starting from 0 |
| `r` | Frame rate of the input video |
| `t` | Timestamp in seconds |

## Examples

### Increase brightness and contrast

Brighten a slightly underexposed clip and add some contrast punch.

```sh
ffmpeg -i input.mp4 -vf "eq=brightness=0.08:contrast=1.3" output.mp4
```

### Warm color grade with gamma

Apply a slight red boost via gamma_r and reduce blue for a warm look.

```sh
ffmpeg -i input.mp4 -vf "eq=gamma_r=1.1:gamma_b=0.9:saturation=1.2" output.mp4
```

### Convert to grayscale (via saturation)

Set saturation to 0 to remove all color.

```sh
ffmpeg -i input.mp4 -vf "eq=saturation=0" output.mp4
```

### Dynamic brightness change over time

Use `eval=frame` and a `t`-based expression to animate brightness as a function of time.

```sh
ffmpeg -i input.mp4 -vf "eq=brightness='0.1*sin(t)':eval=frame" output.mp4
```

### Fix underexposed dark footage with gamma

Lift the shadows using gamma correction while protecting the highlights with `gamma_weight`.

```sh
ffmpeg -i input.mp4 -vf "eq=gamma=1.5:gamma_weight=0.5" output.mp4
```

## Notes

- Contrast values below `-1` or above `1` create increasingly extreme effects; use values close to `1.0` for subtle grading.
- `gamma_weight` is used to prevent blown-out highlights when boosting overall gamma — a value of `0.5` keeps bright areas from becoming completely white.
- When `eval=frame`, expressions are re-evaluated for every frame, which allows animation but has a small CPU overhead. Use `eval=init` for static corrections.
- `eq` uses an approximate gamma calculation rather than a fully color-managed workflow; for precision color work, consider `curves` or `lut3d` with a proper ICC profile.
