+++
title = "vibrance"
description = "Boost or reduce the saturation of muted colors while protecting already-saturated colors."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "saturation", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["huesaturation", "colorbalance"]
parameters = ["intensity", "rbal", "gbal", "bbal", "rlum", "glum", "blum", "alternate"]
cohort = 2
source_file = "libavfilter/vf_vibrance.c"
+++

The `vibrance` filter boosts or reduces saturation of muted (less saturated) colors more than already-saturated colors, similar to the Vibrance slider in Adobe Lightroom. This preserves naturally saturated elements like skin tones while making dull colours pop. Negative values reduce vibrance, pushing the image toward more muted or monochromatic tones.

## Quick Start

```sh
# Boost vibrance without over-saturating skin tones
ffmpeg -i input.mp4 -vf "vibrance=intensity=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| intensity | float | `0.0` | Vibrance intensity. Range: -2–2. Positive=more vibrant, negative=less. |
| rbal | float | `1.0` | Red balance adjustment. |
| gbal | float | `1.0` | Green balance adjustment. |
| bbal | float | `1.0` | Blue balance adjustment. |
| rlum | float | `0.072` | Red luminance coefficient. |
| glum | float | `0.715` | Green luminance coefficient. |
| blum | float | `0.213` | Blue luminance coefficient. |
| alternate | bool | `0` | Use an alternate vibrance calculation method. |

## Examples

### Subtle vibrance boost for landscape

```sh
ffmpeg -i landscape.mp4 -vf "vibrance=intensity=0.5" output.mp4
```

### Strong vibrance for colourful content

```sh
ffmpeg -i product.mp4 -vf "vibrance=intensity=1.2" output.mp4
```

### Reduce vibrance for muted, filmic look

```sh
ffmpeg -i input.mp4 -vf "vibrance=intensity=-0.5" output.mp4
```

### Combine with hue rotation

```sh
ffmpeg -i input.mp4 -vf "huesaturation=hue=10,vibrance=intensity=0.6" output.mp4
```

## Notes

- `vibrance` differs from `saturation` in that it targets muted colors preferentially. Full saturation (`huesaturation=saturation=1`) boosts all colors equally and can cause skin tones to go orange.
- `intensity=0` is a no-op passthrough; the practical range for normal adjustments is -0.8 to 1.5.
- The `rbal`/`gbal`/`bbal` parameters fine-tune per-channel vibrance balance; leave at defaults unless correcting specific colour channel biases.
- For a complete colour workflow, use `vibrance` after any global exposure/white-balance corrections and before any creative grading.
