+++
title = "adelay"
description = "Delay one or more audio channels by a specified amount of time or number of samples."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["delay", "timing", "channels", "sync"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aecho", "apad", "atrim"]
parameters = ["delays", "all"]
cohort = 1
source_file = "libavfilter/af_adelay.c"
+++

The `adelay` filter shifts individual audio channels in time by a specified delay, padding the beginning with silence. Each channel can have an independent delay value, making it useful for fixing inter-channel timing mismatches, implementing Haas-effect stereo widening, or compensating for microphone placement differences.

## Quick Start

```sh
ffmpeg -i input.wav -af "adelay=500|0" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delays | string | — | Pipe-separated list of delay values for each channel. Append `S` for samples, `s` for seconds, or no suffix for milliseconds. Channels without a specified delay value are left undelayed (unless `all=1`). |
| all | bool | false | When enabled, the last delay value in `delays` is applied to all remaining channels not explicitly listed. |

## Examples

### Delay the left channel by 500 ms (right channel unchanged)

```sh
ffmpeg -i stereo.wav -af "adelay=500|0" output.wav
```

### Delay three channels at different times

Delay the first channel by 1.5 seconds, skip the second (no delay), delay the third by 0.5 seconds:

```sh
ffmpeg -i multichannel.wav -af "adelay=1500|0|500" output.wav
```

### Delay by exact sample counts

Delay the second channel by 500 samples and the third by 700 samples:

```sh
ffmpeg -i input.wav -af "adelay=0|500S|700S" output.wav
```

### Apply the same delay to all channels

Using `all=1` repeats the last specified delay for every remaining channel:

```sh
ffmpeg -i input.wav -af "adelay=delays=64S:all=1" output.wav
```

### Haas effect stereo widening

A short delay of 20–40 ms on one channel creates a perceived stereo widening effect (Haas/precedence effect):

```sh
ffmpeg -i mono.mp3 -af "pan=stereo|c0=c0|c1=c0,adelay=0|30" wide_stereo.mp3
```

## Notes

- Channels with a delay of `0` (or channels for which no delay is provided when `all=0`) pass through with no modification.
- Very long delays allocate a correspondingly large silence buffer in memory; keep delays reasonable for batch or streaming workflows.
- Unlike `aecho`, `adelay` does not add any feedback or repeated reflections — it is a pure one-time time shift.
- When using the `s` (seconds) suffix, the value is a floating-point number of seconds; the `S` (samples) suffix requires an integer.
