+++
title = "flanger"
description = "Apply a flanging effect to audio using a short modulated delay line."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "flanger", "modulation"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aphaser", "chorus"]
parameters = ["delay", "depth", "regen", "width", "speed", "shape", "phase", "interp"]
cohort = 2
+++

The `flanger` filter applies a flanging effect by mixing the original signal with a slightly delayed copy whose delay time is swept back and forth by a low-frequency oscillator. This creates a characteristic jet-engine or comb-filter sweep sound. It is similar to phasing but uses a physical delay line, producing a more pronounced and metallic-sounding effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "flanger" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delay | double | `0.0` | Base delay in milliseconds. Range: 0–30. |
| depth | double | `2.0` | Swept delay range in milliseconds. Range: 0–10. |
| regen | double | `0.0` | Feedback percentage (regeneration). Range: -95–95. |
| width | double | `71.0` | Percentage of delayed signal mixed with original. Range: 0–100. |
| speed | double | `0.5` | LFO sweep rate in Hz. Range: 0.1–10. |
| shape | int | `sinusoidal` | LFO waveform: `triangular` or `sinusoidal`. |
| phase | double | `25.0` | Stereo phase difference 0–100 (%). Range: 0–100. |
| interp | int | `linear` | Interpolation for delay: `linear` or `quadratic`. |

## Examples

### Classic flanger

```sh
ffmpeg -i input.mp3 -af "flanger=delay=0:depth=2:regen=0:speed=0.5" output.mp3
```

### Fast jet-plane flanger

```sh
ffmpeg -i guitar.wav -af "flanger=speed=2:depth=4:regen=30" output.wav
```

### Stereo flanger with phase offset

```sh
ffmpeg -i input.mp3 -af "flanger=phase=50:speed=0.5:depth=2" output.mp3
```

### Negative feedback (hollow, metallic sound)

```sh
ffmpeg -i synth.mp3 -af "flanger=regen=-60:depth=3:speed=0.3" output.mp3
```

## Notes

- `regen` (feedback) is the primary control for intensity. Positive feedback creates resonant peaks; negative feedback creates notches. Values above ±70 can be very extreme.
- `depth` sets the range of delay sweep; larger values create a wider, more obvious sweep.
- Unlike `aphaser` (all-pass filters), flanger uses an actual delay line, which produces a stronger, more obvious effect — particularly on high-frequency content.
- `phase` controls the L/R stereo phase offset of the LFO; 90° creates a swirling stereo effect.
