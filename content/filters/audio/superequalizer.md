+++
title = "superequalizer"
description = "Apply an 18-band graphic equalizer with bands spanning 65 Hz to 20 kHz, adjustable in dB per band."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "equalizer", "eq", "tone"]

[extra]
filter_type = "audio"
since = ""
see_also = ["equalizer", "highpass", "lowpass"]
parameters = ["1b", "2b", "3b", "4b", "5b", "6b", "7b", "8b", "9b", "10b", "11b", "12b", "13b", "14b", "15b", "16b", "17b", "18b"]
cohort = 3
source_file = "libavfilter/af_superequalizer.c"
+++

The `superequalizer` filter provides an 18-band graphic equalizer with fixed center frequencies spanning 65 Hz to 20 kHz. Each band gain is set in dB, defaulting to 1.0 (unity, 0 dB). It is the simplest way to apply broadband tonal shaping without the complexity of parametric EQ chains. Typical uses include voice enhancement, music frequency balancing, and correcting room acoustics.

## Quick Start

```sh
# Boost bass and reduce highs
ffmpeg -i input.wav -af "superequalizer=1b=3:2b=2:17b=0.5:18b=0.3" output.wav
```

## Parameters

| Band | Center Frequency | Band | Center Frequency |
|------|-----------------|------|-----------------|
| `1b` | 65 Hz | `10b` | 1480 Hz |
| `2b` | 92 Hz | `11b` | 2093 Hz |
| `3b` | 131 Hz | `12b` | 2960 Hz |
| `4b` | 185 Hz | `13b` | 4186 Hz |
| `5b` | 262 Hz | `14b` | 5920 Hz |
| `6b` | 370 Hz | `15b` | 8372 Hz |
| `7b` | 523 Hz | `16b` | 11840 Hz |
| `8b` | 740 Hz | `17b` | 16744 Hz |
| `9b` | 1047 Hz | `18b` | 20000 Hz |

All gains default to `1.0`. Values > 1.0 boost; values < 1.0 cut.

## Examples

### Bass boost

```sh
ffmpeg -i input.mp3 -af "superequalizer=1b=2.5:2b=2:3b=1.5" bass_boosted.mp3
```

### Voice clarity boost (presence at 2–5kHz)

```sh
ffmpeg -i voice.wav -af "superequalizer=11b=1.8:12b=2.0:13b=1.6:4b=0.7:5b=0.8" enhanced.wav
```

### Flat (default, no change)

```sh
ffmpeg -i input.wav -af superequalizer output.wav  # same as input
```

### Loudness curve (bass + treble boost, mid cut)

```sh
ffmpeg -i input.wav -af "superequalizer=1b=2:2b=1.8:3b=1.4:9b=0.8:10b=0.7:15b=1.3:16b=1.5" output.wav
```

## Notes

- Gain values are **linear** (not dB), where `1.0` = 0 dB, `2.0` ≈ +6 dB, `0.5` ≈ −6 dB.
- For parametric EQ with precise frequency, bandwidth, and gain control, use the `equalizer` filter instead.
- Combine multiple `equalizer` filter instances in a chain for more targeted shaping than `superequalizer` allows.
- Heavy boosting may cause clipping — follow with `volume` or `alimiter` if needed.
