+++
title = "deesser"
description = "Reduce sibilance ('s', 'sh', 'ch' sounds) in vocal recordings by dynamically attenuating high-frequency harsh content."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["deesser", "sibilance", "vocal", "dynamics"]

[extra]
filter_type = "audio"
since = ""
see_also = ["afftdn", "highpass"]
parameters = ["i", "m", "f", "s"]
cohort = 2
+++

The `deesser` filter reduces harsh sibilant sounds — the piercing 's', 'sh', and 'ch' consonants common in vocal recordings — by detecting and attenuating the offending high-frequency energy. Unlike a static high-shelf EQ cut, it operates dynamically, only reducing treble when sibilance is detected. The `s` option lets you monitor just the removed frequencies to dial in the settings.

## Quick Start

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| i | double | `0` | Intensity: sibilance detection sensitivity. Range: 0–1. Higher = triggers more easily. |
| m | double | `0.5` | Amount of ducking on the treble portion. Range: 0–1. 1 = maximum attenuation. |
| f | double | `0.5` | Frequency content preservation. Range: 0–1. Higher = keep more original high frequencies. |
| s | int | `o` | Output mode: `i` (pass input unchanged), `o` (pass de-essed output), `e` (pass only removed ess). |

## Examples

### Basic de-essing on a vocal

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5" output.wav
```

### Aggressive de-essing for harsh microphone

```sh
ffmpeg -i harsh_vocal.wav -af "deesser=i=0.8:m=0.8:f=0.3" output.wav
```

### Subtle de-essing (minimal impact on sound)

```sh
ffmpeg -i interview.wav -af "deesser=i=0.3:m=0.3:f=0.7" output.wav
```

### Monitor what is being removed (`e` mode)

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5:s=e" ess_only.wav
```

## Notes

- Use `s=e` (ess-only output mode) to hear exactly what frequencies are being removed — this helps dial in `i` and `m` correctly before committing.
- `i` (intensity) controls when the de-esser triggers: low values only trigger on very strong sibilance; high values are more aggressive.
- `m` (max ducking) controls the reduction depth: `0.5` is moderate; `1.0` is maximum attenuation.
- `f` preserves original high-frequency content after de-essing — higher values sound more natural but may leave some sibilance.
- For clinical de-essing, pair with a high-shelf EQ cut to further tame the top end after de-essing.
