+++
title = "ciescope"
description = "Overlay a CIE 1931 chromaticity diagram on video to visualize the color gamut and distribution of pixel colors."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "video", "color", "scope", "analysis"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["vectorscope", "waveform", "histogram"]
parameters = ["system", "cie", "gamuts", "size", "intensity", "fill"]
cohort = 3
source_file = "libavfilter/vf_ciescope.c"
+++

The `ciescope` filter renders a CIE 1931 xy chromaticity diagram and plots the colors present in the input video onto it. The horseshoe-shaped diagram represents all visible colors, with white at the center. Each video frame's pixel colors appear as dots or a heatmap, showing how the content's gamut compares to standard color spaces (sRGB, DCI-P3, BT.2020, etc.). It is used in color grading QC to verify gamut compliance and spot out-of-gamut colors.

## Quick Start

```sh
ffplay -i input.mp4 -vf ciescope
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| system | int | `hdtv` | Reference color system to display: `ntsc`, `470m`, `ebu`, `470bg`, `smpte`, `240m`, `film`, `hdtv`, `cie1931`, `2020`, `dcip3`. |
| cie | int | `xyy` | CIE diagram type: `xyy`, `ucs`, `luv`. |
| gamuts | flags | `0` | Additional gamut triangles to overlay (bitfield: 1=ntsc, 2=470m, …). |
| size / s | image_size | `512x512` | Output size of the scope image. |
| intensity / i | float | `0.001` | Intensity of each plotted pixel dot. |
| fill | bool | `1` | Fill the chromaticity diagram with the visible spectrum colors. |

## Examples

### Basic CIE scope overlay on video

```sh
ffplay -i input.mp4 -vf ciescope
```

### Show BT.2020 gamut triangle with sRGB reference

```sh
ffplay -i input.mp4 -vf "ciescope=system=hdtv:gamuts=0x40"
```

### Save first 10 seconds of CIE scope video

```sh
ffmpeg -i input.mp4 -vf ciescope -t 10 cie_scope.mp4
```

### Increase dot intensity for sparse colors

```sh
ffplay -i input.mp4 -vf "ciescope=intensity=0.01:size=800x800"
```

## Notes

- Colors outside the displayed gamut triangle are outside that color space — useful for checking HDR/wide-gamut content.
- Low `intensity` values prevent overexposure with bright or saturated content; increase for low-saturation material.
- The filter shows all frame pixels simultaneously — use a representative frame or clip for meaningful results.
- See also `vectorscope` for a vectorscope-style display that is more common in broadcast grading workflows.
