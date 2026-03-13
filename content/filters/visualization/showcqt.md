+++
title = "showcqt"
description = "Render an audio stream as an animated Constant-Q Transform (CQT) spectrogram video, showing frequency content on a musical scale."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "spectrum", "scope"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "showfreqs", "aphasemeter"]
parameters = ["size", "fps", "bar_h", "axis_h", "sono_h", "volume", "bar_v", "gamma", "basefreq", "endfreq", "tlength", "count", "fontcolor", "cscheme"]
cohort = 3
+++

The `showcqt` filter converts audio to a real-time spectrogram video using the Constant-Q Transform — a frequency analysis that spaces bins logarithmically, aligning with musical octaves and note intervals. The display can combine a scrolling sonogram (time-frequency heatmap) with a bar graph of instantaneous spectrum. Unlike FFT visualizers, `showcqt` maps frequency linearly to pitch, making it ideal for music analysis and visualization.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showcqt"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `1920x1080` | Output video size. |
| fps / rate / r | video_rate | `25` | Output frame rate. |
| bar_h | int | `-1` | Bar graph height (auto if −1). |
| axis_h | int | `-1` | Axis label height (auto if −1). |
| sono_h | int | `-1` | Sonogram height (auto if −1). |
| volume / sono_v | string | `16` | Sonogram volume (brightness) expression. |
| bar_v / volume2 | string | `sono_v` | Bar graph volume expression. |
| gamma / sono_g | float | `3.0` | Sonogram gamma correction. |
| basefreq | double | `20.01523...` | Lowest displayed frequency (Hz). |
| endfreq | double | `20495.6...` | Highest displayed frequency (Hz). |
| tlength | string | `384*tc/(384+tc*f)` | Per-frequency transform length expression. |
| count | int | `6` | Number of transform passes per frame. |
| fontcolor | string | `st(0,…)` | Axis label color expression. |
| cscheme | string | `1|0.5|0|0|0.5|1` | Color scheme (`R|G|B|R|G|B` for low/high). |

## Examples

### Basic visualization with ffplay

```sh
ffplay -f lavfi "amovie=music.flac,showcqt=size=1920x1080:count=4"
```

### Save spectrogram video

```sh
ffmpeg -i music.mp3 \
  -filter_complex "[0:a]showcqt=size=1280x720:fps=25[v]" \
  -map "[v]" -c:v libx264 cqt.mp4
```

### Only show bar graph (no sonogram)

```sh
ffplay -f lavfi "amovie=music.mp3,showcqt=sono_h=0:bar_h=400:axis_h=50"
```

### Custom color scheme (green tones)

```sh
ffplay -f lavfi "amovie=music.mp3,showcqt=cscheme=0|1|0|0|0.5|0"
```

## Notes

- `showcqt` is computationally expensive; reduce `count` or `size` for real-time use on slower machines.
- The frequency axis spans piano key range by default (A0 to C8 approximately).
- Combine with `[0:a]showcqt[v];[0:a][0:v]…` to get synchronized audio/video in one output.
- `tlength` controls the time-frequency trade-off: longer = better frequency resolution, shorter = better time resolution.
