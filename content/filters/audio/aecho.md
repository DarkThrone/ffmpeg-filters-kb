+++
title = "aecho"
description = "Add echo or reverb-style reflections to an audio stream with configurable delays and decay levels."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["echo", "delay", "reverb", "effect"]

[extra]
filter_type = "audio"
since = ""
see_also = ["adelay", "afade", "acompressor"]
parameters = ["in_gain", "out_gain", "delays", "decays"]
cohort = 1
+++

The `aecho` filter simulates echoes and reflections by feeding delayed, attenuated copies of the input signal back into the output. Multiple echoes can be stacked by providing pipe-separated delay and decay lists. Use it to add depth to a voice recording, simulate outdoor environments, or create the classic "double-tracking" effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000:0.3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | float | 0.6 | Gain applied to the input signal before processing. Range: (0, 1]. |
| out_gain | float | 0.3 | Gain applied to the output signal after mixing in reflections. Range: (0, 1]. |
| delays | string | 1000 | Pipe-separated list of delay times in milliseconds for each reflection. Each value must be in the range (0, 90000]. |
| decays | string | 0.5 | Pipe-separated list of loudness factors for each reflection. Each value must be in the range (0, 1]. The number of decays must match the number of delays. |

## Examples

### Double-tracking effect (very short delay)

A 60 ms delay creates the impression of two instruments playing in unison:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.88:60:0.4" output.mp3
```

### Metallic robot effect (extremely short delay)

A 6 ms delay creates a metallic or robotic character:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.88:6:0.4" output.mp3
```

### Open-air mountain echo (single long delay)

A 1-second delay at moderate decay simulates an outdoor echo:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000:0.3" output.mp3
```

### Multiple mountain walls (two separate echoes)

Two echoes at different delays and decays simulate reflections from two surfaces:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000|1800:0.3|0.25" output.mp3
```

### Subtle room reverb (multiple short echoes)

Three rapidly decaying echoes approximate a small room:

```sh
ffmpeg -i input.mp3 -af "aecho=0.6:0.4:20|40|80:0.5|0.3|0.15" output.mp3
```

## Notes

- The sum of `in_gain` and each `decay` multiplied by `out_gain` should not exceed 1.0 to avoid clipping and feedback buildup.
- `delays` and `decays` must have the same number of pipe-separated values; mismatched counts produce an error.
- Very long delays (e.g., 10000 ms or more) allocate a correspondingly large internal buffer; keep memory constraints in mind for embedded or batch pipelines.
- This filter is purely additive — it cannot model complex reverb tails as accurately as convolution-based approaches, but it is very fast and sufficient for stylistic effects.
