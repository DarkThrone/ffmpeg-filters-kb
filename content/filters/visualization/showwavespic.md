+++
title = "showwavespic"
description = "Render the full waveform of an audio file as a single static image."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "waveform", "image"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "showfreqs"]
parameters = ["size", "mode", "split_channels", "colors", "scale", "draw", "filter"]
cohort = 3
source_file = "libavfilter/avf_showwaves.c"
+++

The `showwavespic` filter renders the entire waveform of an audio stream into a single static image — the visual equivalent of the waveform view in a DAW or audio editor. Unlike `showwaves` (which produces a scrolling video), `showwavespic` buffers the complete audio and outputs one frame covering the full duration. It is ideal for thumbnail generation, album art waveforms, or batch waveform previews.

## Quick Start

```sh
ffmpeg -i input.mp3 -filter_complex "showwavespic=size=800x200" waveform.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `600x240` | Output image size. |
| mode | int | `point` | Rendering mode: `point`, `line`, `p2p`, `cline`. |
| split_channels | bool | `0` | Display each channel in a separate row. |
| colors | string | `red\|green\|…` | Per-channel colors separated by `\|`. |
| scale | int | `lin` | Amplitude scale: `lin`, `log`, `sqrt`, `cbrt`. |
| draw | int | `scale` | Drawing mode: `scale` or `full`. |
| filter | int | `off` | IIR smoothing filter: `off` or `average`. |

## Examples

### Generate a waveform PNG

```sh
ffmpeg -i podcast.mp3 -filter_complex "showwavespic=size=1200x300:mode=line:colors=steelblue" waveform.png
```

### Split stereo channels

```sh
ffmpeg -i stereo.flac \
  -filter_complex "showwavespic=size=1000x400:split_channels=1" \
  stereo_waveform.png
```

### Waveform for a trimmed section

```sh
ffmpeg -i input.mp3 -ss 30 -t 60 \
  -filter_complex "showwavespic=size=800x200" section.png
```

### Logarithmic scale (shows quiet parts better)

```sh
ffmpeg -i input.wav -filter_complex "showwavespic=scale=log:mode=p2p" waveform_log.png
```

## Notes

- The filter buffers the entire audio before producing output — memory usage scales with audio duration at the sample rate.
- Trim long files with `-t` or `atrim` before feeding to `showwavespic` to keep memory usage manageable.
- For a scrolling real-time waveform video, use `showwaves` instead.
- `mode=p2p` (peak-to-peak) is the most common choice for DAW-style waveform thumbnails.
