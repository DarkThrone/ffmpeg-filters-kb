+++
title = "abitscope"
description = "Visualize audio sample bit patterns as a video scope, showing which bits are active across samples."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "scope", "bits"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "aphasemeter", "a3dscope"]
parameters = ["rate", "size", "colors", "mode"]
cohort = 3
+++

The `abitscope` filter renders a video visualization of the bit patterns in audio samples. Each horizontal row represents a bit position (MSB at top), and the display scrolls in time showing which bits are set across samples. It is primarily useful for analyzing the true bit depth of audio — distinguishing between genuine 24-bit content and 16-bit audio upsampled to 24-bit (which shows blank lower bits).

## Quick Start

```sh
ffplay -f lavfi "amovie=input.wav,abitscope"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `512x256` | Output video size. |
| colors | string | `red\|green\|blue\|…` | Per-channel colors. |
| mode / m | int | `combined` | Channel display: `combined` or `separate`. |

## Examples

### Inspect bit depth of a WAV file

```sh
ffplay -f lavfi "amovie=audio.wav,abitscope=size=800x400"
```

### Separate channel display

```sh
ffplay -f lavfi "amovie=stereo.flac,abitscope=mode=separate"
```

### Save bit scope video

```sh
ffmpeg -i input.wav \
  -filter_complex "[0:a]abitscope=size=512x256[v]" \
  -map "[v]" bitscope.mp4
```

## Notes

- Genuine 24-bit audio shows activity down to the lowest bit rows; upsampled 16-bit audio shows the bottom 8 rows as blank.
- The display is most informative for uncompressed PCM sources (WAV, FLAC, AIFF).
- For waveform and frequency visualization, `showwaves` and `showfreqs` are more commonly used.
