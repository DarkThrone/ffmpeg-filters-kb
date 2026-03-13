+++
title = "silencedetect"
description = "Detect silent segments in audio by reporting start time, duration, and end time whenever audio falls below a noise threshold for a minimum duration."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "audio", "silence", "detection"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["silenceremove", "freezedetect", "volumedetect"]
parameters = ["noise", "duration", "mono"]
cohort = 3
+++

The `silencedetect` filter monitors audio level and logs an event when the signal stays below a configurable noise floor for at least a minimum duration. It sets `lavfi.silence_start`, `lavfi.silence_duration`, and `lavfi.silence_end` frame metadata, and prints to stderr. It is used to find gaps in recordings, split audio at silence, or quality-check broadcast playout. The audio passes through unchanged.

## Quick Start

```sh
# Detect silences longer than 1 second
ffmpeg -i input.wav -af "silencedetect=d=1" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise / n | double | `-60dB` | Noise floor. Can be dB (e.g., `-50dB`) or amplitude ratio (e.g., `0.001`). |
| duration / d | duration | `2s` | Minimum silence duration before reporting. |
| mono / m | bool | `0` | When enabled, analyze each channel independently (adds `.X` suffix to metadata keys). |

## Examples

### Detect 2-second silences (default)

```sh
ffmpeg -i podcast.mp3 -af silencedetect -f null - 2>&1 | grep silence
```

### Detect short pauses (500ms, relaxed noise floor)

```sh
ffmpeg -i interview.wav -af "silencedetect=n=-50dB:d=0.5" -f null -
```

### Per-channel silence detection (stereo)

```sh
ffmpeg -i stereo.wav -af "silencedetect=mono=1" -f null - 2>&1 | grep silence
```

### Extract silence timestamps for use as chapter markers

```sh
ffmpeg -i long_recording.wav -af silencedetect -f null - 2>&1 | \
  grep silence_end | awk '{print $5}' > chapter_times.txt
```

## Notes

- Metadata keys: `lavfi.silence_start` is set on the first frame at or after the minimum duration; `lavfi.silence_end` and `lavfi.silence_duration` are set on the first non-silent frame after.
- With `mono=1`, keys are suffixed `.0`, `.1`, etc. per channel — useful for detecting dropout on one channel only.
- To actually remove silence rather than just detect it, use the `silenceremove` filter.
- The noise floor default of −60 dB is quite tight; for recordings with floor noise or hum, use −50 dB or higher.
