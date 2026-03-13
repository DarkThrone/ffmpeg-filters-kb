+++
title = "colorkey"
description = "Remove a specific RGB color from video by making matching pixels transparent."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["keying", "compositing", "color"]

[extra]
filter_type = "video"
since = ""
see_also = ["chromakey", "overlay"]
parameters = ["color", "similarity", "blend"]
cohort = 2
+++

The `colorkey` filter removes a specific color from video by making pixels that match the key color fully or partially transparent. Unlike `chromakey` which operates in YUV color space, `colorkey` works in RGB and is more accurate for exact color matching. It is useful for removing solid colored backgrounds in title cards, motion graphics, and screen recordings.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "colorkey=0x00FF00:0.3:0.1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | color | `black` | The key color to remove. Accepts hex `0xRRGGBB` or color names. |
| similarity | float | `0.01` | Radius of colors to match. 0=exact match only, 1=all colors match. Range: 0–1. |
| blend | float | `0.0` | Softness of the edge. 0=hard cut, 1=gradual fade at boundary. Range: 0–1. |

## Examples

### Remove a green screen

```sh
ffmpeg -i greenscreen.mp4 -vf "colorkey=0x00FF00:0.3:0.1" keyed.mp4
```

### Remove white background from title card

```sh
ffmpeg -i title.mp4 -vf "colorkey=white:0.2:0.05" keyed.mp4
```

### Composite keyed video over background

Use `overlay` after `colorkey` to place the subject over a new background.

```sh
ffmpeg -i background.mp4 -i subject.mp4 \
  -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[keyed];[0:v][keyed]overlay" \
  output.mp4
```

### Soft key with blend for anti-aliased edges

```sh
ffmpeg -i input.mp4 -vf "colorkey=0x00B140:0.35:0.15" output.mp4
```

## Notes

- `colorkey` operates in RGB color space, making it precise for exact solid colors but potentially less robust on compressed video than `chromakey` (YUV).
- Start with `similarity=0.3` and `blend=0.1` for green screen work; adjust based on the cleanliness of your key color.
- Compressed video (H.264, etc.) often has chroma noise around key colors — increase `similarity` or `blend` to compensate.
- For true chroma key work (Rec. 709 YCbCr), `chromakey` usually gives cleaner results on encoded footage.
