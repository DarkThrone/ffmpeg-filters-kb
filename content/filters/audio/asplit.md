+++
title = "asplit"
description = "Split an audio stream into two or more identical copies for parallel processing in a filter graph."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["split", "routing", "filter", "graph"]

[extra]
filter_type = "audio"
since = ""
see_also = ["amix", "anull", "aformat"]
parameters = ["outputs"]
cohort = 1
source_file = "libavfilter/split.c"
+++

The `asplit` filter duplicates an audio stream into multiple identical output streams. Each output is an independent copy of the input that can be routed to a different branch of a filter graph. Use it whenever you need to apply different processing chains to the same audio source, or when you want to mix a processed version back with the original (parallel processing).

## Quick Start

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]asplit=2[a1][a2]" -map "[a1]" out1.mp3 -map "[a2]" out2.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outputs | int | 2 | Number of output streams to produce. All outputs are identical copies of the input. |

## Examples

### Split into two outputs and apply different EQ to each

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]asplit=2[a1][a2]; \
    [a1]highpass=f=200[high]; \
    [a2]lowpass=f=500[low]" \
  -map "[high]" high.mp3 \
  -map "[low]" low.mp3
```

### Parallel compression: blend dry and compressed signals

```sh
ffmpeg -i drums.wav \
  -filter_complex "[0:a]asplit=2[dry][wet]; \
    [wet]acompressor=threshold=0.1:ratio=8:makeup=4[comp]; \
    [dry][comp]amix=inputs=2:weights='0.5 0.5'[out]" \
  -map "[out]" parallel_comp.wav
```

### Split into three branches for simultaneous encoding

```sh
ffmpeg -i input.flac \
  -filter_complex "[0:a]asplit=3[a1][a2][a3]" \
  -map "[a1]" -c:a aac out_aac.m4a \
  -map "[a2]" -c:a mp3 out_mp3.mp3 \
  -map "[a3]" -c:a flac out_flac.flac
```

### Preview and save simultaneously

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]asplit=2[play][save]" \
  -map "[play]" -f alsa default \
  -map "[save]" saved.mp3
```

## Notes

- Each output of `asplit` is a full copy of the input data. Memory usage scales linearly with the number of outputs; use only as many as you need.
- The source JSON lists `asplit` with `type = "video"` and description "Pass on the input to N video outputs" — this is a known data artifact from the shared `split.c` implementation. `asplit` is the audio-specific variant; the video counterpart is `split`.
- For two outputs, `asplit` and `asplit=2` are equivalent.
- `asplit` is a pure routing primitive with no signal processing and no latency.
