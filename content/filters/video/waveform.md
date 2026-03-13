+++
title = "waveform"
description = "Generate a video waveform monitor overlay for analyzing luma and chroma levels."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["analysis", "waveform", "broadcast"]

[extra]
filter_type = "video"
since = ""
see_also = ["vectorscope", "histogram"]
parameters = ["mode", "intensity", "mirror", "display", "components", "envelope", "filter", "graticule", "opacity", "flags", "bgopacity"]
cohort = 2
+++

The `waveform` filter generates a video waveform monitor — a tool used in professional video production to analyze the luminance and chrominance levels of a video signal. The waveform shows the distribution of pixel values across each scanline, making it easy to spot clipping, crushing, or color casts. It outputs the waveform overlaid on or beside the video.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "waveform" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode / m | int | `row` | Waveform orientation: `row` (horizontal) or `column` (vertical). |
| intensity / i | float | `0.04` | Intensity of each plotted point (0.0–1.0). |
| mirror / r | bool | `1` | Mirror the waveform display. |
| display / d | int | `stack` | Output layout: `stack` (waveform below video), `parade` (side by side), `overlay` (waveform over video). |
| components / c | int | `1` | Which components to show. Bitmask: 1=Y, 2=Cb, 4=Cr, 7=all. |
| envelope / e | int | `none` | Envelope mode: `none`, `instant`, `peak`, `peak+instant`. |
| filter / f | int | `lowpass` | Filter type: `lowpass`, `flat`, `aflat`, `chroma`, `color`, `acolor`. |
| graticule / g | int | `none` | Graticule overlay: `none`, `green`, `orange`, `invert`. |
| opacity / o | float | `0.75` | Opacity of the graticule. |
| bgopacity / b | float | `0.75` | Background opacity. |
| flags / fl | flags | `0` | Flags: `torchlight` (show all planes at once). |

## Examples

### Standard luma waveform

```sh
ffmpeg -i input.mp4 -vf "waveform" output.mp4
```

### Parade mode (all three components side by side)

```sh
ffmpeg -i input.mp4 -vf "waveform=display=parade:components=7" output.mp4
```

### Overlay waveform on video

```sh
ffmpeg -i input.mp4 -vf "waveform=display=overlay:intensity=0.1" output.mp4
```

### Graticule with green markers

```sh
ffmpeg -i input.mp4 -vf "waveform=graticule=green:opacity=0.9" output.mp4
```

## Notes

- In `row` mode, each vertical column of the waveform corresponds to the same horizontal position in the video, making it easy to identify left-right color casts.
- `parade` mode displays Y, Cb, and Cr side by side — very useful for identifying white balance and color casts simultaneously.
- Legal broadcast levels are typically 16–235 (luma) and 16–240 (chroma) for 8-bit video. The waveform makes clipping immediately visible.
- For chroma analysis, `vectorscope` is more useful than waveform; use both together for complete broadcast QC.
