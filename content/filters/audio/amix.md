+++
title = "amix"
description = "Mix multiple audio input streams into a single output stream."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["mixing", "audio", "multichannel", "gain"]

[extra]
filter_type = "audio"
since = ""
see_also = ["amerge", "pan", "volume"]
parameters = ["inputs", "duration", "dropout_transition", "weights", "normalize"]
cohort = 1
+++

The `amix` filter combines two or more audio streams into one by summing their samples. It supports per-input weighting, automatic volume normalization to prevent clipping, and configurable end-of-stream behavior. Use it to overlay background music with dialogue, combine multiple microphone inputs, or blend any set of audio sources.

## Quick Start

```sh
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex "amix=inputs=2:duration=first" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | 2 | Number of input audio streams to mix. |
| duration | int | longest | How to determine the end of the output stream: `longest` (continue until the longest input ends), `shortest` (stop when the shortest input ends), `first` (stop when the first input ends). |
| dropout_transition | float | 2.0 | Transition time in seconds for volume re-normalization when an input stream ends. |
| weights | string | "1 1 ..." | Space-separated weight for each input stream. The last specified weight is repeated for any remaining inputs. |
| normalize | bool | true | When enabled, inputs are scaled so the total gain stays at unity. Disable with caution — unweighted summation can clip. |

## Examples

### Mix three audio streams, ending when the first ends

```sh
ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 \
  -filter_complex "amix=inputs=3:duration=first:dropout_transition=3" \
  output.mp3
```

### Mix vocals and background music with music at 25% volume

`normalize=0` preserves the explicit weight ratios without automatic re-scaling:

```sh
ffmpeg -i vocals.mp3 -i music.mp3 \
  -filter_complex "amix=inputs=2:duration=longest:dropout_transition=0:weights='1 0.25':normalize=0" \
  output.mp3
```

### Mix two stereo streams in a video pipeline

```sh
ffmpeg -i video.mp4 -i commentary.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy output.mp4
```

### Mix four radio channels and keep the longest

```sh
ffmpeg -i ch1.mp3 -i ch2.mp3 -i ch3.mp3 -i ch4.mp3 \
  -filter_complex "amix=inputs=4:duration=longest" \
  mixed.mp3
```

### Equal mix with a 5-second dropout transition

When one input ends, the remaining inputs are smoothly re-normalized over 5 seconds:

```sh
ffmpeg -i intro.mp3 -i loop.mp3 \
  -filter_complex "amix=inputs=2:duration=longest:dropout_transition=5" \
  output.mp3
```

## Notes

- `amix` only supports float samples internally. Integer-format inputs are automatically converted via `aresample`; if you need integer output, consider `amerge` instead.
- When `normalize=1` (the default), the volume of each input is scaled by `1/n_active_inputs`, which avoids clipping but also reduces loudness when all streams are active. Use `weights` to compensate.
- The `weights` and `normalize` options can be changed at runtime using the `sendcmd` filter.
- For lossless channel merging (e.g., combining separate mono tracks into a stereo file), `amerge` is more appropriate than `amix`.
