+++
title = "highpass"
description = "Apply a high-pass biquad filter to attenuate frequencies below a specified cutoff frequency."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["filter", "eq", "highpass", "frequency", "biquad"]

[extra]
filter_type = "audio"
since = ""
see_also = ["lowpass", "equalizer", "highshelf"]
parameters = ["frequency", "width_type", "width", "poles", "mix", "channels", "normalize", "transform", "precision"]
cohort = 1
source_file = "libavfilter/af_biquads.c"
+++

The `highpass` filter attenuates frequencies below its cutoff (the 3 dB point) and passes frequencies above it largely unchanged. It is implemented as a biquad IIR filter and supports both single-pole (6 dB/octave) and two-pole (12 dB/octave) configurations. Common uses include removing low-frequency rumble, wind noise, or DC offset from recordings.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "highpass=f=200" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Cutoff frequency in Hz — the -3 dB point. (alias: `f`) |
| width_type | int | q | Interpretation of the `width` parameter: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 0.707 | Bandwidth or resonance of the filter, in units set by `width_type`. Only meaningful when `poles=2`. (alias: `w`) |
| poles | int | 2 | Number of filter poles. `1` gives a gentle 6 dB/octave roll-off; `2` gives a steeper 12 dB/octave roll-off. (alias: `p`) |
| mix | double | 1.0 | Wet/dry blend: 1.0 is fully filtered, 0.0 is the original signal. (alias: `m`) |
| channels | string | all | Channels to filter, e.g., `FL|FR`. (alias: `c`) |
| normalize | bool | false | Normalize filter coefficients so the passband gain is 0 dB. (alias: `n`) |
| transform | int | di | IIR transform type: `di`, `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |

## Examples

### Remove low-frequency rumble from a recording

A 100 Hz highpass is a standard rumble filter for voice and instrument recordings:

```sh
ffmpeg -i input.wav -af "highpass=f=100" output.wav
```

### Remove wind noise from a field recording

Wind noise typically concentrates below 200 Hz:

```sh
ffmpeg -i outdoor.mp3 -af "highpass=f=200" output.mp3
```

### Gentle single-pole roll-off

A single pole provides a subtle 6 dB/octave slope suitable for thinning a bass-heavy mix:

```sh
ffmpeg -i input.mp3 -af "highpass=f=150:poles=1" output.mp3
```

### Telephone or radio effect (combined with lowpass)

Bandpass a voice track to simulate a telephone by combining a highpass and lowpass:

```sh
ffmpeg -i voice.mp3 -af "highpass=f=300,lowpass=f=3400" telephone.mp3
```

### Apply only to the center channel in a 5.1 stream

```sh
ffmpeg -i surround.mp4 -af "highpass=f=80:channels=FC" output.mp4
```

## Notes

- The default two-pole configuration rolls off at 12 dB/octave below the cutoff. For a steeper slope, chain multiple `highpass` filters.
- The `width_type=q` default uses a Q of 0.707 (Butterworth response), which gives a maximally flat passband with no resonance peak. Higher Q values add resonance near the cutoff.
- This filter shares its implementation (`af_biquads.c`) with `lowpass`, `equalizer`, `highshelf`, `lowshelf`, and other biquad filters.
- The `texi_section` field in the source data is empty for this filter; parameters and defaults are sourced from the shared biquad implementation.
