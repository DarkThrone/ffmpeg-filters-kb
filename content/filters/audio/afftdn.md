+++
title = "afftdn"
description = "Denoise audio using FFT-based spectral subtraction, supporting white, vinyl, shellac, and custom noise profiles."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["denoise", "noise-reduction", "fft", "restoration"]

[extra]
filter_type = "audio"
since = ""
see_also = ["arnndn", "compand", "afir"]
parameters = ["noise_reduction", "noise_floor", "noise_type", "band_noise", "track_noise", "output_mode"]
cohort = 2
+++

The `afftdn` filter removes noise from audio using FFT-based spectral subtraction. It models the noise floor spectrum and subtracts it from each frame. It supports several built-in noise type profiles (white, vinyl, shellac) and a custom 15-band profile. The noise floor can be tracked automatically over time for varying noise conditions, making it effective for tape hiss, vinyl crackle, and microphone self-noise reduction.

## Quick Start

```sh
ffmpeg -i noisy.wav -af "afftdn=nr=10:nf=-40" clean.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise_reduction / nr | float | `12` | Noise reduction amount in dB. Range: 0.01–97. |
| noise_floor / nf | float | `-50` | Noise floor in dB. Range: -80 to -20. |
| noise_type / nt | int | `white` | Noise model: `white` (w), `vinyl` (v), `shellac` (s), `custom` (c). |
| band_noise / bn | string | — | Custom 15-band noise profile (space or `\|` separated dB values). |
| residual_floor / rf | float | `-38` | Residual floor in dB after reduction. Range: -80 to -20. |
| track_noise / tn | bool | `0` | Auto-track and adapt the noise floor over time. |
| track_residual / tr | bool | `0` | Auto-track the residual floor. |
| output_mode / om | int | `output` | Output: `input` (passthrough), `output` (denoised), `noise` (only removed noise). |
| adaptivity / ad | float | `0.5` | Gain adaptation speed (0=instant, 1=very slow). |
| gain_smooth / gs | int | `0` | Smooth gain across frequency bins to reduce musical noise. Range: 0–50. |

## Examples

### Remove white noise (microphone self-noise)

```sh
ffmpeg -i mic.wav -af "afftdn=nr=10:nf=-40" clean.wav
```

### Vinyl noise reduction

```sh
ffmpeg -i vinyl.wav -af "afftdn=nt=vinyl:nr=15:nf=-50" clean.wav
```

### Enable noise floor tracking for variable noise

```sh
ffmpeg -i recording.wav -af "afftdn=nr=12:nf=-50:tn=1" output.wav
```

### Monitor what is being removed

```sh
ffmpeg -i noisy.wav -af "afftdn=nr=10:nf=-40:om=noise" noise_only.wav
```

### Reduce musical noise artifacts with gain smoothing

```sh
ffmpeg -i input.wav -af "afftdn=nr=12:nf=-40:gs=10" output.wav
```

## Notes

- Start with conservative settings (`nr=10:nf=-40`) and increase only if noise remains. Excessive reduction causes artifacts ("musical noise").
- `track_noise=1` continuously adapts the noise floor model — useful for recordings with changing background noise.
- `output_mode=noise` lets you hear exactly what is being removed, which helps tune `nr` and `nf` parameters.
- `gain_smooth` reduces the "musical noise" artifact (random tonal remnants) at the cost of some resolution.
- For speech-specific denoising, `arnndn` uses a trained neural network and often produces better results on voice material.
