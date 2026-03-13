+++
title = "showvolume"
description = "Render a real-time per-channel volume meter as a video stream, useful for monitoring audio levels during recording or playback."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "volume", "meter", "scope"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "ebur128", "volumedetect"]
parameters = ["rate", "b", "w", "h", "f", "c", "t", "v", "dm", "dmc", "o", "s", "p", "m", "ds"]
cohort = 3
source_file = "libavfilter/avf_showvolume.c"
+++

The `showvolume` filter produces a real-time volume level meter as a video stream, showing per-channel level bars. It is similar to a hardware VU meter — useful for monitoring recording levels, checking for clipping, or adding a visual level display to a video output. Colors can change based on level (green/yellow/red gradient).

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showvolume"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| b | int | `1` | Border width in pixels around each channel's meter. |
| w | int | `400` | Meter width in pixels. |
| h | int | `20` | Channel meter height in pixels. |
| f | double | `0.95` | Fade factor per frame (0 = instant decay, 1 = no decay). |
| c | string | `PEAK*255+floor(…)` | Meter bar color expression. |
| t | bool | `1` | Show volume value text on the meter bar. |
| v | bool | `1` | Show volume value numerically. |
| dm | double | `0` | Duration of max level display in seconds (peak hold). |
| dmc | color | `orange` | Color of the max level marker. |
| o | int | `h` | Channel display orientation: `h` (horizontal) or `v` (vertical). |
| s | int | `0` | Step in dB between background divisions. |
| p | float | `0` | Background opacity (0 = transparent). |
| m | int | `p` | Averaging mode: `p` (peak), `r` (rms). |
| ds | int | `lin` | Display scale: `lin` or `log`. |

## Examples

### Simple volume meter

```sh
ffplay -f lavfi "amovie=input.wav,showvolume=w=600:h=30"
```

### Peak hold meter (2-second hold)

```sh
ffplay -f lavfi "amovie=music.mp3,showvolume=dm=2:dmc=red"
```

### Embed in a video alongside the waveform

```sh
ffmpeg -i input.mp4 \
  -filter_complex \
    "[0:a]showvolume=w=200:h=720:o=v,format=yuva420p[vol];
     [0:v][vol]overlay=W-w:0" \
  output.mp4
```

### RMS mode with logarithmic display

```sh
ffplay -f lavfi "amovie=music.mp3,showvolume=m=r:ds=log"
```

## Notes

- Default color expression maps level to green→yellow→red via the `PEAK` variable.
- Use `f` (fade factor) to control peak decay speed — `f=1` holds bars statically.
- Combine with `overlay` to add the meter HUD to a video stream.
- For broadcast loudness compliance, use `ebur128`; `showvolume` shows instantaneous amplitude, not integrated loudness.
