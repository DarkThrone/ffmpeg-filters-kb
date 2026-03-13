+++
title = "aevalsrc"
description = "Generate audio samples from a mathematical expression, allowing arbitrary waveform synthesis using FFmpeg's expression engine."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "audio", "synthesis", "expression"]

[extra]
filter_type = "source"
since = ""
see_also = ["sine", "anoisesrc"]
parameters = ["exprs", "channel_layout", "sample_rate", "duration", "nb_samples"]
cohort = 3
source_file = "libavfilter/aeval.c"
+++

The `aevalsrc` source generates audio by evaluating a mathematical expression for each sample. It supports multi-channel output with separate expressions per channel, and provides access to sample time (`t`), sample number (`n`), and sample rate (`s`) in the expression. This is the most flexible audio source — any waveform that can be expressed mathematically can be generated.

## Quick Start

```sh
# 440 Hz sine wave
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t)" -t 5 output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exprs | string | — | `\|`-separated expressions, one per channel. **Required.** |
| channel_layout / c | string | (auto) | Output channel layout (e.g. `stereo`, `5.1`). |
| sample_rate / s | string | `44100` | Sample rate in Hz. |
| duration / d | duration | infinite | Total duration. |
| nb_samples / n | int | `1024` | Samples per output frame. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Sample number (starts at 0) |
| `t` | Time in seconds |
| `s` | Sample rate |

## Examples

### Simple 440 Hz sine wave

```sh
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t):s=48000" -t 5 sine.wav
```

### Stereo with different frequencies per channel

```sh
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t)|sin(550*2*PI*t):c=stereo:s=44100" -t 5 stereo.wav
```

### Amplitude-modulated signal

```sh
ffplay -f lavfi "aevalsrc=sin(10*2*PI*t)*sin(880*2*PI*t):s=44100"
```

### White noise from random()

```sh
ffmpeg -f lavfi -i "aevalsrc=-2+random(0)" -t 5 whitenoise.wav
```

### 2.5 Hz binaural beats on a 360 Hz carrier

```sh
ffmpeg -f lavfi -i "aevalsrc=0.1*sin(2*PI*(360-1.25)*t)|0.1*sin(2*PI*(360+1.25)*t):c=stereo" -t 30 binaural.wav
```

### Silence

```sh
ffmpeg -f lavfi -i "aevalsrc=0" -t 5 silence.wav
```

## Notes

- Multiple channels are separated by `|` in the `exprs` string; `channel_layout` must match the number of expressions.
- Use `sin()`, `cos()`, `random()`, `floor()`, `mod()` and any FFmpeg math functions in expressions.
- `random(n)` returns a random value in [-1, 1] from PRNG seed `n` — useful for deterministic noise.
- For simple sine tones, `sine` source is simpler; `aevalsrc` is for custom/complex waveforms.
