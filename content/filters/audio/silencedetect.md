+++
title = "silencedetect"
description = "Detect silent intervals in an audio stream and emit timing metadata for each silence period."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["silence", "detection", "metadata", "analysis"]

[extra]
filter_type = "audio"
since = ""
see_also = ["apad", "atrim", "dynaudnorm"]
parameters = ["noise", "duration", "mono"]
cohort = 1
+++

The `silencedetect` filter analyzes an audio stream and logs a message and metadata whenever the signal level stays at or below a noise threshold for a minimum specified duration. The audio is passed through unmodified. The metadata keys it emits can be used by downstream filters (such as `ametadata`) to cut, split, or annotate the stream at silence boundaries.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise | double | -60dB (0.001) | Noise floor threshold. Frames at or below this level are considered silent. Accepts a linear amplitude value or a dB string (e.g., `-50dB`). (alias: `n`) |
| duration | duration | 2.0 | Minimum duration of silence in seconds before a silence event is reported. (alias: `d`) |
| mono | bool | false | When enabled, each channel is evaluated independently and separate metadata keys with a `.X` suffix are emitted per channel. (alias: `m`) |

## Metadata Output

The filter writes the following metadata keys to the frame that marks the end of a silence period (or when using `mono=1`, per-channel variants with a `.X` suffix):

| Key | Description |
|-----|-------------|
| `lavfi.silence_start` | Timestamp (in seconds) of the first frame of the silence period. |
| `lavfi.silence_end` | Timestamp of the first frame after the silence ends. |
| `lavfi.silence_duration` | Duration of the silence period in seconds. |

## Examples

### Detect silences longer than 0.5 seconds at -50 dB

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5" -f null -
```

### Detect silences with a very low noise tolerance (near-digital silence)

```sh
ffmpeg -i silence.mp3 -af "silencedetect=noise=0.0001" -f null -
```

### Log all silence intervals to a text file

Redirect FFmpeg's log output to capture the silence timestamps:

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-40dB:d=1" -f null - 2>&1 | grep silence
```

### Detect silence per channel separately

```sh
ffmpeg -i stereo.wav -af "silencedetect=n=-50dB:d=0.3:mono=1" -f null -
```

### Use metadata to split on silence boundaries

Combine with `ametadata` and `asegment` for practical audio splitting:

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5,ametadata=print:file=silence_log.txt" -f null -
```

## Notes

- The filter passes audio through unchanged — it is a pure analysis filter and does not remove or modify samples.
- The noise threshold default of -60 dB (`0.001` linear) is suitable for most recordings. For very quiet sources or high-resolution audio, consider lowering it to `-70dB` or `-80dB`.
- The `duration` parameter controls the minimum silence length reported; very short values (below 0.1 s) may generate many false positives from breath sounds or room tone.
- When `mono=1`, silence in any single channel does not trigger the combined event — each channel is tracked independently with `.X`-suffixed metadata keys (e.g., `lavfi.silence_start.0`, `lavfi.silence_start.1`).
