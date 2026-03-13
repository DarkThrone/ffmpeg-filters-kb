+++
title = "silenceremove"
description = "Remove silence from the beginning, end, or middle of audio based on configurable threshold and duration settings."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["silence", "trimming", "editing", "utility"]

[extra]
filter_type = "audio"
since = ""
see_also = ["agate", "silencedetect", "compand"]
parameters = ["start_periods", "start_duration", "start_threshold", "stop_periods", "stop_duration", "stop_threshold", "detection", "window"]
cohort = 2
source_file = "libavfilter/af_silenceremove.c"
+++

The `silenceremove` filter trims silence from the beginning, end, or middle of audio. Configurable threshold and duration settings control what counts as silence. The `start_periods` parameter controls how many silence periods to skip at the start (typically 1), and `stop_periods` controls the end (negative values enable silence removal from the middle of the audio).

## Quick Start

```sh
# Remove leading and trailing silence
ffmpeg -i padded.wav -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=1:stop_threshold=-50dB" trimmed.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_periods | int | `0` | Number of silence periods to skip at start before audio begins. 0 = disabled. |
| start_duration | duration | `0` | Min non-silence duration before trimming stops at start. |
| start_threshold | double | `0` | Silence threshold for start detection. In dB (e.g. `-50dB`) or amplitude ratio. |
| start_silence | duration | `0` | How much silence to keep at start after trimming. |
| start_mode | int | `any` | Multi-channel trigger: `any` (any non-silent channel) or `all` (all channels). |
| stop_periods | int | `0` | Silence periods to skip at end. Negative = remove middle silence (repeating). |
| stop_duration | duration | `0` | Min silence duration to trigger end trimming. |
| stop_threshold | double | `0` | Silence threshold for end detection. |
| stop_silence | duration | `0` | How much silence to keep at end after trimming. |
| detection | int | `avg` | Silence detection method: `avg` (RMS average) or `peak`. |
| window | duration | `0.02` | Duration of the detection window for silence measurement. |
| timestamp | int | `write` | Timestamp mode: `write` (update) or `copy` (preserve original). |

## Examples

### Remove leading silence only

```sh
ffmpeg -i input.wav -af "silenceremove=start_periods=1:start_threshold=-60dB" output.wav
```

### Remove leading and trailing silence

```sh
ffmpeg -i padded.wav \
  -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=1:stop_duration=0.1:stop_threshold=-50dB" \
  trimmed.wav
```

### Remove silence from the middle (podcast editing)

Use negative `stop_periods` to keep stripping silent gaps.

```sh
ffmpeg -i interview.wav \
  -af "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB" \
  compact.wav
```

### Leave 0.1s of silence at start after trim

```sh
ffmpeg -i input.wav \
  -af "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1" \
  output.wav
```

## Notes

- `start_periods=1` removes silence up to and including the first non-silent period. Higher values skip N periods of silence (e.g. `2` removes the first silent section and the first audio section, then starts at the second audio).
- Negative `stop_periods` enables repeating removal of internal silence — effectively compacting the audio by removing all pauses above `stop_duration`.
- Threshold can be given in dB (`-50dB`) or amplitude ratio (`0.001`). dB format is easier to reason about for practical use.
- `detection=peak` reacts to the peak sample value; `detection=avg` uses RMS averaging for smoother behavior on transient-heavy audio.
- Always audition the result — aggressive settings can clip words or cut room tone that's needed for natural-sounding audio.
