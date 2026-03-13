+++
title = "colorlevels"
description = "Adjust input and output black/white levels per channel, similar to Levels in Photoshop."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "color-correction", "levels"]

[extra]
filter_type = "video"
since = ""
see_also = ["curves", "eq", "colorbalance"]
parameters = ["rimin", "gimin", "bimin", "aimin", "rimax", "gimax", "bimax", "aimax", "romin", "gomin", "bomin", "aomin", "romax", "gomax", "bomax", "aomax"]
cohort = 2
source_file = "libavfilter/vf_colorlevels.c"
+++

The `colorlevels` filter adjusts the black point, white point, and output range of each color channel independently. Setting the input black and white points remaps the tonal range, allowing you to correct washed-out footage or fix colour casts. It is equivalent to the Levels adjustment tool in Photoshop or Lightroom.

## Quick Start

```sh
# Remap input range 0.06–0.94 to full output range
ffmpeg -i input.mp4 -vf "colorlevels=rimin=0.06:gimin=0.06:bimin=0.06:rimax=0.94:gimax=0.94:bimax=0.94" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rimin | double | `0.0` | Input black point for red channel. Range: 0–1. |
| gimin | double | `0.0` | Input black point for green channel. |
| bimin | double | `0.0` | Input black point for blue channel. |
| aimin | double | `0.0` | Input black point for alpha channel. |
| rimax | double | `1.0` | Input white point for red channel. Range: 0–1. |
| gimax | double | `1.0` | Input white point for green channel. |
| bimax | double | `1.0` | Input white point for blue channel. |
| aimax | double | `1.0` | Input white point for alpha channel. |
| romin | double | `0.0` | Output black point for red channel. |
| gomin | double | `0.0` | Output black point for green channel. |
| bomin | double | `0.0` | Output black point for blue channel. |
| aomin | double | `0.0` | Output black point for alpha channel. |
| romax | double | `1.0` | Output white point for red channel. |
| gomax | double | `1.0` | Output white point for green channel. |
| bomax | double | `1.0` | Output white point for blue channel. |
| aomax | double | `1.0` | Output white point for alpha channel. |

## Examples

### Fix washed-out footage

Remap the actual signal range (0.06–0.94) to the full 0–1 range.

```sh
ffmpeg -i washed_out.mp4 -vf "colorlevels=rimin=0.06:gimin=0.06:bimin=0.06:rimax=0.94:gimax=0.94:bimax=0.94" output.mp4
```

### Correct a blue colour cast

Reduce the blue white point to pull down highlights in the blue channel.

```sh
ffmpeg -i bluish.mp4 -vf "colorlevels=bimax=0.85" output.mp4
```

### Add a fade-to-black (output remapping)

Limit the output range to 0–0.8 for a faded, low-contrast look.

```sh
ffmpeg -i input.mp4 -vf "colorlevels=romax=0.8:gomax=0.8:bomax=0.8" output.mp4
```

### Lift blacks (output black point)

Set output minimum to 0.05 for a film-print faded-black look.

```sh
ffmpeg -i input.mp4 -vf "colorlevels=romin=0.05:gomin=0.05:bomin=0.05" output.mp4
```

## Notes

- `imax` = input white point: pixels at this value or above are mapped to output white. Setting it below 1.0 stretches highlights.
- `imin` = input black point: pixels at this value or below are mapped to output black. Setting it above 0.0 crushes shadows.
- Values are 0–1 regardless of bit depth; the filter scales internally.
- For per-channel tonal curves, `curves` provides finer control; for simple contrast/brightness, `eq` is faster.
