+++
title = "showwaves"
description = "Render an audio waveform as a real-time video stream, with configurable display modes, colors, and scaling."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "waveform", "scope"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwavespic", "showfreqs", "showvolume"]
parameters = ["size", "mode", "n", "rate", "split_channels", "colors", "scale", "draw", "filter"]
cohort = 3
source_file = "libavfilter/avf_showwaves.c"
+++

The `showwaves` filter converts an audio stream into an animated waveform video. It supports several rendering modes — point, line, p2p (peak-to-peak), and cline (centered line) — and can display all channels merged or split into separate rows. It is commonly used for YouTube music visualizations, podcast videos, and audio quality inspection.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showwaves=size=800x300:mode=line"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `600x240` | Output video size. |
| mode | int | `point` | Display mode: `point`, `line`, `p2p`, `cline`. |
| n | int64 | auto | Number of audio samples per output pixel (auto-computed from rate). |
| rate / r | video_rate | `25` | Output frame rate. |
| split_channels | bool | `0` | Display each channel in a separate row. |
| colors | string | `red|green|blue|yellow|…` | Per-channel colors separated by `\|`. |
| scale | int | `lin` | Amplitude scale: `lin`, `log`, `sqrt`, `cbrt`. |
| draw | int | `scale` | Drawing mode: `scale` or `full`. |
| filter | int | `off` | IIR filter to smooth: `off`, `average`. |

## Examples

### Scrolling waveform with ffplay

```sh
ffplay -f lavfi "amovie=music.mp3,showwaves=size=1280x360:mode=line:colors=white"
```

### Split channels in stereo

```sh
ffplay -f lavfi "amovie=stereo.flac,showwaves=size=800x400:split_channels=1:mode=cline"
```

### Save waveform video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]showwaves=size=1280x720:mode=line:colors=0x00aaff[v]" \
  -map "[v]" -c:v libx264 waveform.mp4
```

### Logarithmic scale for dynamic range

```sh
ffplay -f lavfi "amovie=music.mp3,showwaves=scale=log:mode=p2p"
```

## Notes

- `mode=line` draws a filled waveform (solid area); `mode=p2p` shows instantaneous peak-to-peak range; `mode=cline` draws lines from the center.
- `n` controls time resolution — lower values = more detail per pixel; auto-calculated from rate and size.
- For a static image of the full waveform, use `showwavespic` instead.
- Colors accept hex (`0xRRGGBB`), named colors, or `RRGGBB@alpha` with transparency.
