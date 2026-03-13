+++
title = "testsrc2"
description = "Generate an animated test video pattern similar to testsrc but with support for a wider range of pixel formats."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "pattern", "source"]

[extra]
filter_type = "source"
since = ""
see_also = ["testsrc", "smptebars"]
parameters = ["size", "rate", "duration", "sar"]
cohort = 3
+++

The `testsrc2` source is nearly identical to `testsrc` but supports more pixel formats beyond the `rgb24` that `testsrc` is limited to. This makes it the preferred choice when testing filters that operate on YUV, planar, or high bit-depth pixel formats, since it avoids a forced format conversion before the test filter.

## Quick Start

```sh
ffplay -f lavfi "testsrc2=size=1280x720:rate=30"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Test a YUV-native filter without format conversion

```sh
ffmpeg -f lavfi -i "testsrc2=size=1280x720:rate=25" -vf "unsharp" -t 5 out.mp4
```

### Generate 10-bit test frames

```sh
ffmpeg -f lavfi -i "testsrc2=size=1920x1080:rate=25" -pix_fmt yuv420p10le -t 5 out.mkv
```

### Preview in ffplay

```sh
ffplay -f lavfi "testsrc2=size=640x480:rate=30"
```

## Notes

- Prefer `testsrc2` over `testsrc` when testing filters on YUV or non-RGB pixel formats.
- The visual pattern is the same as `testsrc`: color grid, scrolling gradient, frame counter.
- Both `testsrc` and `testsrc2` produce an animated pattern; use `-frames:v 1` for a single still frame.
