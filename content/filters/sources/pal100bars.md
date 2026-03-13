+++
title = "pal100bars"
description = "Generate EBU PAL 100% color bars for European broadcast calibration."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "broadcast", "color-bars", "source", "pal", "ebu"]

[extra]
filter_type = "source"
since = ""
see_also = ["pal75bars", "smptebars", "smptehdbars"]
parameters = ["size", "rate", "duration"]
cohort = 3
+++

The `pal100bars` source generates EBU (European Broadcasting Union) PAL color bars at 100% amplitude. Unlike `pal75bars` (75% amplitude) and the SMPTE variants, PAL 100% bars drive the color components to full amplitude, making them useful for peak signal level testing and gamut verification on European broadcast equipment.

## Quick Start

```sh
ffplay -f lavfi "pal100bars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### PAL SD 100% bars

```sh
ffplay -f lavfi "pal100bars=size=720x576:rate=25"
```

### Generate bars clip

```sh
ffmpeg -f lavfi -i "pal100bars=size=720x576:rate=25" -t 10 pal100bars.mp4
```

## Notes

- EBU PAL 100% bars: all seven color bars at 100% amplitude (white, yellow, cyan, green, magenta, red, blue).
- Use `pal75bars` for the more common 75% level variant used in standard PAL test recordings.
- SMPTE bars (`smptebars`, `smptehdbars`) are the North American equivalents.
