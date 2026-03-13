+++
title = "atempo"
description = "Adjust audio playback speed without changing pitch, using a time-stretching algorithm."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["tempo", "speed", "time-stretch", "pitch"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aresample", "atrim", "afade"]
parameters = ["tempo"]
cohort = 1
source_file = "libavfilter/af_atempo.c"
+++

The `atempo` filter changes the playback speed of audio — making it faster or slower — without altering the pitch. It accepts a tempo scale factor where 1.0 is the original speed, values below 1.0 slow it down, and values above 1.0 speed it up. The supported range per instance is 0.5–100.0. For ratios outside the range 0.5–2.0, FFmpeg skips some samples instead of blending them; to avoid artifacts for large changes, chain multiple `atempo` instances whose product equals the desired ratio.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "atempo=1.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tempo | double | 1.0 | Playback speed multiplier. Range: 0.5–100.0. Values below 1.0 slow down, values above 1.0 speed up. |

## Examples

### Slow down audio to 80% speed

```sh
ffmpeg -i input.mp3 -af "atempo=0.8" slow.mp3
```

### Speed up audio to 150% (1.5×)

```sh
ffmpeg -i input.mp3 -af "atempo=1.5" fast.mp3
```

### Speed up to 300% by chaining two instances

For ratios above 2.0, chaining two filters whose product equals the target avoids sample-skipping artifacts:

```sh
ffmpeg -i input.mp3 -af "atempo=sqrt(3),atempo=sqrt(3)" output.mp3
```

### Speed up to 400% using two 2.0× steps

```sh
ffmpeg -i input.mp3 -af "atempo=2.0,atempo=2.0" output.mp3
```

### Slow down to 25% by chaining two 0.5× steps

```sh
ffmpeg -i input.mp3 -af "atempo=0.5,atempo=0.5" output.mp3
```

## Notes

- The `tempo` parameter supports AVExpr expressions such as `sqrt(3)`, which is useful when chaining filters to achieve an exact combined ratio.
- For tempo values in the range 0.5–2.0, the filter uses a phase vocoder-style time-stretching algorithm. Outside this range (2.0–100.0), some samples are skipped rather than blended, which can introduce noticeable artifacts on musical content — chain multiple instances to stay within the blending range.
- The minimum supported value per instance is 0.5 (half speed). Values below 0.5 or above 100.0 will produce an error.
- `atempo` changes duration but not pitch. To change pitch without changing duration, use the `asetrate` filter followed by `aresample`.
- The `tempo` value can be updated at runtime using the `sendcmd` filter, which allows dynamic speed changes without re-encoding.
