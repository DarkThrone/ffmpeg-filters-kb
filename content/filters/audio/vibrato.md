+++
title = "vibrato"
description = "Apply a vibrato effect by modulating the frequency (pitch) of audio at a set rate and depth."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "vibrato", "modulation"]

[extra]
filter_type = "audio"
since = ""
see_also = ["tremolo"]
parameters = ["f", "d"]
cohort = 2
+++

The `vibrato` filter applies frequency modulation (FM) to audio, creating a regular pitch oscillation — the same effect used by singers and instrumentalists when they apply vibrato. Unlike `tremolo` (which modulates amplitude/volume), vibrato modulates pitch. The `f` parameter sets how fast the pitch oscillates, and `d` controls how wide the pitch swings.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "vibrato=f=5:d=0.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | double | `5.0` | Vibrato frequency in Hz. Range: 0.1–20000. Typical musical range: 4–8 Hz. |
| d | double | `0.5` | Depth as a fraction 0–1. Controls the pitch swing width. |

## Examples

### Classic vocal vibrato

```sh
ffmpeg -i vocal.wav -af "vibrato=f=5.5:d=0.5" output.wav
```

### Deep, slow string-instrument vibrato

```sh
ffmpeg -i violin.wav -af "vibrato=f=3.5:d=0.7" output.wav
```

### Fast, shallow guitar vibrato

```sh
ffmpeg -i guitar.wav -af "vibrato=f=7:d=0.3" output.wav
```

### Extreme pitch wobble effect

```sh
ffmpeg -i input.mp3 -af "vibrato=f=8:d=1.0" output.mp3
```

## Notes

- `f` in Hz corresponds to the vibrato rate: 4–6 Hz is typical for vocal vibrato, 5–8 Hz for string instruments.
- `d=0.5` is a moderate depth; `d=1.0` is very wide pitch swing (almost a wobble/whammy effect); `d=0.2` is subtle.
- Vibrato modulates pitch (frequency); `tremolo` modulates volume (amplitude). Both use the same parameter names and ranges.
- For tempo-synced vibrato, calculate `f = BPM / 60 / beat_division` (e.g. 8th-note vibrato at 120 BPM = 4 Hz).
