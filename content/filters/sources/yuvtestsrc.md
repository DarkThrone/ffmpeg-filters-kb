+++
title = "yuvtestsrc"
description = "Generate a YUV test pattern with Y, Cb, and Cr vertical stripes for verifying YUV channel ordering."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "pattern", "source", "yuv"]

[extra]
filter_type = "source"
since = ""
see_also = ["rgbtestsrc", "testsrc"]
parameters = ["size", "rate", "duration"]
cohort = 3
+++

The `yuvtestsrc` source generates a test pattern with Y (luma), Cb, and Cr (chroma) vertical stripes, useful for verifying that YUV components are mapped correctly and that chroma channel ordering is preserved through a processing pipeline.

## Quick Start

```sh
ffplay -f lavfi "yuvtestsrc=size=640x480"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Verify YUV channel order

```sh
ffplay -f lavfi "yuvtestsrc=size=640x480"
```

### Generate a single YUV test frame

```sh
ffmpeg -f lavfi -i "yuvtestsrc=size=640x480" -frames:v 1 yuv_test.png
```

### Test YUV format round-trip

```sh
ffmpeg -f lavfi -i "yuvtestsrc=size=640x480:rate=1" -pix_fmt yuv420p -t 1 test.mkv
ffplay test.mkv
```

## Notes

- You should see three horizontal bands: **Y (luma)**, **Cb**, **Cr** from top to bottom.
- If the Cb and Cr stripes appear swapped, the chroma plane ordering in the pixel format is reversed.
- Use `rgbtestsrc` for testing RGB channel ordering instead.
