+++
title = "colortemperature"
description = "Adjust the color temperature of video by shifting toward warm (low K) or cool (high K) tones."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "white-balance", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["colorbalance"]
parameters = ["temperature", "mix", "pl"]
cohort = 2
+++

The `colortemperature` filter adjusts the white balance of a video by simulating the effect of different color temperatures of light. Lower Kelvin values (2000–4000K) produce warm amber/orange tones (like candlelight or tungsten), while higher values (7000–10000K) produce cool blue tones (like a cloudy sky). It is useful for correcting footage shot under the wrong white balance preset.

## Quick Start

```sh
# Warm up footage to 3200K (tungsten warmth)
ffmpeg -i input.mp4 -vf "colortemperature=temperature=3200" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| temperature | float | `6500.0` | Color temperature in Kelvin. Range: 1000–40000. Lower=warmer, higher=cooler. |
| mix | float | `1.0` | Blend between original (0) and fully adjusted (1). Range: 0–1. |
| pl | float | `0.0` | Preserve luminance: 0 = allow luminance shift, 1 = preserve original luminance. |

## Examples

### Correct cool daylight footage to neutral 6500K

```sh
ffmpeg -i cool_footage.mp4 -vf "colortemperature=temperature=6500" output.mp4
```

### Warm up to 3200K (golden hour / tungsten look)

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=3200:mix=1" warm.mp4
```

### Cool down to 8000K (overcast / moonlight)

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=8000" cool.mp4
```

### 50% blend for subtle warm grade

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=4000:mix=0.5" subtle_warm.mp4
```

## Notes

- 6500K is approximately "daylight"; 5500K is slightly warm (afternoon sun); 3200K is tungsten (very warm orange).
- `mix=1.0` applies the full effect; lower values allow gradual adjustment or blending between corrected and original.
- `pl=1.0` prevents the filter from changing the overall brightness of the image while shifting color temperature.
- For fine-tuning skin tones without changing the entire frame, combine with `huesaturation=colors=r`.
