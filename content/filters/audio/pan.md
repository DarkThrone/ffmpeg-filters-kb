+++
title = "pan"
description = "Remix, remap, or pan audio channels with arbitrary gain coefficients to produce any output channel layout."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["mixing", "panning", "channels", "surround", "remapping"]

[extra]
filter_type = "audio"
since = ""
see_also = ["amerge", "amix", "aformat"]
parameters = []
cohort = 1
+++

The `pan` filter provides full control over how input audio channels are combined into output channels. Unlike the `-ac` option, which applies a fixed automatic downmix, `pan` lets you specify exact gain coefficients for each output channel, making it suitable for custom stereo downmixes from surround sources, channel remapping, muting individual channels, and panning mono signals anywhere in a multi-channel layout.

## Quick Start

```sh
ffmpeg -i input.mp4 -af "pan=stereo|FL=FL|FR=FR" output.mp4
```

## Syntax

The filter takes a single string argument with the format:

```
pan=layout|out_ch=expr|out_ch=expr|...
```

- `layout`: output channel layout name (e.g., `stereo`, `5.1`, `mono`) or number of channels (e.g., `2`).
- `out_ch`: output channel name (`FL`, `FR`, `FC`, etc.) or number (`c0`, `c1`, …).
- `expr`: a sum of `[gain*]in_channel` terms. Use `+` or `-` to combine channels.
- Replace `=` with `<` to auto-normalize the gains for that output channel so their sum equals 1.

## Examples

### Stereo to mono with equal weight

```sh
ffmpeg -i stereo.mp3 -af "pan=1c|c0=0.5*c0+0.5*c1" mono.mp3
```

### Stereo to mono with more weight on the left

```sh
ffmpeg -i stereo.mp3 -af "pan=1c|c0=0.9*c0+0.1*c1" mono.mp3
```

### 5.1 to stereo downmix preserving surround information

The `<` operator normalizes the gains automatically to prevent clipping. Works for 3, 4, 5, and 7-channel sources:

```sh
ffmpeg -i surround.mp4 \
  -af "pan=stereo|FL<FL+0.5*FC+0.6*BL+0.6*SL|FR<FR+0.5*FC+0.6*BR+0.6*SR" \
  stereo.mp4
```

### 5.1 to stereo by keeping only front left and right

Pure channel remapping (no mixing) — FFmpeg detects this and uses a lossless copy path:

```sh
ffmpeg -i surround.mkv -af "pan=stereo|c0=FL|c1=FR" stereo.mkv
```

### Swap left and right channels in a stereo stream

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c0=c1|c1=c0" swapped.mp3
```

### Mute the left channel of a stereo stream

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c1=c1" muted_left.mp3
```

### Copy the right channel to both outputs

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c0=FR|c1=FR" right_both.mp3
```

## Notes

- When all gain coefficients are 0 or 1 and each output channel draws from exactly one input channel, FFmpeg detects a "pure channel mapping" and uses a highly optimized, lossless path.
- The `pan` filter supports many formats (integer and float). For floating-point-only mixing of many inputs, `amix` can be more convenient.
- Named channel identifiers (`FL`, `FR`, `FC`, `LFE`, `BL`, `BR`, `SL`, `SR`) and numbered identifiers (`c0`, `c1`, …) cannot be mixed within a single channel specification.
- FFmpeg's built-in `-ac` downmix is preferred for standard conversions; use `pan` only when you need precise control over gain coefficients.
