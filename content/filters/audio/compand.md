+++
title = "compand"
description = "Compress or expand the dynamic range of audio using a configurable transfer function and attack/decay times."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "compand", "compression"]

[extra]
filter_type = "audio"
since = ""
see_also = ["acompressor"]
parameters = ["attacks", "decays", "points", "soft-knee", "gain", "volume", "delay"]
cohort = 2
source_file = "libavfilter/af_compand.c"
+++

The `compand` filter performs combined compression and expansion of audio dynamic range. Unlike `acompressor`, it specifies the transfer function as a series of (input, output) level points, with separate attack and decay time constants. It can both compress loud sounds and expand (boost) quiet ones, and supports an initial volume level and a time-delayed bypass for de-noising.

## Quick Start

```sh
# Gentle compression
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=0.8:points=-80/-80|-45/-15|0/-3:gain=3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| attacks | string | `0.3` | Comma-separated attack times per channel in seconds. |
| decays | string | `0.8` | Comma-separated decay (release) times per channel in seconds. |
| points | string | — | Transfer function as `input/output` pairs in dBFS. E.g. `-70/-70\|-60/-20\|0/0`. |
| soft-knee | double | `0.01` | Softness of the knee in dB. |
| gain | double | `0.0` | Output gain in dB. |
| volume | double | `0.0` | Initial volume in dB (at startup). |
| delay | double | `0.0` | Delay in seconds before compression activates. |

## Examples

### Radio-style compression

Aggressive compression for broadcast/radio with high perceived loudness.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=0.8:points=-70/-70|-60/-20|0/-3:soft-knee=6:gain=6" output.mp3
```

### Noise gate + compression combined

Silence signals below -50 dBFS, compress everything above -20 dBFS.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.2:decays=0.5:points=-90/-900|-50/-50|-20/-15|0/-3" output.mp3
```

### Expand quiet audio (reverse compression)

Boost signals below -40 dBFS to reduce noise floor.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.05:decays=0.1:points=-80/-80|-40/-40|-10/-10|0/0:gain=4" output.mp3
```

## Notes

- `points` defines the transfer function: each `x/y` pair maps input level x dBFS to output level y dBFS. Connect at least 2 points; points must be in ascending input-level order.
- For a gate, set the output for low inputs to `-900` (silence): `points=-90/-900|-50/-50|0/0` silences everything below -50 dBFS.
- `attacks` and `decays` are in seconds (not milliseconds as in `acompressor`). Typical broadcast values: attack=0.3s, decay=0.8s.
- For a simpler ratio-based compressor, `acompressor` is easier to configure; `compand` provides more flexibility for complex multi-point transfer curves.
