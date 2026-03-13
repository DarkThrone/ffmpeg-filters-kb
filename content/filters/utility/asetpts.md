+++
title = "asetpts"
description = "Recompute the presentation timestamps of audio frames using a configurable expression, mirroring the setpts filter for audio streams."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "audio", "timing", "pts", "speed"]

[extra]
filter_type = "utility"
since = ""
see_also = ["setpts", "atempo", "aresample"]
parameters = ["expr"]
cohort = 3
+++

The `asetpts` filter recomputes PTS values for audio frames using a mathematical expression — the audio equivalent of the `setpts` video filter. It is used to generate synthetic timestamps, fix desync, or adjust audio timing. For speed changes, `atempo` is usually better (it resamples to preserve pitch), but `asetpts` gives direct PTS control for cases where timing surgery is needed.

## Quick Start

```sh
# Reset audio PTS to start from zero (after atrim)
ffmpeg -i input.mp4 -af "atrim=start=10,asetpts=PTS-STARTPTS" trimmed.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string | `PTS` | Expression evaluated per frame to compute output PTS. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | Current input PTS. |
| `N` | Cumulative number of consumed samples (not including current frame). |
| `NB_SAMPLES` / `S` | Number of samples in the current frame. |
| `SAMPLE_RATE` / `SR` | Audio sample rate. |
| `TB` | Timebase of input. |
| `STARTPTS` | PTS of the first frame. |
| `T` | Time in seconds of current frame. |

## Examples

### Reset timestamps after trim

```sh
ffmpeg -i input.wav -af "atrim=start=5,asetpts=PTS-STARTPTS" trimmed.wav
```

### Generate timestamps from sample count (most accurate)

```sh
ffmpeg -i input.wav -af "asetpts=N/SR/TB" resampled.wav
```

### Fix broken audio timestamps

```sh
ffmpeg -i broken.mp4 -af "asetpts=N/SR/TB" fixed.mp4
```

### Add a 2-second audio delay

```sh
ffmpeg -i input.wav -af "asetpts=PTS+2/TB" delayed.wav
```

## Notes

- `asetpts=PTS-STARTPTS` is the standard fix after `atrim` to reset audio to start at time 0.
- `N/SR/TB` generates PTS purely from sample counting — the most robust approach when input timestamps are unreliable.
- For actual playback speed change, use `atempo` (pitch-corrected) instead of `asetpts`.
- `asetpts` and `setpts` can be used together to keep audio/video in sync after timeline manipulation.
