+++
title = "sidechaingate"
description = "Apply a noise gate to audio where the gate is triggered by an external sidechain signal."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "gate", "sidechain"]

[extra]
filter_type = "audio"
since = ""
see_also = ["agate", "sidechaincompress"]
parameters = ["level_in", "mode", "range", "threshold", "ratio", "attack", "release", "makeup", "knee", "detection", "link"]
cohort = 2
source_file = "libavfilter/af_agate.c"
+++

The `sidechaingate` filter applies a noise gate controlled by an external sidechain signal rather than the input signal itself. The gate opens when the sidechain exceeds the threshold and closes when it drops below. A classic use case is keying a reverb tail — when a dry vocal drops below the threshold, the reverb send is gated off. It requires `filter_complex` with two audio inputs.

## Quick Start

```sh
# Gate the reverb (second input) based on the dry signal (first input)
ffmpeg -i reverb.mp3 -i dry_signal.mp3 \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.02:attack=10:release=200[out]" \
  -map "[out]" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before gating. Range: 0.015625–64. |
| mode | int | `downward` | Gate mode: `downward` (attenuate when sidechain is quiet) or `upward`. |
| range | double | `0.06125` | Attenuation when gate is closed. 0 = silence, 1 = passthrough. |
| threshold | double | `0.125` | Sidechain level at which the gate opens (linear amplitude). |
| ratio | double | `2.0` | Rate of attenuation below threshold. |
| attack | double | `20.0` | Time in ms for gate to open. |
| release | double | `250.0` | Time in ms for gate to close. |
| makeup | double | `1.0` | Output gain after gating. |
| knee | double | `2.828` | Soft-knee transition width in dB. |
| detection | int | `rms` | Sidechain level detection: `rms` or `peak`. |
| link | int | `average` | Multi-channel link: `average` or `maximum`. |

## Examples

### Gate reverb with dry vocal as sidechain

The reverb opens when the vocal is active, closes in the spaces between words.

```sh
ffmpeg -i reverb_return.wav -i dry_vocal.wav \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.02:attack=5:release=300:range=0[out]" \
  -map "[out]" gated_reverb.wav
```

### Duck noise floor using a reference signal

Gate background noise based on a click track or guide track.

```sh
ffmpeg -i noisy_bg.mp3 -i reference.mp3 \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.05:release=500[out]" \
  -map "[out]" output.mp3
```

### Tight sidechain gating (live performance)

Fast attack and release to gate a live instrument tightly.

```sh
ffmpeg -i guitar.wav -i pick_trigger.wav \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.1:attack=2:release=50:range=0[out]" \
  -map "[out]" output.wav
```

## Notes

- The first input (`[0:a]`) is the audio to be gated; the second (`[1:a]`) is the sidechain trigger. Only the first stream appears in the output.
- `threshold` uses linear amplitude. For dBFS: `linear = 10^(dBFS/20)`. A threshold of 0.02 ≈ -34 dBFS.
- `range=0` completely silences the gated stream when closed. `range=0.06` (default) gives ~-24 dB attenuation.
- For gating triggered by the signal itself, use the simpler `agate` filter.
