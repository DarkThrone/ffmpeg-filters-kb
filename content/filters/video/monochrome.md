+++
title = "monochrome"
description = "Convert video to grayscale using a custom color filter for stylized black-and-white output."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "grading", "black-and-white"]

[extra]
filter_type = "video"
since = ""
see_also = ["huesaturation"]
parameters = ["cb", "cr", "size", "high"]
cohort = 2
+++

The `monochrome` filter converts color video to stylized black-and-white by allowing you to specify the chroma channel contributions to the final luminance. This is analogous to using a colored filter in front of a black-and-white film camera: a red filter makes reds lighter and blues darker. It produces more expressive monochrome conversions than a simple desaturation.

## Quick Start

```sh
# Classic B&W with slight red-channel boost
ffmpeg -i input.mp4 -vf "monochrome=cb=-0.1:cr=0.3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cb | float | `0.0` | Chroma blue (Cb) contribution to luminance. Range: -1–1. Negative = blue tones darker. |
| cr | float | `0.0` | Chroma red (Cr) contribution to luminance. Range: -1–1. Positive = red/warm tones lighter. |
| size | float | `1.0` | Color filter size, controlling the width of the chroma sensitivity. Range: 0–1. |
| high | float | `0.0` | Highlights sensitivity adjustment. Range: 0–1. |

## Examples

### Neutral desaturation (no chroma bias)

```sh
ffmpeg -i input.mp4 -vf "monochrome" output.mp4
```

### Red filter effect (landscapes, dramatic skies)

Makes blues darker and reds lighter — classic for sky drama and foliage.

```sh
ffmpeg -i landscape.mp4 -vf "monochrome=cr=0.5:cb=-0.3" output.mp4
```

### Green filter (portraits, skin tones)

Brightens skin tones and foliage.

```sh
ffmpeg -i portrait.mp4 -vf "monochrome=cr=-0.2:cb=-0.1" output.mp4
```

### Blue filter effect (high-contrast, dark skies)

```sh
ffmpeg -i input.mp4 -vf "monochrome=cb=0.5:cr=-0.3" output.mp4
```

## Notes

- `cr > 0` brightens warm/red tones and darkens cool/blue tones, similar to an orange or red filter on a film camera.
- `cb > 0` brightens blues; `cb < 0` darkens blues (simulating a red filter's effect on blue sky).
- For a purely flat desaturation, use `huesaturation=saturation=-3` or `colorchannelmixer` to average channels equally.
- `size` affects how broadly or narrowly the color filter sensitivity is applied. Default 1.0 is full-width.
