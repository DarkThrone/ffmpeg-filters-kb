+++
title = "ebur128"
description = "Measure loudness according to the EBU R128 / ITU-R BS.1770 standard, logging momentary, short-term, and integrated loudness with optional real-time video output."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "audio", "loudness", "broadcast"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["volumedetect", "replaygain", "loudnorm"]
parameters = ["video", "size", "meter", "framelog", "metadata", "peak", "dualmono", "panlaw", "target", "gauge", "scale"]
cohort = 3
source_file = "libavfilter/f_ebur128.c"
+++

The `ebur128` filter implements the EBU R128 / ITU-R BS.1770 loudness scanner. It measures Momentary loudness (M, 400 ms window), Short-term loudness (S, 3 s window), Integrated loudness (I, gated over the whole programme), and Loudness Range (LRA). The audio passes through unchanged; statistics are logged to stderr and optionally injected into frame metadata. With `video=1`, a real-time graphing display is produced as a video output stream.

## Quick Start

```sh
# Measure loudness of a file and print summary to stderr
ffmpeg -i input.wav -af ebur128 -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| video | bool | `0` | Output a real-time loudness graph as a video stream. |
| size | image_size | `640x480` | Size of the video output (only used when `video=1`). |
| meter | int | `9` | EBU scale meter: `9` (±9 LU) or `18` (±18 LU). |
| metadata | bool | `0` | Inject per-100ms loudness values as frame metadata (`lavfi.r128.*`). |
| framelog | int | `info` | Logging level: `quiet`, `info`, `verbose`. |
| peak | flags | `none` | Enable `sample` and/or `true` peak measurement. |
| dualmono | bool | `0` | Treat mono input as dual-mono (adds 3 LU to account for equal-loudness of dual mono). |
| panlaw | double | `-3.0103` | Pan law for dual-mono (dB). |
| target | int | `-23` | Target loudness in LUFS; shifts the green ±1 LU zone in the video display. |
| gauge | int | `momentary` | Gauge type: `momentary` or `shortterm`. |
| scale | int | `absolute` | Scale display: `absolute` (LUFS) or `relative` (LU). |

## Examples

### Measure integrated loudness (broadcast compliance check)

```sh
ffmpeg -i input.mp4 -af ebur128=peak=true -f null -
```

### Real-time loudness graph alongside video

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:a]ebur128=video=1:size=640x480[vid][aud]" \
  -map "[vid]" -map "[aud]" -map 0:v \
  -c:v libx264 output.mp4
```

### Inject metadata for downstream processing

```sh
ffmpeg -i input.wav -af ebur128=metadata=1 -f null -
```

### Check true peak and sample peak

```sh
ffmpeg -i input.wav -af ebur128=peak=sample+true -f null - 2>&1 | grep -E "I:|TPK:|SPK:"
```

## Notes

- The EBU R128 broadcast target is **−23 LUFS** (integrated) with a max true peak of −1 dBTP.
- `true` peak mode requires an over-sampled analysis and a build with `libswresample` — it is more accurate than sample peak.
- The filter outputs `lavfi.r128.I`, `lavfi.r128.M`, `lavfi.r128.S`, `lavfi.r128.LRA` as frame metadata when `metadata=1`.
- Use `loudnorm` (also EBU R128) to actually normalize loudness; `ebur128` only measures.
