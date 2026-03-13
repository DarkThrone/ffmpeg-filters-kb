+++
title = "agate"
description = "Apply a noise gate to audio, attenuating signals that fall below a configurable threshold."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "gate", "noise"]

[extra]
filter_type = "audio"
since = ""
see_also = ["sidechaingate", "acompressor"]
parameters = ["level_in", "mode", "range", "threshold", "ratio", "attack", "release", "makeup", "knee", "detection", "link", "level_sc"]
cohort = 2
source_file = "libavfilter/af_agate.c"
+++

The `agate` filter applies a noise gate that attenuates (closes) when the signal level drops below the `threshold`, and opens when the level rises above it. It is commonly used to suppress background noise, room tone, or microphone hiss between speech passages. For gating triggered by an external sidechain signal, see `sidechaingate`.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "agate=threshold=0.02:attack=10:release=200" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before gating. Range: 0.015625–64. |
| mode | int | `downward` | Gate mode: `downward` (attenuate below threshold) or `upward` (attenuate above threshold). |
| range | double | `0.06125` | Attenuation when gate is closed (linear). 0 = silence, 1 = passthrough. |
| threshold | double | `0.125` | Level at which the gate opens (linear amplitude). |
| ratio | double | `2.0` | Rate of attenuation below the threshold. Higher = harder gate. |
| attack | double | `20.0` | Time in ms for the gate to open after signal exceeds threshold. |
| release | double | `250.0` | Time in ms for the gate to close after signal drops below threshold. |
| makeup | double | `1.0` | Output gain applied after gating. |
| knee | double | `2.828` | Width in dB of soft-knee transition around the threshold. |
| detection | int | `rms` | Level detection: `rms` or `peak`. |
| link | int | `average` | Multi-channel link: `average` or `maximum`. |
| level_sc | double | `1.0` | Sidechain input gain (used when operating as sidechain). |

## Examples

### Remove microphone noise between speech

```sh
ffmpeg -i interview.mp3 -af "agate=threshold=0.015:attack=20:release=500:range=0.01" output.mp3
```

### Drum gate — cut bleed between hits

Tight gate with fast release to isolate drum hits.

```sh
ffmpeg -i drums.wav -af "agate=threshold=0.05:attack=5:release=80:range=0" output.wav
```

### Gentle noise floor reduction

Reduce (but not silence) background noise.

```sh
ffmpeg -i recording.mp3 -af "agate=threshold=0.02:range=0.1:attack=50:release=1000" output.mp3
```

## Notes

- `threshold` uses linear amplitude. For dBFS conversion: `linear = 10^(dBFS/20)`. For example, -30 dBFS ≈ 0.0316.
- `range=0` completely silences the gated signal; `range=0.06125` (the default) gives about -24 dB of attenuation.
- `attack` and `release` are in milliseconds. Long release values prevent chattering (rapid open/close) on reverb tails.
- For gating triggered by a second audio stream (e.g. gate the music when the voice is active), use `sidechaingate`.
