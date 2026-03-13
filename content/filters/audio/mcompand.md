+++
title = "mcompand"
description = "Multiband dynamic range compressor/expander that splits audio into frequency bands and applies independent compander settings per band."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "compressor", "dynamics", "multiband"]

[extra]
filter_type = "audio"
since = ""
see_also = ["compand", "loudnorm", "alimiter"]
parameters = ["args"]
cohort = 3
source_file = "libavfilter/af_mcompand.c"
+++

The `mcompand` filter is a multiband dynamic range processor. It splits audio into frequency bands using 4th-order Linkwitz-Riley crossover filters (the same design used in loudspeaker crossovers, ensuring flat frequency response when all bands are combined at unity gain). Each band has independent attack/decay times and a compander transfer curve defined by input/output point pairs. This enables frequency-aware compression — for example, tighter control of low-frequency dynamics without affecting treble.

## Quick Start

```sh
# Two-band compander: different settings for bass and treble
ffmpeg -i input.wav -af "mcompand=args=0.005,0.1 6 -47/-40,-34/-34,-17/-33 | 0.003,0.05 6 -47/-40,-34/-34,-17/-33:crossover_freq=1500" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | string | — | Band definitions separated by `\|`. Each band: `attack,decay,[attack,decay] soft-knee points crossover_frequency [delay [init_volume [gain]]]`. |

## Band Syntax

```
attack,decay soft-knee points crossover_freq
```

- `attack,decay`: Attack and decay times in seconds
- `soft-knee`: Soft-knee width in dB
- `points`: Space-separated `in/out` dB point pairs defining the transfer curve
- `crossover_freq`: Upper crossover frequency of this band (Hz)

## Examples

### Simple two-band compression

```sh
ffmpeg -i input.wav \
  -af "mcompand=args=0.005,0.1 6 -47/-40,-34/-34,-17/-33 | 0.003,0.05 6 -47/-40,-34/-34,-17/-33:crossover_freq=1000" \
  output.wav
```

### Three-band with different ratios

```sh
ffmpeg -i music.wav \
  -af "mcompand=args=0.1,0.3 6 -50/-50,-30/-25,-15/-10 | 0.05,0.1 6 -50/-50,-30/-22,-15/-8 | 0.02,0.05 6 -50/-50,-30/-20,-15/-6:crossover_freq=200,2000" \
  mastered.wav
```

## Notes

- The `args` syntax is complex — refer to the `compand` filter documentation for point-pair transfer curve details.
- Because Linkwitz-Riley crossovers have flat summed response, the filter is transparent at unity gain (no transfer curve applied).
- For simpler single-band compression, use `compand` or `acompressor`.
- More bands = more CPU usage; two or three bands is typical for practical use.
