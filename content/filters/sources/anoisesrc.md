+++
title = "anoisesrc"
description = "Generate a noise audio signal in various colors: white, pink, brown, blue, violet, or velvet noise."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "audio", "noise", "test"]

[extra]
filter_type = "source"
since = ""
see_also = ["sine", "aevalsrc"]
parameters = ["sample_rate", "amplitude", "duration", "color", "seed", "nb_samples", "density"]
cohort = 3
source_file = "libavfilter/asrc_anoisesrc.c"
+++

The `anoisesrc` source generates noise audio signals with selectable spectral color — white (flat spectrum), pink (−3 dB/octave), brown (−6 dB/octave), blue (+3 dB/octave), violet (+6 dB/octave), or velvet (sparse random spikes). Noise sources are used for acoustic testing, psychoacoustic masking tests, dithering reference signals, and creative audio design.

## Quick Start

```sh
# 30 seconds of pink noise
ffmpeg -f lavfi -i "anoisesrc=d=30:c=pink" pink_noise.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sample_rate / r | int | `48000` | Output sample rate in Hz. |
| amplitude / a | double | `1.0` | Amplitude (0.0–1.0). |
| duration / d | duration | infinite | Total duration. |
| color / colour / c | int | `white` | Noise color: `white`, `pink`, `brown`, `blue`, `violet`, `velvet`. |
| seed / s | int64 | random | PRNG seed for reproducible noise. |
| nb_samples / n | int | `1024` | Samples per output frame. |
| density | double | `0.05` | Density for velvet noise (0–1). |

## Examples

### White noise (flat spectrum)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=white:d=10" white_noise.wav
```

### Pink noise (most common for audio testing)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=pink:r=44100:a=0.5:d=60" pink_noise.wav
```

### Brown noise (deep rumble)

```sh
ffplay -f lavfi "anoisesrc=c=brown:r=44100"
```

### Velvet noise (sparse impulses, for reverb seeding)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=velvet:density=0.1:d=5" velvet.wav
```

### Reproducible noise (fixed seed)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=pink:seed=42:d=10" repeatable.wav
```

## Notes

- **White**: flat power spectral density — equally loud at all frequencies (sounds harsh/hissy).
- **Pink**: −3 dB/octave — equal power per octave, matching human loudness perception (most natural-sounding noise).
- **Brown** (red): −6 dB/octave — deep, rumbling noise resembling a waterfall or ocean surf.
- **Blue**: +3 dB/octave — emphasizes high frequencies; sounds thin and bright.
- **Violet**: +6 dB/octave — very high-frequency emphasis; useful for dithering.
- **Velvet**: sparse random spikes at a given density; used in reverberation algorithms and spatial audio.
