+++
title = "arnndn"
description = "Reduce noise from speech recordings using a Recurrent Neural Network model trained specifically for voice denoising."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["denoise", "rnn", "speech", "AI", "noise-reduction"]

[extra]
filter_type = "audio"
since = ""
see_also = ["afftdn", "compand"]
parameters = ["model", "mix"]
cohort = 2
+++

The `arnndn` filter removes noise from speech audio using a Recurrent Neural Network (RNN) trained on a large corpus of speech and noise samples. Unlike `afftdn` which uses generic spectral subtraction, `arnndn` is optimized specifically for voice recordings and can cleanly separate speech from complex background noise (crowds, traffic, wind). Requires an external `.rnnn` model file.

## Quick Start

```sh
ffmpeg -i noisy_voice.wav -af "arnndn=m=/path/to/model.rnnn" clean.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| model / m | string | — | Path to the `.rnnn` model file. **Required.** |
| mix | float | `1` | Mix ratio of denoised vs. original. Range: -1 to 1. 1=full denoised, 0=original, -1=noise only. |

## Examples

### Full denoising with a model file

```sh
ffmpeg -i speech_with_noise.wav \
  -af "arnndn=m=./models/bd.rnnn" \
  clean_speech.wav
```

### Partial denoising (70% clean, 30% original)

```sh
ffmpeg -i interview.wav \
  -af "arnndn=m=./models/bd.rnnn:mix=0.7" \
  output.wav
```

### Extract removed noise only (`mix=-1`)

```sh
ffmpeg -i input.wav \
  -af "arnndn=m=./models/bd.rnnn:mix=-1" \
  noise_only.wav
```

### Chain with compand for broadcast speech

```sh
ffmpeg -i podcast.wav \
  -af "arnndn=m=./models/lq.rnnn,compand=attacks=0.1:decays=0.3:points=-70/-70|-20/-10|0/-3" \
  output.wav
```

## Notes

- Pre-trained model files are available in the `ffmpeg-rnnnoise-models` and `RNNoise` projects. Common models: `bd.rnnn` (broadband), `lq.rnnn` (low quality microphone), `mp.rnnn` (music+speech).
- `arnndn` is designed for speech — it may suppress or distort non-speech audio (music, sound effects).
- `mix=-1` outputs the removed noise, useful to verify what the model is discarding.
- The model expects 48 kHz audio; FFmpeg will automatically resample if needed, but for best results ensure input is at 48 kHz.
- For non-speech audio, `afftdn` with noise floor tracking is usually a better choice.
