+++
title = "pal75bars"
description = "Generate EBU PAL 75% color bars — the standard European broadcast test signal for monitor calibration."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "broadcast", "color-bars", "source", "pal", "ebu"]

[extra]
filter_type = "source"
since = ""
see_also = ["pal100bars", "smptebars"]
parameters = ["size", "rate", "duration"]
cohort = 3
source_file = "libavfilter/vsrc_testsrc.c"
+++

The `pal75bars` source generates EBU PAL 75% color bars — the standard European broadcast test signal. The 75% amplitude is the EBU recommended level for color bar generators, matching the output of most European broadcast equipment and VTR leaders. These are the go-to bars for calibrating PAL monitors and VTR decks.

## Quick Start

```sh
ffplay -f lavfi "pal75bars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard PAL 75% bars

```sh
ffplay -f lavfi "pal75bars=size=720x576:rate=25"
```

### Embed as test leader in a PAL production file

```sh
ffmpeg -f lavfi -i "pal75bars=size=720x576:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 60 -pix_fmt yuv420p leader.mov
```

## Notes

- 75% bars are the EBU standard for PAL broadcast test recordings; `pal100bars` provides full-amplitude bars.
- The seven color patches are: white, yellow, cyan, green, magenta, red, blue — all at 75% of peak amplitude.
- Use with `vectorscope` to verify the bars land on their expected targets in the scope.
