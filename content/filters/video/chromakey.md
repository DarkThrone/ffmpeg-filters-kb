+++
title = "chromakey"
description = "Remove a chroma key color from video (green/blue screen) by making matching pixels transparent."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["keying", "compositing", "green-screen"]

[extra]
filter_type = "video"
since = ""
see_also = ["colorkey", "overlay"]
parameters = ["color", "similarity", "blend", "yuv"]
cohort = 2
source_file = "libavfilter/vf_chromakey.c"
+++

The `chromakey` filter removes a chroma key color (typically green or blue) from video by making matching pixels transparent. It operates in YUV color space, which is more robust on compressed video formats than the RGB-based `colorkey`. This is the standard way to remove green screen and blue screen backgrounds in FFmpeg.

## Quick Start

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.1:0.1" keyed.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | color | `black` | The chroma key color. Accepts hex `0xRRGGBB` or named colors. Common: `0x00FF00` (green), `0x0000FF` (blue). |
| similarity | float | `0.01` | Color range to key out (YUV distance). Range: 0.01–1. Higher = more aggressive keying. |
| blend | float | `0.0` | Blending factor at the key boundary for soft edges. Range: 0–1. |
| yuv | bool | `0` | If enabled, the `color` parameter is specified in YUV values instead of RGB. |

## Examples

### Basic green screen removal

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.1:0.1" keyed.mp4
```

### Blue screen removal

```sh
ffmpeg -i bluescreen.mp4 -vf "chromakey=0x0000FF:0.15:0.05" keyed.mp4
```

### Composite over a new background

```sh
ffmpeg -i background.mp4 -i greenscreen.mp4 \
  -filter_complex "[1:v]chromakey=0x00FF00:0.1:0.1[fg];[0:v][fg]overlay" \
  output.mp4
```

### Adjust similarity for a spill-heavy key

Increase similarity to catch green spill on hair and edges.

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.25:0.15" keyed.mp4
```

## Notes

- `similarity` determines how broadly the key color is matched in YUV space. Values of 0.1–0.2 are typical for clean studio footage; increase up to 0.3–0.4 for compressed or poorly lit backgrounds.
- `blend` adds a soft transition at the edge, reducing aliasing but potentially showing some background colour at the border.
- `chromakey` works in YUV and is more resilient to H.264/H.265 chroma subsampling than `colorkey` (RGB). Prefer it for encoded footage.
- For best results, key before any other color correction — adjust the key color to the exact value of your screen.
