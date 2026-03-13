+++
title = "lut3d"
description = "Apply a 3D color LUT from a file to adjust colors with full three-dimensional color mapping."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "lut", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["haldclut", "lut", "colorspace"]
parameters = ["file", "interp"]
cohort = 2
+++

The `lut3d` filter loads a 3D Look-Up Table from an external file and applies it to video. Unlike 1D per-channel LUTs, a 3D LUT maps every possible RGB combination to a new color, allowing complex non-linear color transformations that cannot be expressed per-channel. It supports industry-standard formats including `.cube`, `.3dl`, `.dat`, and `.m3d`.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| file | string | Path to the 3D LUT file. Supported formats: `.cube` (Adobe), `.3dl` (Autodesk), `.dat`, `.m3d` (Pandora), `.csp` (cineSpace). |
| interp | int | Interpolation method: `nearest` (no interpolation), `trilinear` (default, good quality), `tetrahedral` (highest quality). |

## Examples

### Apply a .cube LUT for cinematic grading

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=film_look.cube" output.mp4
```

### Use tetrahedral interpolation for best quality

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube:interp=tetrahedral" output.mp4
```

### Apply LUT and re-encode with libx264

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube" -c:v libx264 -crf 18 output.mp4
```

### Chain with colorspace conversion

Convert from Rec.709 to log-C before applying a log-to-display LUT.

```sh
ffmpeg -i input.mp4 -vf "colorspace=all=bt709,lut3d=file=logc_to_display.cube" output.mp4
```

## Notes

- `.cube` files from tools like DaVinci Resolve, Adobe Premiere, or online LUT collections work directly with this filter.
- Tetrahedral interpolation provides the most accurate results and is preferred for final grading, while trilinear is a good default for previews.
- For Hald CLUT images (PNG-based LUTs) instead of file-based LUTs, use the `haldclut` filter.
- 3D LUTs operate in linear RGB space; if your footage uses a log or gamma curve, convert to linear first with `colorspace` or `lut`.
