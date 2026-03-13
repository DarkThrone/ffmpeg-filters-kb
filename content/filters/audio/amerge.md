+++
title = "amerge"
description = "Merge two or more audio streams into a single multi-channel stream by concatenating their channels."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["mixing", "multichannel", "channels", "merge"]

[extra]
filter_type = "audio"
since = ""
see_also = ["amix", "pan", "aformat"]
parameters = ["inputs", "layout_mode"]
cohort = 1
source_file = "libavfilter/af_amerge.c"
+++

The `amerge` filter combines multiple audio streams into one multi-channel stream by placing all channels from each input stream side-by-side. Unlike `amix`, which sums the samples of multiple streams together, `amerge` preserves each channel independently. It is the correct tool for assembling a multi-channel file from separate mono or stereo sources.

## Quick Start

```sh
ffmpeg -i left.wav -i right.wav -filter_complex "[0:a][1:a]amerge=inputs=2" -ac 2 stereo.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | 2 | Number of input audio streams to merge. |
| layout_mode | int | legacy | How to determine the output channel layout: `legacy` (reorder channels when layouts are compatible and disjoint), `reset` (ignore input layouts, output channels in stream order), `normal` (preserve channel names without reordering). |

## Examples

### Merge two mono files into a stereo stream

Using the `amovie` source to reference files and then merging:

```sh
ffmpeg -i left.wav -i right.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2,pan=stereo|c0=c0|c1=c1" \
  stereo.wav
```

### Merge six separate audio tracks from an MKV into a single 5.1 stream

```sh
ffmpeg -i input.mkv \
  -filter_complex "[0:1][0:2][0:3][0:4][0:5][0:6]amerge=inputs=6" \
  -c:a pcm_s16le output.mkv
```

### Merge a mono vocal with a stereo music track into a 3-channel stream

```sh
ffmpeg -i vocal_mono.wav -i music_stereo.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2[out]" \
  -map "[out]" -c:a flac three_channel.flac
```

### Use reset mode to avoid unexpected channel reordering

```sh
ffmpeg -i stream1.wav -i stream2.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2:layout_mode=reset" \
  merged.wav
```

## Notes

- All inputs to `amerge` must have the same sample rate and sample format; mismatched inputs will cause an error. Insert `aresample` or `aformat` before `amerge` if needed.
- If inputs have different durations, the output stops at the end of the shortest input.
- In `legacy` mode, when input channel layouts are disjoint and known (e.g., 2.1 + FC+BL+BR = 5.1), channels are reordered to conform to the standard layout. This can produce unexpected ordering if the layouts are not perfectly complementary — use `reset` or `normal` mode to disable reordering.
- The `amerge` filter has an empty `description` field in the source data; the description above is derived from the `texi_section` documentation.
