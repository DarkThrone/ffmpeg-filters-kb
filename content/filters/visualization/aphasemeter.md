+++
title = "aphasemeter"
description = "Render a stereo phase correlation meter (Lissajous-style) as a video stream, showing the stereo phase relationship between left and right channels."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "audio", "phase", "stereo", "scope"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["showwaves", "showvolume", "vectorscope"]
parameters = ["rate", "size", "rc", "gc", "bc", "mpc", "video", "phasing", "tolerance", "angle", "duration"]
cohort = 3
source_file = "libavfilter/avf_aphasemeter.c"
+++

The `aphasemeter` filter renders a stereo phase meter — a Lissajous-style display where left and right audio channels drive the X and Y axes. When the stereo image is perfectly mono (identical channels), dots cluster on the vertical center line. Wide stereo spreads diagonally, while out-of-phase content spreads horizontally. It can optionally detect and log "out-of-phase" conditions where mono sum would cause cancellation. The audio passes through unchanged.

## Quick Start

```sh
ffplay -f lavfi "amovie=stereo.mp3,aphasemeter"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `800x400` | Output video size. |
| rc | int | `2` | Red component of phase dot color. |
| gc | int | `7` | Green component of phase dot color. |
| bc | int | `1` | Blue component of phase dot color. |
| mpc | color | `orange` | Color for the out-of-phase indicator. |
| video | bool | `1` | Enable video output. |
| phasing | bool | `0` | Enable out-of-phase detection. |
| tolerance / t | float | `0.0` | Phase tolerance (0–1) before triggering out-of-phase alert. |
| angle / a | float | `170.0` | Angle (degrees) defining the out-of-phase detection zone. |
| duration / d | duration | `2s` | Duration before triggering an out-of-phase event. |

## Examples

### Basic phase meter

```sh
ffplay -f lavfi "amovie=stereo.flac,aphasemeter"
```

### With out-of-phase detection

```sh
ffmpeg -i stereo.wav -af "aphasemeter=phasing=1:duration=1" -f null - 2>&1 | grep phase
```

### Combine phase meter with audio in output

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex "[0:a]aphasemeter=size=400x200,format=yuva420p[scope];[0:a]anull[aud]" \
  -map "[scope]" -map "[aud]" output.mp4
```

### Save phase meter video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]aphasemeter=size=600x300[v]" \
  -map "[v]" phasemeter.mp4
```

## Notes

- A vertical line indicates perfectly mono-compatible audio; a horizontal spread indicates out-of-phase content that will cancel when summed to mono.
- Enable `phasing=1` to log metadata events when extended out-of-phase conditions are detected — useful for broadcast QC.
- The Lissajous display is the industry-standard tool for checking stereo compatibility before broadcast or streaming.
- For mono content, all dots will appear on the center diagonal (Y = X line).
