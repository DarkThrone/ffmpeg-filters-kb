+++
title = "aformat"
description = "Constrain the output audio format to one of a set of allowed sample formats, sample rates, or channel layouts."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["format", "conversion", "samplerate", "channels"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aresample", "amerge", "pan"]
parameters = ["sample_fmts", "sample_rates", "channel_layouts"]
cohort = 1
source_file = "libavfilter/af_aformat.c"
+++

The `aformat` filter forces the audio stream to conform to one of the formats you specify. FFmpeg's filter negotiation framework will insert the minimum number of automatic conversions needed to satisfy the constraint. It is useful for ensuring downstream filters or encoders receive a compatible format without manually inserting `aresample` or format conversion filters.

## Quick Start

```sh
ffmpeg -i input.wav -af "aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=stereo" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sample_fmts | sample_fmt | (all allowed) | A `\|`-separated list of acceptable sample formats, e.g., `s16\|s32\|fltp`. (alias: `f`) |
| sample_rates | int | (all allowed) | A `\|`-separated list of acceptable sample rates in Hz, e.g., `44100\|48000`. (alias: `r`) |
| channel_layouts | channel_layout | (all allowed) | A `\|`-separated list of acceptable channel layouts, e.g., `stereo\|mono`. (alias: `cl`) |

## Examples

### Force unsigned 8-bit or signed 16-bit stereo output

```sh
ffmpeg -i input.flac -af "aformat=sample_fmts=u8|s16:channel_layouts=stereo" output.wav
```

### Ensure 48 kHz sample rate for broadcast delivery

```sh
ffmpeg -i input.mp3 -af "aformat=sample_rates=48000" output.wav
```

### Restrict to float formats for a downstream DSP filter

Some filters only work with float samples. This ensures conversion happens before the chain:

```sh
ffmpeg -i input.wav -af "aformat=sample_fmts=fltp|flt,dynaudnorm" output.wav
```

### Accept either stereo or mono, forcing a conversion if needed

```sh
ffmpeg -i input.wav -af "aformat=channel_layouts=stereo|mono" output.wav
```

### Constrain all three dimensions at once

```sh
ffmpeg -i input.flac -af "aformat=sample_fmts=s16:sample_rates=44100|48000:channel_layouts=stereo" output.wav
```

## Notes

- If a parameter is omitted, any value is accepted for that dimension — you only need to specify the dimensions you want to constrain.
- FFmpeg automatically inserts the cheapest conversion (e.g., `aresample` for rate conversion, `aconvert` for format conversion) to satisfy the constraint; no explicit conversion filter is needed.
- The `|` separator in option values must be used without spaces: `s16|s32`, not `s16 | s32`.
- `aformat` is often used as a final step in a filter chain to guarantee encoder-compatible output before the muxer stage.
