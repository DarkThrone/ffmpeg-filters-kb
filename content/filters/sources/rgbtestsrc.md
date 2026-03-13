+++
title = "rgbtestsrc"
description = "Generate an RGB test pattern with red, green, and blue vertical stripes for verifying channel ordering."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "pattern", "source", "color"]

[extra]
filter_type = "source"
since = ""
see_also = ["yuvtestsrc", "testsrc", "smptebars"]
parameters = ["size", "rate", "duration"]
cohort = 3
source_file = "libavfilter/vsrc_testsrc.c"
+++

The `rgbtestsrc` source generates a simple test pattern with red, green, and blue vertical stripes from top to bottom. It is primarily used to diagnose RGB channel order issues — if the red stripe appears blue and vice versa, the input/output channel mapping is swapped.

## Quick Start

```sh
ffplay -f lavfi "rgbtestsrc=size=640x480"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Check RGB channel order

```sh
ffplay -f lavfi "rgbtestsrc=size=640x480"
```

### Generate a single test frame

```sh
ffmpeg -f lavfi -i "rgbtestsrc=size=640x480" -frames:v 1 rgb_test.png
```

### Verify a codec/container preserves colors

```sh
ffmpeg -f lavfi -i "rgbtestsrc=size=640x480:rate=1" -t 1 test.mov
ffplay test.mov
```

## Notes

- You should see three horizontal bands from top to bottom: **red**, **green**, **blue**.
- If the red and blue bands are swapped, the pixel format has reversed RGB channel order (a common issue with some codecs or pixel format conversions).
- `yuvtestsrc` generates the equivalent Y/Cb/Cr stripe pattern for YUV format diagnostics.
