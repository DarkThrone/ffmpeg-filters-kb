+++
title = "tremolo"
description = "Apply a tremolo effect by modulating the amplitude of audio at a set frequency and depth."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "tremolo", "modulation"]

[extra]
filter_type = "audio"
since = ""
see_also = ["vibrato"]
parameters = ["f", "d"]
cohort = 2
+++

The `tremolo` filter applies amplitude modulation (AM) to audio, creating a regular volume pulsation. It is the classic "tremolo arm" effect used on electric guitars and organ music. Unlike `vibrato` (which modulates pitch), tremolo modulates volume — making the sound swell and recede rhythmically.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "tremolo=f=5:d=0.8" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | double | `5.0` | Tremolo frequency in Hz. Range: 0.1–20000. |
| d | double | `0.5` | Depth as a fraction 0–1. 0 = no effect, 1 = silence on each down-cycle. |

## Examples

### Classic guitar tremolo (5 Hz, moderate depth)

```sh
ffmpeg -i guitar.wav -af "tremolo=f=5:d=0.6" output.wav
```

### Slow, deep swell effect

```sh
ffmpeg -i strings.wav -af "tremolo=f=1.5:d=0.9" output.wav
```

### Fast shimmering tremolo

```sh
ffmpeg -i keys.mp3 -af "tremolo=f=10:d=0.5" output.mp3
```

### Sync to tempo (120 BPM = 2 Hz for quarter notes)

```sh
ffmpeg -i input.mp3 -af "tremolo=f=2:d=0.7" output.mp3
```

## Notes

- `f` in Hz can be synced to musical tempo: frequency = BPM / 60 / beat_division (e.g. 120 BPM quarter notes = 120/60/1 = 2 Hz).
- `d=1.0` produces complete silence at the bottom of each cycle (full amplitude modulation). `d=0.3` is subtle.
- Tremolo modulates amplitude (volume); `vibrato` modulates frequency (pitch). Both use the same `f` and `d` parameters.
- For tube-amp-style tremolo with a slight asymmetry, combine with a very subtle `aphaser`.
