+++
title = "acrusher"
description = "Reduce audio bit depth to create lo-fi, digital distortion effects, with optional LFO modulation and logarithmic mode."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "distortion", "lo-fi", "bit-crush"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aformat", "volume"]
parameters = ["level_in", "level_out", "bits", "mix", "mode", "dc", "aa", "samples", "lfo", "lforange", "lforate"]
cohort = 2
+++

The `acrusher` filter simulates the effect of reducing audio bit depth, creating the harsh, quantization-distorted sound characteristic of early digital audio, lo-fi electronics, and video game music. Unlike simply changing the bit depth, it produces the *perceptual* effect while keeping the actual sample depth unchanged. It supports linear and logarithmic quantization, anti-aliasing, DC offset, and optional LFO modulation for dynamic bit-crushing effects.

## Quick Start

```sh
# 8-bit lo-fi effect
ffmpeg -i input.mp3 -af "acrusher=bits=8:mode=lin" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1` | Input gain. |
| level_out | double | `1` | Output gain. |
| bits | double | `8` | Target bit depth. Lower = harsher distortion. |
| mix | double | `0.5` | Blend between crushed and clean signal. |
| mode | int | `lin` | Quantization mode: `lin` (linear) or `log` (logarithmic). |
| dc | double | `1` | DC offset — asymmetric crushing of positive/negative halves. |
| aa | double | `0.5` | Anti-aliasing factor. Higher = smoother, less harsh. |
| samples | double | `1` | Sample rate reduction factor (>1 reduces effective sample rate). |
| lfo | bool | `0` | Enable LFO modulation of bit depth. |
| lforange | double | `20` | LFO modulation depth (in bits). |
| lforate | double | `0.3` | LFO rate in Hz. |

## Examples

### Classic 8-bit game audio

```sh
ffmpeg -i music.wav -af "acrusher=bits=8:mode=lin:aa=0.3" retro.wav
```

### Very lo-fi 4-bit effect

```sh
ffmpeg -i input.wav -af "acrusher=bits=4:mix=0.8" lofi.wav
```

### Logarithmic mode (more natural sounding)

```sh
ffmpeg -i input.wav -af "acrusher=bits=8:mode=log" output.wav
```

### Wobble effect with LFO

```sh
ffmpeg -i input.mp3 -af "acrusher=bits=12:lfo=1:lforange=8:lforate=2" wobble.mp3
```

### Sample rate reduction (adds aliasing)

```sh
ffmpeg -i input.wav -af "acrusher=bits=16:samples=4:aa=0" telephone.wav
```

## Notes

- `mode=log` produces a more "natural" lo-fi sound because human hearing is logarithmic; `lin` gives a harsher, more digital sound.
- `aa` (anti-aliasing) softens the harsh aliasing noise at the cost of some fidelity. `aa=0` gives maximum harshness.
- `samples` reduces the effective sample rate by only updating the output every N samples, adding gritty aliasing artifacts.
- `lfo=1` with moderate `lforange` and `lforate` creates a rhythmic wobbling bit-crush, useful for electronic music effects.
- `mix` blends the effect — `0` = clean original, `1` = fully crushed. Use intermediate values for parallel compression-style blending.
