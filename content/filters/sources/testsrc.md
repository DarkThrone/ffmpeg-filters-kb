+++
title = "testsrc"
description = "Generate an animated test video pattern showing color bars, a scrolling gradient, and a frame timestamp counter."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "pattern", "source"]

[extra]
filter_type = "source"
since = ""
see_also = ["testsrc2", "smptebars", "rgbtestsrc"]
parameters = ["size", "rate", "duration", "sar"]
cohort = 3
+++

The `testsrc` source generates an animated test video pattern with a color patch grid, a scrolling gradient bar, and a live frame-number counter. It is mainly used for pipeline testing, format verification, and building filter graphs without needing a real input file. All video test sources share the same common parameters (`size`, `rate`, `duration`, `sar`).

## Quick Start

```sh
# 10-second 1080p test pattern at 30fps
ffmpeg -f lavfi -i "testsrc=size=1920x1080:rate=30" -t 10 output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. Accepts named sizes (`hd1080`, `vga`) or `WxH`. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. Omit for infinite stream. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard definition test pattern (PAL)

```sh
ffplay -f lavfi "testsrc=size=720x576:rate=25"
```

### Generate 5 seconds as PNG images

```sh
ffmpeg -f lavfi -i "testsrc=size=640x480:rate=1" -t 5 frame_%04d.png
```

### Use as input in a filter_complex

```sh
ffmpeg -f lavfi -i "testsrc=size=1280x720:rate=30" -vf "drawtext=text='Hello'" -t 5 out.mp4
```

### Generate a single frame

```sh
ffmpeg -f lavfi -i "testsrc=size=1920x1080" -frames:v 1 test_frame.png
```

## Notes

- The pattern includes: a 7-color bar section, a scrolling luminance gradient, a 100% white box, and a frame counter in the bottom-right corner.
- `testsrc2` supports more pixel formats (beyond `rgb24`) and is preferred when testing filters that operate on YUV or high bit-depth formats.
- All video test sources (`smptebars`, `rgbtestsrc`, `yuvtestsrc`, etc.) accept the same `size`, `rate`, `duration`, `sar` parameters.
- Use `-f lavfi` when specifying the source on the command line; in `-filter_complex` it is used directly as `[testsrc=...]`.
