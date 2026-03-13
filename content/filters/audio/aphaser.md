+++
title = "aphaser"
description = "Apply a phasing effect to audio using an all-pass filter chain modulated by an LFO."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "phaser", "modulation"]

[extra]
filter_type = "audio"
since = ""
see_also = ["flanger", "chorus"]
parameters = ["in_gain", "out_gain", "delay", "decay", "speed", "type"]
cohort = 2
+++

The `aphaser` filter applies a phaser effect by passing audio through a chain of all-pass filters whose cutoff frequencies are modulated by a low-frequency oscillator (LFO). This creates the characteristic sweeping notches in the frequency spectrum associated with phaser pedals. Unlike a flanger, a phaser does not use a delay line — it produces a smoother, more subtle effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "aphaser=in_gain=0.4:speed=0.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | double | `0.4` | Input gain. Range: 0–1. |
| out_gain | double | `0.74` | Output gain. Range: 0–1. |
| delay | double | `3.0` | Delay in milliseconds (initial phase shift). Range: 0–5. |
| decay | double | `0.4` | Feedback decay — controls intensity. Range: 0–0.99. |
| speed | double | `0.5` | LFO modulation speed in Hz. Range: 0.1–2. |
| type | int | `triangular` | LFO waveform: `triangular` or `sinusoidal`. |

## Examples

### Classic slow phaser

```sh
ffmpeg -i guitar.wav -af "aphaser=in_gain=0.4:decay=0.4:speed=0.3" output.wav
```

### Fast, intense phaser

```sh
ffmpeg -i synth.mp3 -af "aphaser=decay=0.8:speed=1.5:type=sinusoidal" output.mp3
```

### Subtle vocal phaser

```sh
ffmpeg -i vocal.wav -af "aphaser=in_gain=0.6:decay=0.3:speed=0.4" output.wav
```

### Deep sweeping phaser

```sh
ffmpeg -i bass.wav -af "aphaser=delay=5:decay=0.7:speed=0.2" output.wav
```

## Notes

- `decay` is the most significant quality knob: higher values (>0.7) produce intense resonant sweeps; lower values (0.2–0.4) are subtle.
- `speed` controls how fast the LFO sweeps. For tempo-locked effects, calculate `speed = BPM/60 / beat_division`.
- Phaser is more subtle than flanger because it uses all-pass filters rather than a physical delay line — it changes phase without adding a distinct echo.
- `out_gain` may need to be reduced if `decay` is high, as strong resonance can boost the signal level.
