+++
title = "lowpass"
description = "Apply a low-pass biquad filter to attenuate frequencies above a specified cutoff frequency."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["filter", "eq", "lowpass", "frequency", "biquad"]

[extra]
filter_type = "audio"
since = ""
see_also = ["highpass", "equalizer", "lowshelf"]
parameters = ["frequency", "width_type", "width", "poles", "mix", "channels", "normalize", "transform", "precision"]
cohort = 1
source_file = "libavfilter/af_biquads.c"
+++

The `lowpass` filter attenuates frequencies above its cutoff (the 3 dB point) and passes lower frequencies unchanged. Like `highpass`, it uses a biquad IIR design and supports one or two poles. Common uses include anti-aliasing before downsampling, removing high-frequency noise or hiss, and creating a warm or muffled sound effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "lowpass=f=3000" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Cutoff frequency in Hz — the -3 dB point. (alias: `f`) |
| width_type | int | q | Interpretation of the `width` parameter: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 0.707 | Bandwidth or resonance of the filter, in units set by `width_type`. Only meaningful when `poles=2`. (alias: `w`) |
| poles | int | 2 | Number of filter poles. `1` gives a 6 dB/octave roll-off; `2` gives a 12 dB/octave roll-off. (alias: `p`) |
| mix | double | 1.0 | Wet/dry blend: 1.0 is fully filtered, 0.0 is the original signal. (alias: `m`) |
| channels | string | all | Channels to filter, e.g., `FL|FR`. (alias: `c`) |
| normalize | bool | false | Normalize filter coefficients so the passband gain is 0 dB. (alias: `n`) |
| transform | int | di | IIR transform type: `di`, `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |

## Examples

### Remove high-frequency hiss

An 8 kHz cutoff reduces tape hiss and high-frequency noise while preserving most speech intelligibility:

```sh
ffmpeg -i noisy.wav -af "lowpass=f=8000" output.wav
```

### Telephone or radio bandpass (with highpass)

Combine `highpass` and `lowpass` to simulate a narrow telephony bandwidth:

```sh
ffmpeg -i voice.mp3 -af "highpass=f=300,lowpass=f=3400" telephone.mp3
```

### Warm up a harsh recording

A gentle 10 kHz cutoff rolls off harshness while keeping the sound natural:

```sh
ffmpeg -i guitar.mp3 -af "lowpass=f=10000:poles=1" warm.mp3
```

### Anti-aliasing before downsampling

Apply a low-pass before reducing the sample rate to avoid aliasing artifacts (FFmpeg often does this automatically via `aresample`, but explicit control is sometimes needed):

```sh
ffmpeg -i input_48k.flac -af "lowpass=f=20000,aresample=44100" output_44k.flac
```

### Partial mix for parallel processing

Blend 70% filtered with 30% dry signal to preserve some high-frequency detail:

```sh
ffmpeg -i input.mp3 -af "lowpass=f=5000:mix=0.7" output.mp3
```

## Notes

- The default two-pole (12 dB/octave) Butterworth response is the most common choice for transparent roll-off. Use `poles=1` for a subtler 6 dB/octave effect.
- Chain multiple `lowpass` instances to achieve steeper slopes (e.g., two two-pole filters in series give 24 dB/octave).
- This filter shares its implementation with `highpass` and the other biquad filters in `af_biquads.c`.
- The `texi_section` field in the source data is empty for this filter; parameters and defaults are sourced from the shared biquad implementation.
