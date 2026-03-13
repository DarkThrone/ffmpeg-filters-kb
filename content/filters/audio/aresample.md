+++
title = "aresample"
description = "Resample audio to a different sample rate or convert between audio formats using libswresample."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["resampling", "samplerate", "conversion", "format"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aformat", "atempo", "apad"]
parameters = []
cohort = 1
source_file = "libavfilter/af_aresample.c"
+++

The `aresample` filter converts audio to a different sample rate and can also stretch or compress audio timestamps to maintain synchronization. It is powered by the `libswresample` library and exposes all of its resampler options. When no parameters are given, it acts as an automatic format adapter, inserting itself wherever a format conversion is needed in a filter graph.

## Quick Start

```sh
ffmpeg -i input.flac -af "aresample=44100" output.flac
```

## Parameters

`aresample` has no parameters defined in its JSON option list. It accepts the following syntax:

```
aresample=[sample_rate:]resampler_options
```

| Argument | Description |
|----------|-------------|
| sample_rate | Target sample rate in Hz. Optional; if omitted, the rate is negotiated automatically. |
| resampler_options | Colon-separated `key=value` pairs passed directly to `libswresample`. See the `ffmpeg-resampler` manual for the complete list. |

Common `libswresample` options:

| Option | Description |
|--------|-------------|
| `async` | Maximum number of samples per second the resampler may add or remove to compensate for timestamp drift. |
| `first_pts` | Assume the first PTS is this value instead of zero. |
| `min_hard_comp` | Minimum difference (in seconds) between timestamps before hard compensation (inserting/dropping samples) is triggered. |
| `filter_size` | Length of the resampling filter (more taps = higher quality, more CPU). |

## Examples

### Resample to 44100 Hz

```sh
ffmpeg -i input_48k.wav -af "aresample=44100" output_44k.wav
```

### Resample to 48000 Hz (common broadcast standard)

```sh
ffmpeg -i input.mp3 -af "aresample=48000" output.wav
```

### Timestamp compensation with up to 1000 samples/s adjustment

This allows the resampler to insert or drop up to 1000 samples per second to correct A/V drift:

```sh
ffmpeg -i input.mp4 -af "aresample=async=1000" output.mp4
```

### High-quality resampling with a larger filter

A longer filter kernel gives better frequency response at the cost of more CPU:

```sh
ffmpeg -i input.flac -af "aresample=96000:filter_size=256" output_96k.flac
```

### Automatic format negotiation (no arguments)

Let FFmpeg decide when a conversion is needed — useful in complex filter graphs:

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]aresample,dynaudnorm[out]" -map "[out]" output.mp3
```

## Notes

- `aresample` with no arguments is equivalent to `aformat` with no constraints — it acts as a passthrough unless FFmpeg's filter negotiation decides a conversion is needed.
- The `async` option is particularly useful when synchronizing audio to video in files with imprecise timestamps; it gradually corrects drift without audible artifacts.
- Very high sample rate conversion (e.g., 8000 Hz to 192000 Hz) is computationally expensive; consider whether it is actually required before including it in a pipeline.
- The `aresample` filter has an empty `options` list in the source JSON because its options are passed through to `libswresample` rather than being declared as AVOptions.
