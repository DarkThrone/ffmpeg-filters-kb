+++
title = "colorbalance"
description = "Adjust the color balance of video by modifying red, green, and blue channel intensities in shadows, midtones, and highlights."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "color-correction", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["hue", "eq", "curves"]
parameters = ["rs", "gs", "bs", "rm", "gm", "bm", "rh", "gh", "bh", "pl"]
cohort = 1
+++

The `colorbalance` filter adjusts the intensity of red, green, and blue channels independently across three tonal regions: shadows (darkest pixels), midtones (medium pixels), and highlights (brightest pixels). Each adjustment is a value from -1.0 to 1.0, where positive shifts the balance toward the primary color and negative shifts it toward the complementary color. This makes it analogous to the Color Balance tool in photo editing applications.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rs=0.1:gs=-0.05:bs=-0.1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rs | float | `0` | Red channel adjustment in shadows. Range: [-1.0, 1.0]. |
| gs | float | `0` | Green channel adjustment in shadows. |
| bs | float | `0` | Blue channel adjustment in shadows. |
| rm | float | `0` | Red channel adjustment in midtones. |
| gm | float | `0` | Green channel adjustment in midtones. |
| bm | float | `0` | Blue channel adjustment in midtones. |
| rh | float | `0` | Red channel adjustment in highlights. |
| gh | float | `0` | Green channel adjustment in highlights. |
| bh | float | `0` | Blue channel adjustment in highlights. |
| pl | bool | `0` | Preserve lightness when adjusting color balance. Prevents color shifts from altering overall brightness. |

## Examples

### Add a warm sunset tone

Boost reds and reduce blues in midtones and highlights to create a warm, golden look.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rm=0.2:rh=0.1:bm=-0.15:bh=-0.1" output.mp4
```

### Add a cool cinematic look

Shift shadows toward blue and highlights toward teal for a common film grade.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=bs=0.2:gs=0.05:rh=-0.1:gh=0.05:bh=0.1" output.mp4
```

### Add red cast to shadows only

A subtle red-shadow treatment often used for dramatic film looks.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rs=0.3" output.mp4
```

### Correct a blue color cast

Remove an unwanted blue cast from shadows while preserving midtones and highlights.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=bs=-0.2:bm=-0.1" output.mp4
```

## Notes

- All range values are [-1.0, 1.0]; values outside this range are clamped. Setting all values to `0` (the default) passes the video through unchanged.
- Use `pl=1` (preserve lightness) when making strong color balance adjustments to prevent the overall brightness of the image from shifting.
- `colorbalance` adjusts the RGB channels after YUV-to-RGB conversion; it works on the pixel values directly and does not distinguish between chroma and luma.
- For finer tonal control, consider `curves` which allows per-channel spline adjustments, or combine `colorbalance` with `eq` for brightness/contrast alongside color adjustments.
