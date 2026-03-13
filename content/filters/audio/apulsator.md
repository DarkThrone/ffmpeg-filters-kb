+++
title = "apulsator"
description = "Modulate stereo audio volume with an LFO (low-frequency oscillator) to create tremolo, auto-panning, or rhythmic stereo effects."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "stereo", "lfo", "tremolo", "panning"]

[extra]
filter_type = "audio"
since = ""
see_also = ["haas", "earwax", "vibrato"]
parameters = ["level_in", "level_out", "mode", "amount", "offset_l", "offset_r", "width", "timing", "bpm", "ms", "hz"]
cohort = 3
+++

The `apulsator` filter is a stereo LFO (low-frequency oscillator) effect that modulates the volume of the left and right audio channels independently. With `offset_r=0`, it acts as a tremolo (both channels pulse together). With `offset_r=0.5` (default), it acts as an auto-panner (channels alternate 180° out of phase). Intermediate offsets create sweeping, rotating stereo effects. Multiple waveform shapes are available.

## Quick Start

```sh
# Auto-panner at 2 Hz
ffmpeg -i input.wav -af "apulsator" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain (0.015625–64). |
| level_out | double | `1.0` | Output gain (0.015625–64). |
| mode | int | `sine` | LFO waveform: `sine`, `triangle`, `square`, `sawup`, `sawdown`. |
| amount | double | `1.0` | Modulation depth (0–1). |
| offset_l | double | `0.0` | Left channel LFO phase offset (0–1). |
| offset_r | double | `0.5` | Right channel LFO phase offset (0–1). Default 0.5 = auto-pan. |
| width | double | `1.0` | Pulse width (0–2). |
| timing | int | `hz` | Timing mode: `hz`, `bpm`, or `ms`. |
| hz | double | `2.0` | LFO frequency in Hz (0.01–100, when `timing=hz`). |
| bpm | double | `120.0` | LFO rate in BPM (30–300, when `timing=bpm`). |
| ms | int | `500` | LFO period in milliseconds (10–2000, when `timing=ms`). |

## Examples

### Auto-panner (default)

```sh
ffplay -i music.wav -af apulsator
```

### Tremolo effect (both channels in phase)

```sh
ffmpeg -i input.wav -af "apulsator=offset_r=0:hz=5" tremolo.wav
```

### Slow auto-pan at 120 BPM with triangle wave

```sh
ffmpeg -i input.wav -af "apulsator=mode=triangle:timing=bpm:bpm=120" output.wav
```

### Fast pulsing effect with square wave

```sh
ffplay -i music.wav -af "apulsator=mode=square:hz=8:amount=0.8"
```

## Notes

- `offset_r=0` → tremolo; `offset_r=0.5` → auto-pan; values in between → continuous panning sweep.
- `amount` sets how much the LFO modulates the signal — `1.0` = full modulation (channel can go silent at the trough); `0.5` = half modulation.
- Use `timing=bpm` when working to music tempo; `timing=ms` for precise period control.
- Combine `mode=sine:offset_r=0.5` for the smoothest auto-pan effect.
