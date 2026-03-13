+++
title = "earwax"
description = "Apply a headphone spatialization effect that moves the stereo image outside the head, simulating speaker listening on headphones."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "stereo", "headphones", "spatial"]

[extra]
filter_type = "audio"
since = ""
see_also = ["haas", "apulsator", "extrastereo"]
parameters = []
cohort = 3
+++

The `earwax` filter adds head-related transfer function (HRTF) cues to stereo audio so that when listened to on headphones, the stereo image appears to come from in front of and around the listener rather than from inside the head. It processes 44.1kHz stereo audio (CD format) by applying cross-feed and spectral shaping. Ported from SoX.

## Quick Start

```sh
ffmpeg -i music.flac -af earwax output.wav
```

## Parameters

None. `earwax` takes no options.

## Examples

### Apply earwax to a music file

```sh
ffmpeg -i stereo.flac -af earwax -ar 44100 headphones.wav
```

### Real-time preview with ffplay

```sh
ffplay -i music.mp3 -af earwax
```

### Process and keep original as comparison

```sh
ffmpeg -i input.wav -af earwax processed.wav
ffplay input.wav &
ffplay processed.wav
```

## Notes

- `earwax` is designed specifically for **44.1kHz stereo** input — for other sample rates, resample first with `-ar 44100`.
- The effect is subjective and not universally preferred; some listeners find it distracting.
- For more control over stereo width and delay, use `haas` instead.
- Ported from the SoX audio toolkit's `earwax` effect.
