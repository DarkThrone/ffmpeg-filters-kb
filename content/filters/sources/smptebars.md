+++
title = "smptebars"
description = "Generate SMPTE EG 1-1990 standard-definition color bars for broadcast calibration and signal testing."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "broadcast", "color-bars", "source"]

[extra]
filter_type = "source"
since = ""
see_also = ["smptehdbars", "pal100bars", "pal75bars"]
parameters = ["size", "rate", "duration"]
cohort = 3
+++

The `smptebars` source generates the classic SMPTE EG 1-1990 color bar pattern used in SD (standard definition) broadcast for monitor calibration, signal level testing, and tape leader. The pattern includes the 7 standard colors at 75% amplitude plus the PLUGE sub-black test signal in the lower section.

## Quick Start

```sh
ffplay -f lavfi "smptebars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard PAL SD color bars

```sh
ffplay -f lavfi "smptebars=size=720x576:rate=25"
```

### Standard NTSC SD color bars

```sh
ffplay -f lavfi "smptebars=size=720x480:rate=30000/1001"
```

### Generate a 10-second bars clip with tone

```sh
ffmpeg -f lavfi -i "smptebars=size=720x576:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 10 bars_with_tone.mp4
```

### Single frame for documentation

```sh
ffmpeg -f lavfi -i "smptebars=size=1280x720" -frames:v 1 smptebars.png
```

## Notes

- Based on SMPTE EG 1-1990 for SD content. For HD use `smptehdbars` (SMPTE RP 219-2002).
- The pattern includes 7 standard color bars (white, yellow, cyan, green, magenta, red, blue) at 75% amplitude plus the PLUGE signal (sub-black, black, super-black) in the lower portion.
- PLUGE is used for CRT monitor black level calibration; in modern workflows it is less critical but still standard for tape leaders.
- Pair with a 1 kHz sine tone (`sine=frequency=1000`) for a complete broadcast test leader.
