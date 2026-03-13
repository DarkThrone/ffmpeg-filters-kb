+++
title = "acontrast"
description = "Apply audio contrast enhancement (dynamic range compression/expansion) to make quiet parts louder and loud parts more distinct."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "dynamics", "contrast", "compression"]

[extra]
filter_type = "audio"
since = ""
see_also = ["compand", "alimiter", "loudnorm"]
parameters = ["contrast"]
cohort = 3
source_file = "libavfilter/af_acontrast.c"
+++

The `acontrast` filter applies simple audio contrast enhancement — an automatic gain adjustment that increases the dynamic contrast between loud and quiet passages. It is similar in concept to a waveform shaper: at high `contrast` values it effectively clips and re-shapes the waveform to make audio subjectively louder and more aggressive. It is a quick, single-parameter alternative to a full compander chain.

## Quick Start

```sh
ffmpeg -i input.wav -af "acontrast=contrast=50" enhanced.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| contrast | float | `33.0` | Contrast amount (0–100). Higher values increase aggressiveness. |

## Examples

### Default contrast (moderate enhancement)

```sh
ffmpeg -i quiet.wav -af acontrast louder.wav
```

### Aggressive enhancement (adds "loudness war" style compression)

```sh
ffmpeg -i music.wav -af "acontrast=contrast=80" aggressive.wav
```

### Subtle enhancement for voice clarity

```sh
ffmpeg -i podcast.wav -af "acontrast=contrast=20" podcast_enhanced.wav
```

### Zero contrast (no-op)

```sh
ffmpeg -i input.wav -af "acontrast=contrast=0" output.wav
```

## Notes

- `contrast=0` is a pass-through (no effect); `contrast=100` is maximum enhancement and can introduce distortion.
- At high values, `acontrast` is equivalent to soft clipping/limiting — the waveform is re-shaped, not just amplified.
- For broadcast-standard loudness normalization, use `loudnorm` or `ebur128` instead of `acontrast`.
- Compare with `compand` or `acompressor` for more nuanced dynamics control.
