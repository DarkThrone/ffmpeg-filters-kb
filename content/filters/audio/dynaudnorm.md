+++
title = "dynaudnorm"
description = "Dynamically normalize audio on a frame-by-frame basis, evening out volume differences while preserving within-frame dynamic range."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["normalization", "dynamics", "loudness", "gain"]

[extra]
filter_type = "audio"
since = ""
see_also = ["acompressor", "volume", "silencedetect"]
parameters = ["framelen", "gausssize", "peak", "maxgain", "targetrms", "coupling", "correctdc", "compress", "threshold", "channels", "overlap"]
cohort = 1
source_file = "libavfilter/af_dynaudnorm.c"
+++

The `dynaudnorm` filter applies per-frame gain normalization so that each frame's peak magnitude approaches a target level. Unlike a static normalizer that computes one gain for the entire file, or a compressor that clips dynamic range, `dynaudnorm` uses a Gaussian-smoothed gain curve across frames to gently even out the volume of quiet and loud sections while retaining 100% of the dynamic range within each frame. It is well-suited for normalizing speech recordings, audio books, and archival material with highly variable loudness.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "dynaudnorm" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| framelen | int | 500 | Length of each analysis frame in milliseconds. Range: 10–8000 ms. (alias: `f`) |
| gausssize | int | 31 | Window size (in frames) of the Gaussian smoothing filter applied to the per-frame gain curve. Must be an odd number. Range: 3–301. (alias: `g`) |
| peak | double | 0.95 | Target peak magnitude for normalized output (0.0–1.0 linear). (alias: `p`) |
| maxgain | double | 10.0 | Maximum gain factor that can be applied to any frame. Prevents over-amplification of very quiet segments. (alias: `m`) |
| targetrms | double | 0.0 | If non-zero, normalize to this RMS level rather than the peak level. Disabled by default. (alias: `r`) |
| coupling | bool | true | When enabled, all channels receive the same gain factor (derived from the loudest channel), preserving stereo balance. (alias: `n`) |
| correctdc | bool | false | Enable DC bias correction to remove any DC offset before normalization. (alias: `c`) |
| altboundary | bool | false | Use silence (rather than the first/last frame value) as boundary condition for the Gaussian filter at stream edges. (alias: `b`) |
| compress | double | 0.0 | Pre-compression factor applied before normalization. 0.0 disables pre-compression. (alias: `s`) |
| threshold | double | 0.0 | Frames whose peak magnitude is below this value are treated as silence and excluded from normalization. (alias: `t`) |
| channels | string | all | Comma-separated list of channels to apply normalization to. (alias: `h`) |
| overlap | double | 0.0 | Fraction of frame overlap (0.0–1.0) to smooth transitions between frames. (alias: `o`) |

## Examples

### Default normalization (recommended starting point)

```sh
ffmpeg -i input.mp3 -af "dynaudnorm" output.mp3
```

### Faster adaptation (shorter frame, smaller Gaussian window)

A 200 ms frame with a window of 11 reacts more quickly to loudness changes — suitable for rapidly varying content:

```sh
ffmpeg -i podcast.mp3 -af "dynaudnorm=f=200:g=11" output.mp3
```

### Slower, more gradual normalization

A longer Gaussian window makes the normalizer behave more like a static loudness pass, with very gentle gain changes:

```sh
ffmpeg -i audiobook.mp3 -af "dynaudnorm=f=500:g=101" output.mp3
```

### Normalize with a maximum gain cap to avoid pumping

Cap gain at 5× to prevent over-amplification of near-silent passages:

```sh
ffmpeg -i input.mp3 -af "dynaudnorm=maxgain=5" output.mp3
```

### RMS-based normalization

Normalize to a target RMS level instead of peak — often sounds more consistent for speech:

```sh
ffmpeg -i speech.wav -af "dynaudnorm=targetrms=0.25" output.wav
```

## Notes

- The filter introduces latency equal to approximately half of `gausssize` × `framelen` milliseconds, because the Gaussian filter is centered around the current frame and needs to look ahead. This makes it unsuitable for real-time streaming.
- A larger `gausssize` produces a smoother gain curve (less audible gain pumping) but reduces responsiveness to sudden loudness changes. A smaller value makes the filter behave more like a dynamic range compressor.
- Setting `coupling=false` allows each channel to receive independent gain, which can alter stereo or surround image — leave it enabled for music and most stereo content.
- The `maxgain` cap is important: without it, a very quiet frame (e.g., room tone between words) could receive an extremely large gain boost, audibly amplifying background noise.
