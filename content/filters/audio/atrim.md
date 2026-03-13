+++
title = "atrim"
description = "Trim an audio stream to a specified time range or sample range, discarding everything outside it."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["trim", "editing", "time", "samples"]

[extra]
filter_type = "audio"
since = ""
see_also = ["afade", "apad", "anull"]
parameters = ["start", "end", "duration", "start_pts", "end_pts", "start_sample", "end_sample"]
cohort = 1
source_file = "libavfilter/trim.c"
+++

The `atrim` filter extracts a continuous subrange from an audio stream and drops all samples outside that range. It can be specified by wall-clock timestamps, PTS values in samples, or by absolute sample count. Use it to cut out a specific section of audio without re-encoding the container, or to chain with `asetpts` to reset timestamps after trimming.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "atrim=start=30:end=90" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | duration | — | Timestamp of the first sample to keep, in seconds (or as a time duration string). |
| end | duration | — | Timestamp of the first sample to drop (the sample immediately before this point is the last kept). |
| duration | duration | — | Maximum duration of the output. The stream ends after this many seconds even if `end` is not set. |
| start_pts | int64 | — | Start point expressed as a PTS value in samples rather than seconds. |
| end_pts | int64 | — | End point expressed as a PTS value in samples. |
| start_sample | int64 | — | Zero-based index of the first sample to include in the output. |
| end_sample | int64 | — | Zero-based index of the first sample to exclude from the output. |

## Examples

### Keep only the second minute of audio

```sh
ffmpeg -i input.mp3 -af "atrim=60:120" output.mp3
```

### Keep the first 30 seconds

```sh
ffmpeg -i input.mp3 -af "atrim=end=30" output.mp3
```

### Keep only the first 1000 samples

```sh
ffmpeg -i input.wav -af "atrim=end_sample=1000" output.wav
```

### Extract a clip and reset timestamps to start at zero

After trimming, the timestamps still reflect the original stream position. Add `asetpts` to renumber them from zero:

```sh
ffmpeg -i input.mp3 -af "atrim=start=60:end=120,asetpts=PTS-STARTPTS" clip.mp3
```

### Trim to a maximum duration of 10 seconds

```sh
ffmpeg -i input.mp3 -af "atrim=duration=10" short.mp3
```

## Notes

- `atrim` does not modify timestamps — the output samples still carry their original PTS values. Use `asetpts=PTS-STARTPTS` after trimming if downstream filters or muxers require timestamps starting at zero.
- The `start`/`end` and `start_pts`/`end_pts` options are timestamp-based and can give different results from `start_sample`/`end_sample` when timestamps are imprecise or do not start at zero.
- When multiple start or end constraints are set simultaneously, the filter keeps any sample that satisfies at least one constraint. To keep only samples matching all constraints, chain multiple `atrim` instances.
- The `type` field in the source JSON shows `video` — this is a known data artifact; `atrim` is the audio-specific trim filter (the video counterpart is `trim`).
