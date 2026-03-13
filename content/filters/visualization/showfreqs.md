+++
title = "showfreqs"
description = "Render a real-time FFT frequency spectrum of an audio stream as a video, with configurable modes, scales, and windowing."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "spectrum", "fft", "scope"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showcqt", "showwaves", "showvolume"]
parameters = ["size", "rate", "mode", "ascale", "fscale", "win_size", "overlap", "averaging", "colors", "cmode", "minamp", "data", "channels"]
cohort = 3
source_file = "libavfilter/avf_showfreqs.c"
+++

The `showfreqs` filter renders an FFT-based frequency spectrum display as a video stream. Unlike `showcqt` (which uses a constant-Q transform), `showfreqs` uses a standard FFT with configurable window size, making it suitable for general-purpose spectrum analysis. It supports both bar and line display modes, linear/log frequency and amplitude scales, and per-channel coloring.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showfreqs=size=800x400:mode=bar"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `1080x430` | Output video size. |
| rate / r | video_rate | `25` | Output frame rate. |
| mode | int | `bar` | Display mode: `bar`, `dot`, `line`, `filledline`. |
| ascale | int | `log` | Amplitude scale: `lin`, `log`, `bark`, `mel`. |
| fscale | int | `lin` | Frequency scale: `lin`, `log`, `rlog`. |
| win_size | int | `2048` | FFT window size (power of 2: 32–65536). |
| overlap | float | `1.0` | Window overlap (0–1). |
| averaging | int | `1` | Number of frames to time-average. |
| colors | string | `red\|green\|…` | Per-channel colors. |
| cmode | int | `combined` | Channel mode: `combined` or `separate`. |
| minamp | float | `1e-6` | Minimum amplitude for log scale. |
| data | int | `magnitude` | Display: `magnitude` or `phase`. |
| channels | string | `all` | Which channels to display. |

## Examples

### Bar spectrum with log frequency scale

```sh
ffplay -f lavfi "amovie=music.mp3,showfreqs=size=1280x480:mode=bar:fscale=log"
```

### Separate channels

```sh
ffplay -f lavfi "amovie=stereo.flac,showfreqs=cmode=separate:mode=line"
```

### Save spectrum video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]showfreqs=size=1280x720:mode=bar:ascale=log[v]" \
  -map "[v]" spectrum.mp4
```

### Phase spectrum display

```sh
ffplay -f lavfi "amovie=music.mp3,showfreqs=data=phase:mode=line"
```

## Notes

- Larger `win_size` gives better frequency resolution but less time resolution.
- `fscale=log` is easier to read for music (equal octave widths); `fscale=lin` is better for engineering analysis.
- `averaging` smooths the display over multiple frames — useful for noisy signals.
- For musical note-aligned display, prefer `showcqt`.
