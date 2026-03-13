+++
title = "freezedetect"
description = "Detect frozen (static) video segments by comparing consecutive frames, logging start time, duration, and end time as metadata."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "detection", "freeze"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["blackframe", "silencedetect", "scdet"]
parameters = ["noise", "duration"]
cohort = 3
+++

The `freezedetect` filter identifies frozen video — segments where consecutive frames show no significant change — and logs the start, duration, and end of each freeze event. It is used in broadcast playout monitoring to catch encoder stalls, dropped feeds, or slate/bug errors. The video stream passes through unchanged; detections are logged to stderr and attached as frame metadata.

## Quick Start

```sh
# Detect freeze events (default: 2 seconds, -60dB noise tolerance)
ffmpeg -i input.mp4 -vf freezedetect -f null - 2>&1 | grep freeze
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise / n | double | `-60dB` | Noise tolerance — max mean absolute difference between frames considered frozen. Can be in dB (e.g., `-50dB`) or ratio (e.g., `0.001`). |
| duration / d | duration | `2s` | Minimum duration of a static segment before it is reported as a freeze. |

## Examples

### Default freeze detection

```sh
ffmpeg -i broadcast.ts -vf freezedetect -f null - 2>&1 | grep freeze
```

### Detect short freezes (500ms) with relaxed noise tolerance

```sh
ffmpeg -i input.mp4 -vf "freezedetect=n=-50dB:d=0.5" -f null -
```

### Log freeze events to file

```sh
ffmpeg -i input.mp4 -vf freezedetect -f null - 2>&1 | grep freezedetect > freezes.txt
```

### Monitor a live stream in real time

```sh
ffmpeg -i rtsp://camera/stream -vf "freezedetect=d=3" -f null -
```

## Notes

- Metadata keys set: `lavfi.freezedetect.freeze_start` (on first frozen frame at or after `d`), `lavfi.freezedetect.freeze_duration` and `lavfi.freezedetect.freeze_end` (on first frame after the freeze).
- The noise threshold accounts for encoder quantization noise — a perfectly frozen H.264 stream may still produce small inter-frame differences due to bitstream artifacts.
- Combine with `silencedetect` for full A/V dropout detection in broadcast QC pipelines.
