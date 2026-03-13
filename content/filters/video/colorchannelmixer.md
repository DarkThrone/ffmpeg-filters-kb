+++
title = "colorchannelmixer"
description = "Adjust colors by mixing color channels using a 4×4 matrix transformation."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "grading", "color-correction"]

[extra]
filter_type = "video"
since = ""
see_also = ["curves", "colorbalance", "eq"]
parameters = ["rr", "rg", "rb", "ra", "gr", "gg", "gb", "ga", "br", "bg", "bb", "ba", "ar", "ag", "ab", "aa"]
cohort = 2
+++

The `colorchannelmixer` filter remixes the R, G, B, and A channels of video by applying a 4×4 matrix transformation. Each output channel is computed as a weighted sum of all four input channels, enabling complex color grading operations such as channel swapping, cross-processing effects, and colorspace approximations. It is one of the most flexible color manipulation tools in FFmpeg.

## Quick Start

```sh
# Classic sepia tone
ffmpeg -i input.mp4 -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rr | double | `1` | Red gain for the red output channel. |
| rg | double | `0` | Green gain for the red output channel. |
| rb | double | `0` | Blue gain for the red output channel. |
| ra | double | `0` | Alpha gain for the red output channel. |
| gr | double | `0` | Red gain for the green output channel. |
| gg | double | `1` | Green gain for the green output channel. |
| gb | double | `0` | Blue gain for the green output channel. |
| ga | double | `0` | Alpha gain for the green output channel. |
| br | double | `0` | Red gain for the blue output channel. |
| bg | double | `0` | Green gain for the blue output channel. |
| bb | double | `1` | Blue gain for the blue output channel. |
| ba | double | `0` | Alpha gain for the blue output channel. |
| ar | double | `0` | Red gain for the alpha output channel. |
| ag | double | `0` | Green gain for the alpha output channel. |
| ab | double | `0` | Blue gain for the alpha output channel. |
| aa | double | `1` | Alpha gain for the alpha output channel. |

## Examples

### Sepia tone

Classic photographic sepia by mixing channels toward warm brown tones.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" output.mp4
```

### Swap red and blue channels

Infrared-like effect by exchanging the red and blue channels.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=0:rb=1:br=1:bb=0" output.mp4
```

### Remove the red channel

Set the red output entirely to zero.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=0" output.mp4
```

### Cross-process look

Shift red toward yellow and blue toward cyan for a film cross-process effect.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=1:rg=0.1:bg=-0.1:bb=1:gg=0.9:gb=0.1" output.mp4
```

## Notes

- The parameters are listed in row-major order: first the four coefficients for the red output (rr rg rb ra), then green (gr gg gb ga), blue (br bg bb ba), alpha (ar ag ab aa).
- The identity matrix (no change) is `rr=1:gg=1:bb=1:aa=1` with all off-diagonal values at 0 (the default).
- Values outside [0, 1] are valid and can produce saturating effects, but may clip the output.
- For simpler hue/saturation adjustments, `huesaturation` or `colorbalance` may be more intuitive.
