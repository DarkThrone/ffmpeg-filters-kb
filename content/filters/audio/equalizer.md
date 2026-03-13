+++
title = "equalizer"
description = "Apply a two-pole peaking EQ biquad filter to boost or cut a specific frequency band."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["eq", "equalizer", "frequency", "biquad", "filter"]

[extra]
filter_type = "audio"
since = ""
see_also = ["highpass", "lowpass", "acompressor"]
parameters = ["frequency", "gain", "width_type", "width", "mix", "channels", "normalize", "transform", "precision", "blocksize"]
cohort = 1
source_file = "libavfilter/af_biquads.c"
+++

The `equalizer` filter implements a standard two-pole peaking EQ — the same type found in hardware mixing consoles and digital audio workstations. It boosts or cuts a band of frequencies centered on a specified frequency, with the bandwidth controlled by the `width` parameter. Multiple `equalizer` instances can be chained in a single `-af` string to build a full parametric EQ.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "equalizer=f=1000:g=5:width_type=o:width=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Center frequency of the EQ band in Hz. (alias: `f`) |
| gain | double | 0.0 | Gain in dB to apply at the center frequency. Positive values boost, negative values cut. (alias: `g`) |
| width_type | int | q | How the `width` parameter is interpreted: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 1.0 | Bandwidth of the filter, in units determined by `width_type`. (alias: `w`) |
| mix | double | 1.0 | Wet/dry blend between filtered (1.0) and original (0.0) signal. (alias: `m`) |
| channels | string | all | Comma-separated list of channel names or numbers to apply the filter to. (alias: `c`) |
| normalize | bool | false | Normalize biquad filter coefficients to preserve 0 dB gain at DC. (alias: `n`) |
| transform | int | di | IIR filter transform type: `di` (direct form I), `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |
| blocksize | int | 0 | When > 0, process audio in blocks of this size for reduced latency (power-of-two values recommended). (alias: `b`) |

## Examples

### Boost presence at 3 kHz

A +4 dB boost at 3 kHz with a one-octave bandwidth adds clarity to vocals:

```sh
ffmpeg -i input.mp3 -af "equalizer=f=3000:g=4:width_type=o:width=1" output.mp3
```

### Cut muddiness at 300 Hz

A -6 dB notch at 300 Hz removes low-mid buildup common in room recordings:

```sh
ffmpeg -i input.mp3 -af "equalizer=f=300:g=-6:width_type=o:width=1" output.mp3
```

### Three-band parametric EQ

Chain multiple equalizer filters to create a full parametric EQ:

```sh
ffmpeg -i input.mp3 \
  -af "equalizer=f=80:g=3:width_type=o:width=1,equalizer=f=1000:g=-2:width_type=q:width=1.4,equalizer=f=8000:g=4:width_type=o:width=2" \
  output.mp3
```

### Precise Q-factor notch to remove a hum

A very narrow Q removes a 50 Hz mains hum without affecting surrounding frequencies:

```sh
ffmpeg -i input.wav -af "equalizer=f=50:g=-40:width_type=q:width=10" output.wav
```

### Apply EQ to the left channel only

```sh
ffmpeg -i input.mp3 -af "equalizer=f=2000:g=3:width_type=o:width=1:channels=FL" output.mp3
```

## Notes

- The `equalizer` filter is a peaking (bell) EQ only. For shelving or high/low-cut shapes use `highpass`, `lowpass`, `highshelf`, or `lowshelf`.
- Setting `width_type=q` with a high Q value (e.g., 30+) approximates a narrow notch filter, useful for removing tonal noise.
- Multiple `equalizer` instances on the same stream are processed in series; the order matters only when bands overlap significantly.
- The `texi_section` field in the source data is empty for this filter — details above are sourced from the FFmpeg biquad filter documentation and well-known defaults.
