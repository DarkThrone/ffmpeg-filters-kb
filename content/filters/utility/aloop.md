+++
title = "aloop"
description = "Loop a segment of audio samples a specified number of times or infinitely."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "audio", "loop", "timing"]

[extra]
filter_type = "utility"
since = ""
see_also = ["loop", "areverse", "asetpts"]
parameters = ["loop", "size", "start", "time"]
cohort = 3
+++

The `aloop` filter repeats a segment of audio samples N times, buffering a configurable number of samples and replaying them in sequence. It is the audio counterpart to the `loop` video filter and uses the same parameter semantics with samples instead of frames. Common uses include creating seamless music loops, extending short clips, and generating ambient sound loops.

## Quick Start

```sh
# Loop 44100 samples (1 second at 44.1kHz) 5 times
ffmpeg -i input.wav -af "aloop=loop=5:size=44100" looped.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| loop | int | `0` | Number of loop iterations. `0` = no looping; `-1` = infinite. |
| size | int64 | `0` | Maximum number of samples to buffer for the loop segment. |
| start | int64 | `0` | Sample number where the loop segment starts. |
| time | duration | — | Loop start time (used instead of `start` when `start=-1`). |

## Examples

### Loop 2 seconds of audio 4 times (at 44.1kHz)

```sh
ffmpeg -i music.wav -af "aloop=loop=4:size=88200" extended.wav
```

### Infinite loop for ambient sound

```sh
ffmpeg -i ambient.flac -af "aloop=loop=-1:size=220500" -t 3600 hour_loop.wav
```

### Loop from 10 seconds in

```sh
ffmpeg -i music.mp3 -af "aloop=loop=3:size=48000:start=-1:time=10" output.wav
```

## Notes

- `size` in samples = seconds × sample_rate (e.g., 2 seconds at 48kHz = 96000).
- Unlike perfect audio loops that require sample-accurate trimming, `aloop` will create a glitch at the loop point unless the audio was already prepared for seamless looping.
- For infinite looping livestreams, combine with `-stream_loop -1` at the input level instead of `aloop` for more efficient memory use.
