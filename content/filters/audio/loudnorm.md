+++
title = "loudnorm"
description = "Normalize audio loudness to EBU R128 targets with optional two-pass linear mode."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["normalization", "loudness", "mastering"]

[extra]
filter_type = "audio"
since = ""
see_also = ["dynaudnorm", "acompressor", "alimiter"]
parameters = ["I", "LRA", "TP", "measured_I", "measured_LRA", "measured_TP", "measured_thresh", "offset", "linear", "dual_mono", "print_format"]
cohort = 2
source_file = "libavfilter/af_loudnorm.c"
+++

The `loudnorm` filter normalizes audio to EBU R128 loudness standards, targeting integrated loudness (LUFS), loudness range (LU), and true peak (dBTP). In single-pass mode it uses dynamic compression to hit targets in real time. In two-pass mode (`linear=true`), it first measures the file then applies a precise linear gain in the second pass — producing better quality with no dynamic processing.

## Quick Start

```sh
# Single-pass normalization to -23 LUFS (EBU R128)
ffmpeg -i input.mp3 -af "loudnorm=I=-23:TP=-1:LRA=7" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| I / i | double | `-24.0` | Integrated loudness target in LUFS (ITU-R BS.1770). Range: -70–-5. |
| LRA / lra | double | `7.0` | Loudness range target in LU. Range: 1–50. |
| TP / tp | double | `-2.0` | Maximum true peak in dBTP. Range: -9–0. |
| measured_I | double | — | Measured integrated loudness from first pass (enables linear mode). |
| measured_LRA | double | — | Measured loudness range from first pass. |
| measured_TP | double | — | Measured true peak from first pass. |
| measured_thresh | double | — | Measured threshold from first pass. |
| offset | double | `0.0` | Gain offset in LU to apply on top of normalization. |
| linear | bool | `true` | Use linear gain when first-pass measurements are provided. |
| dual_mono | bool | `false` | Treat mono content as dual-mono (applies +3 LU correction). |
| print_format | int | `none` | Output format: `none`, `json`, `summary`. Use `json` in first pass. |

## Examples

### Single-pass normalization (streaming/fast mode)

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp3
```

### Two-pass normalization (best quality)

**Pass 1** — measure the file:

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-23:TP=-2:LRA=7:print_format=json" -f null -
```

Capture the JSON output, then use the measured values in **Pass 2**:

```sh
ffmpeg -i input.mp3 -af \
  "loudnorm=I=-23:TP=-2:LRA=7:measured_I=-18.5:measured_LRA=9.2:measured_TP=-1.3:measured_thresh=-28.4:linear=true" \
  output.mp3
```

### Broadcast normalization to -23 LUFS

EBU R128 standard for broadcast.

```sh
ffmpeg -i voice.wav -af "loudnorm=I=-23:TP=-1:LRA=7" normalized.wav
```

### Streaming platform normalization (-14 LUFS)

Target for YouTube/Spotify/Apple Music.

```sh
ffmpeg -i music.mp3 -af "loudnorm=I=-14:TP=-1:LRA=11" streaming.mp3
```

## Notes

- The EBU R128 standard for broadcast is I=-23 LUFS, TP=-1 dBTP, LRA=7 LU. For online streaming, I=-14 LUFS is common.
- Single-pass (`linear=false`) uses dynamic processing (compression/limiting) which can affect transients. Two-pass linear mode preserves the original dynamics.
- `dual_mono=true` adds +3 LU to match how mono files measured in stereo containers are perceived by the R128 algorithm.
- The `print_format=json` output from pass 1 includes all measured_ values needed for pass 2. Parse the `[Parsed_loudnorm]` section of stderr.
