+++
title = "sine"
description = "Generate a pure sine wave audio signal at a configurable frequency, with an optional periodic beep."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "audio", "test", "tone"]

[extra]
filter_type = "source"
since = ""
see_also = ["anoisesrc", "aevalsrc"]
parameters = ["frequency", "beep_factor", "sample_rate", "duration", "samples_per_frame"]
cohort = 3
+++

The `sine` source generates a bit-exact sine wave audio signal at a specified frequency. It is the standard way to produce a test tone in FFmpeg — commonly used as a 1 kHz calibration tone in broadcast leaders, or as a reference signal for audio testing. An optional periodic beep at a harmonic frequency can also be enabled.

## Quick Start

```sh
# 1 kHz test tone for 10 seconds
ffmpeg -f lavfi -i "sine=frequency=1000:duration=10" tone_1khz.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency / f | double | `440` | Carrier frequency in Hz. |
| beep_factor / b | double | `0` | Periodic beep at `frequency × beep_factor` Hz (0 = disabled). |
| sample_rate / r | int | `44100` | Output sample rate in Hz. |
| duration / d | duration | infinite | Total duration. |
| samples_per_frame | expression | `1024` | Samples per output frame. |

## Examples

### 1 kHz broadcast test tone

```sh
ffmpeg -f lavfi -i "sine=frequency=1000:sample_rate=48000" -t 60 tone.wav
```

### 440 Hz concert A with beep every second at 880 Hz

```sh
ffplay -f lavfi "sine=frequency=440:beep_factor=2"
```

### 220 Hz with 880 Hz beep, 5 second duration

```sh
ffmpeg -f lavfi -i "sine=f=220:b=4:d=5" sine_test.wav
```

### Pair with SMPTE bars for a broadcast leader

```sh
ffmpeg -f lavfi -i "smptehdbars=size=1920x1080:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 60 broadcast_leader.mxf
```

## Notes

- The output amplitude is fixed at 1/8 (approximately -18 dBFS) — a standard reference level for broadcast.
- `beep_factor=2` gives a beep at double the carrier frequency (one octave up); `beep_factor=4` gives two octaves up.
- Specify `sample_rate=48000` for broadcast work (48 kHz is the professional audio standard).
- The signal is bit-exact — the same settings will always produce identical samples.
