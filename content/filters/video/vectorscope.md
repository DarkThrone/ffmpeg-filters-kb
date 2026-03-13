+++
title = "vectorscope"
description = "Display a 2D color vectorscope showing the distribution of chroma values, used for broadcast color QC and calibration."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["analysis", "vectorscope", "broadcast", "color"]

[extra]
filter_type = "video"
since = ""
see_also = ["waveform", "histogram", "signalstats"]
parameters = ["mode", "x", "y", "intensity", "envelope", "graticule", "opacity", "bgopacity", "colorspace"]
cohort = 2
+++

The `vectorscope` filter generates a 2D plot of two color components against each other — typically Cb vs. Cr (U vs. V) — creating the classic vectorscope display used in broadcast video production. It reveals color saturation, hue accuracy, and whether colors fall within legal broadcast gamut. Multiple visualization modes provide different ways to inspect the color distribution.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "vectorscope" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode / m | int | `gray` | Display mode: `gray`, `tint`, `color`, `color2`, `color3`, `color4`, `color5`. |
| x | int | `1` | Color component for X axis (0=Y, 1=U/Cb, 2=V/Cr, 3=A). |
| y | int | `2` | Color component for Y axis. |
| intensity / i | float | `0.004` | Brightness of plotted points (used in gray/color/color3/color5 modes). |
| envelope / e | int | `none` | Envelope: `none`, `instant`, `peak`, `peak+instant`. |
| graticule / g | int | `none` | Graticule overlay: `none`, `green`, `color`, `invert`. |
| opacity / o | float | `0.75` | Graticule opacity. |
| bgopacity / b | float | `0.3` | Background opacity. |
| colorspace / c | int | `auto` | Colorspace for graticule targets: `auto`, `601`, `709`. |
| lthreshold / l | float | `0.0` | Low threshold for the 3rd component (ignored below this). |
| hthreshold / h | float | `1.0` | High threshold for the 3rd component (ignored above this). |

## Examples

### Standard Cb/Cr vectorscope

```sh
ffmpeg -i input.mp4 -vf "vectorscope" output.mp4
```

### With color graticule targets (BT.709)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=graticule=color:colorspace=709:opacity=0.9" output.mp4
```

### Show actual pixel colors (color2 mode)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=mode=color2" output.mp4
```

### Peak envelope (hold max saturation)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=envelope=peak" output.mp4
```

### Display alongside original video

```sh
ffmpeg -i input.mp4 -vf "[in]split[a][b];[a]vectorscope[vs];[b][vs]hstack" output.mp4
```

## Notes

- Default X=1 (U/Cb) and Y=2 (V/Cr) gives the standard vectorscope view — dots at center = neutral, saturated colors appear farther from center.
- `graticule=color` overlays the standard broadcast target boxes for primary and secondary colors; dots outside these boxes indicate out-of-gamut chroma.
- `colorspace=709` draws Rec.709 targets (HDTV); `colorspace=601` draws Rec.601 targets (SDTV).
- Use alongside `waveform` for complete broadcast QC: waveform checks luma levels, vectorscope checks chroma.
- `lthreshold`/`hthreshold` filter which pixels contribute based on the 3rd component (luma by default), useful for isolating highlights or shadows.
