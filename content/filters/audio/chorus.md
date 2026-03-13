+++
title = "chorus"
description = "Add a chorus effect to audio by mixing the signal with delayed, pitch-modulated copies."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["effects", "chorus", "modulation"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aphaser", "flanger"]
parameters = ["in_gain", "out_gain", "delays", "decays", "speeds", "depths"]
cohort = 2
+++

The `chorus` filter adds a chorus effect by mixing the original signal with one or more delayed and pitch-modulated copies. The pitch modulation is achieved by oscillating the delay time, simulating the slight timing and pitch variations that occur when multiple voices or instruments play in unison. Each chorus "voice" is defined by a set of delay, decay, speed, and depth values.

## Quick Start

```sh
# Single-voice chorus
ffmpeg -i input.mp3 -af "chorus=in_gain=0.5:out_gain=0.9:delays=50:decays=0.8:speeds=0.5:depths=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | float | `0.4` | Input gain applied before the chorus effect. Range: 0–1. |
| out_gain | float | `0.4` | Output gain. Range: 0–1. |
| delays | string | — | Pipe-separated list of delay times in milliseconds per voice (e.g. `55\|60`). |
| decays | string | — | Pipe-separated list of decay (feedback) values per voice (e.g. `0.4\|0.4`). Range per voice: 0–1. |
| speeds | string | — | Pipe-separated list of LFO speeds in Hz per voice (e.g. `0.25\|0.5`). |
| depths | string | — | Pipe-separated list of depth (modulation amount) in milliseconds per voice. |

## Examples

### Subtle single-voice chorus

```sh
ffmpeg -i vocal.mp3 -af "chorus=in_gain=0.5:out_gain=0.9:delays=50:decays=0.8:speeds=0.5:depths=2" output.mp3
```

### Two-voice chorus for guitar

```sh
ffmpeg -i guitar.wav -af "chorus=in_gain=0.6:out_gain=0.9:delays=55|60:decays=0.4|0.4:speeds=0.25|0.5:depths=2|3" output.wav
```

### Rich three-voice vocal doubling

```sh
ffmpeg -i vocal.mp3 -af "chorus=0.5:0.9:50|60|40:0.8|0.7|0.8:0.5|0.3|0.7:2|2.5|1.5" output.mp3
```

### Slow deep chorus for strings

```sh
ffmpeg -i strings.wav -af "chorus=in_gain=0.4:out_gain=0.8:delays=70:decays=0.6:speeds=0.2:depths=4" output.wav
```

## Notes

- Each pipe-separated set (delays, decays, speeds, depths) must have the same number of elements — one per chorus voice.
- `delays` sets the base delay (in ms) around which the LFO oscillates. Typical values: 20–80 ms.
- `depths` sets the maximum additional delay from the LFO (also in ms). Higher values = more obvious pitch wobble.
- `in_gain` and `out_gain` together control the output level — reduce both if the output clips.
