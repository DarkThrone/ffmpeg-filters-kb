+++
title = "alimiter"
description = "Apply a lookahead peak limiter to audio to prevent samples from exceeding a configurable ceiling."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "limiter", "mastering"]

[extra]
filter_type = "audio"
since = ""
see_also = ["acompressor", "agate"]
parameters = ["level_in", "level_out", "limit", "attack", "release", "asc", "asc_level", "level"]
cohort = 2
+++

The `alimiter` filter applies a lookahead peak limiter to audio, ensuring that no sample exceeds the configured `limit` ceiling. Unlike a compressor, a limiter has an effectively infinite ratio: any peak above the threshold is hard-limited. It includes optional auto-level control (ASC) to prevent pumping artifacts on sustained loud signals.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "alimiter=limit=0.9:attack=5:release=50" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain applied before limiting. Range: 0.015625–64. |
| level_out | double | `1.0` | Output gain applied after limiting. Range: 0.015625–64. |
| limit | double | `1.0` | Maximum output level (linear amplitude). Default 1.0 = 0 dBFS. |
| attack | double | `5.0` | Attack time in milliseconds. Range: 0.1–80. |
| release | double | `50.0` | Release time in milliseconds. Range: 1–8000. |
| asc | bool | `0` | Enable auto-level control to prevent pumping on sustained loud signals. |
| asc_level | double | `0.5` | ASC sensitivity (0–1). Lower values make ASC trigger less aggressively. |
| level | bool | `1` | Auto-level: auto-adjust gain to avoid clipping. |

## Examples

### True peak limiting at -1 dBFS

Standard mastering limiter ceiling to prevent inter-sample peaks above -1 dBFS.

```sh
ffmpeg -i input.mp3 -af "alimiter=limit=0.891:attack=5:release=50" output.mp3
```

### Combine with loudnorm for broadcast normalisation

Apply EBU R128 normalization then limit peaks.

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-16:TP=-1.5,alimiter=limit=0.891" output.mp3
```

### Brick-wall limiter with fast attack

Catch transient peaks very aggressively.

```sh
ffmpeg -i drums.wav -af "alimiter=limit=0.95:attack=0.5:release=20" output.wav
```

### Add input gain before limiting

Boost the signal then limit it to prevent clipping.

```sh
ffmpeg -i input.mp3 -af "alimiter=level_in=2:limit=1.0:attack=5:release=100" output.mp3
```

## Notes

- `limit=1.0` corresponds to 0 dBFS. For mastering, set `limit=0.891` (-1 dBFS) or `limit=0.794` (-2 dBFS) to leave headroom.
- Very short attack values (< 1 ms) can cause audible distortion on transients; 3–10 ms is a typical mastering range.
- ASC (`asc=1`) helps prevent pumping when the signal stays continuously loud for extended periods.
- The lookahead window is determined by the `attack` time: longer attack = more lookahead, smoother limiting.
