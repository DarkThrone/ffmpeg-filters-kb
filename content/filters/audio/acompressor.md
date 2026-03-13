+++
title = "acompressor"
description = "Apply dynamic range compression to reduce the difference between loud and quiet parts of an audio stream."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "compression", "mastering", "gain"]

[extra]
filter_type = "audio"
since = ""
see_also = ["dynaudnorm", "volume", "equalizer"]
parameters = ["level_in", "threshold", "ratio", "attack", "release", "makeup", "knee", "link", "detection", "level_sc", "mix", "mode"]
cohort = 1
source_file = "libavfilter/af_sidechaincompress.c"
+++

The `acompressor` filter reduces the dynamic range of an audio signal by attenuating samples that exceed a configurable threshold. Configurable attack and release times control how quickly the gain reduction is applied and withdrawn, while a makeup gain parameter compensates for the resulting drop in overall loudness. It is widely used in broadcast normalization, podcast processing, and music mastering to achieve a consistent, controlled sound.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "acompressor=threshold=0.089:ratio=9:attack=200:release=1000:makeup=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | 1.0 | Input gain applied before compression. Range: 0.015625–64. |
| mode | int | downward | Compression mode: `downward` (reduce loud peaks) or `upward` (boost quiet signals). |
| threshold | double | 0.125 | Level above which gain reduction begins. Expressed as a linear amplitude (0.00097563–1). For example, 0.125 corresponds to approximately -18 dBFS. |
| ratio | double | 2.0 | Compression ratio. A ratio of 4:1 means that for every 4 dB above the threshold, only 1 dB passes through. Range: 1–20. |
| attack | double | 20.0 | Time in milliseconds the signal must remain above the threshold before gain reduction starts. Range: 0.01–2000. |
| release | double | 250.0 | Time in milliseconds the signal must remain below the threshold before gain reduction is eased off. Range: 0.01–9000. |
| makeup | double | 1.0 | Post-compression gain multiplier to restore loudness. Range: 1–64. |
| knee | double | 2.828 | Width in dB around the threshold where the compression curve is softened. A higher value gives a gentler transition. Range: 1–8. |
| link | int | average | Whether gain reduction is driven by the `average` level across all channels or the `maximum` (loudest) channel. |
| detection | int | rms | How the signal level is measured: `peak` (instantaneous sample) or `rms` (root-mean-square of recent samples). |
| level_sc | double | 1.0 | Gain applied to the sidechain signal (the signal used for level detection when used as a sidechain compressor). |
| mix | double | 1.0 | Blend between the uncompressed (0.0) and fully compressed (1.0) output — enables parallel compression. |

## Examples

### Gentle broadcast compression

A conservative 3:1 ratio with moderate attack and release is suitable for dialogue normalization:

```sh
ffmpeg -i podcast.mp3 -af "acompressor=threshold=0.125:ratio=3:attack=50:release=500:makeup=1.5" output.mp3
```

### Hard limiting (very high ratio)

A 20:1 ratio effectively acts as a limiter, clamping any peak above the threshold:

```sh
ffmpeg -i input.mp3 -af "acompressor=threshold=0.5:ratio=20:attack=5:release=100:makeup=1" output.mp3
```

### Upward compression to boost quiet passages

`mode=upward` raises quiet sections toward the threshold rather than reducing loud ones:

```sh
ffmpeg -i input.mp3 -af "acompressor=mode=upward:threshold=0.25:ratio=4:attack=20:release=200" output.mp3
```

### Parallel compression (New York compression)

Blend a heavily compressed signal with the dry signal at 50% mix:

```sh
ffmpeg -i drums.wav -af "acompressor=threshold=0.1:ratio=10:attack=1:release=50:makeup=4:mix=0.5" output.wav
```

### Sidechain compression (duck music under voice)

Use `filter_complex` to have the compressor react to the voice stream and apply gain reduction to the music stream:

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300[aout]" \
  -map "[aout]" output.mp3
```

## Notes

- The `threshold` parameter uses a linear amplitude scale, not dBFS. To convert: `linear = 10^(dBFS/20)`. For example, -18 dBFS is approximately 0.125.
- Short `attack` values (below ~5 ms) can cause audible distortion on transients; start with 20–50 ms and adjust by ear.
- Setting `makeup` too aggressively after heavy compression can cause downstream clipping — follow with a `volume` or limiter stage if needed.
- When `detection=rms`, the compressor reacts to perceived loudness more smoothly than with `peak`, making it better suited for musical material.
- The `link=average` default is appropriate for stereo material; use `link=maximum` to preserve stereo image on hard-panned sources.
