+++
title = "setsar"
description = "Set the sample (pixel) aspect ratio of the video frames without rescaling the pixel data."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["aspect-ratio", "metadata", "format"]

[extra]
filter_type = "video"
since = ""
see_also = ["scale", "format", "crop"]
parameters = ["sar", "ratio", "max"]
cohort = 1
+++

The `setsar` filter changes the Sample Aspect Ratio (SAR) metadata of video frames without modifying the actual pixel data. SAR describes the shape of individual pixels (e.g., square pixels have SAR 1:1, while anamorphic SD video often has non-square pixels). Use `setsar` to correct incorrectly tagged SAR metadata, to signal square pixels after a resize operation, or to prepare anamorphic content for display. The companion filter `setdar` sets the Display Aspect Ratio instead.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "setsar=1:1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sar (ratio, r) | string | — | The desired sample aspect ratio as a fraction (e.g., `1:1`, `16:15`, `64:45`). |
| max | int | `100` | Maximum value for numerator or denominator in the simplified ratio. |

## Examples

### Reset SAR to square pixels (1:1)

Mark the output as having square pixels, which is the standard for most modern video.

```sh
ffmpeg -i input.mp4 -vf "setsar=1:1" output.mp4
```

### Set SAR for PAL 16:9 anamorphic

Tag widescreen SD video with the appropriate non-square pixel ratio.

```sh
ffmpeg -i input.mpg -vf "setsar=64:45" output.mp4
```

### Fix incorrectly tagged SAR after scaling

After scaling a video, reset SAR to 1:1 to ensure correct display.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720,setsar=1:1" output.mp4
```

### Use rational expression

Specify the ratio as a division expression.

```sh
ffmpeg -i input.mp4 -vf "setsar=ratio=16/15" output.mp4
```

## Notes

- `setsar` only modifies metadata; it does not resample or rescale any pixel data. If you need actual pixel changes to match a new aspect ratio, use `scale` instead.
- The `scale` filter automatically adjusts SAR to maintain the display aspect ratio when resizing; you usually only need `setsar` to override or correct that metadata afterward.
- Display Aspect Ratio (DAR) = SAR * (width / height). Use `setdar` to set the DAR directly if that is more convenient.
- Many encoders and muxers reset SAR to 1:1 unless explicitly told otherwise; check the output with `ffprobe` to confirm the metadata was written correctly.
