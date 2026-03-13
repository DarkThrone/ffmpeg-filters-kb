+++
title = "setdar"
description = "Set the display aspect ratio (DAR) of a video stream by adjusting the sample aspect ratio (SAR), without scaling pixels."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "aspect ratio", "metadata"]

[extra]
filter_type = "utility"
since = ""
see_also = ["scale", "crop", "pad"]
parameters = ["dar", "max"]
cohort = 3
+++

The `setdar` filter sets the Display Aspect Ratio (DAR) of a video stream by changing the Sample Aspect Ratio (SAR) metadata — it does **not** rescale the pixels. This is used to correct mislabeled anamorphic content (e.g., 720×576 material that should display as 16:9 but is incorrectly tagged as 4:3), or to override the aspect ratio for a specific output format.

## Quick Start

```sh
# Tag a 720x576 frame as 16:9 display aspect
ffmpeg -i input.mp4 -vf "setdar=dar=16/9" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dar / ratio / r | string | `0` | Display aspect ratio as a fraction (`16/9`), decimal (`1.7778`), or expression. `0` = keep input DAR. |
| max | int | `100` | Maximum numerator/denominator when reducing the ratio to a fraction. |

## Expression Variables (for `dar`)

| Variable | Description |
|----------|-------------|
| `w`, `h` | Input frame width and height. |
| `a` | `w / h` (pixel aspect). |
| `sar` | Input sample aspect ratio. |
| `dar` | Input display aspect ratio. |

## Examples

### Set to 16:9

```sh
ffmpeg -i anamorphic.mp4 -vf "setdar=dar=16/9" corrected.mp4
```

### Set to 4:3

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=4/3" output.mp4
```

### Set using decimal value

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=1.7778" widescreen.mp4
```

### Compute DAR based on pixel dimensions (no-op, keeps correct DAR)

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=w/h" output.mp4
```

## Notes

- `setdar` changes the SAR in the bitstream headers — the pixel data is unchanged. Players that respect SAR will display correctly; players that ignore SAR will show the raw pixel dimensions.
- DAR = `(width / height) × SAR`. If you have 720×576 pixels at SAR 64:45, DAR = `(720/576) × (64/45) = 16/9`.
- To actually resize pixels to match the aspect ratio, use `scale=1280:720` or `scale=iw*sar:ih`.
- Use `ffprobe` to check the current DAR/SAR values before applying this filter.
