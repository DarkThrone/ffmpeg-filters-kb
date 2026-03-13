+++
title = "sidechaincompress"
description = "Apply dynamic range compression to audio where the gain reduction is triggered by a sidechain signal."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["dynamics", "compression", "sidechain"]

[extra]
filter_type = "audio"
since = ""
see_also = ["acompressor", "sidechaingate"]
parameters = ["level_in", "mode", "threshold", "ratio", "attack", "release", "makeup", "knee", "link", "detection", "level_sc", "mix"]
cohort = 2
+++

The `sidechaincompress` filter compresses one audio stream based on the level of a second, independent "sidechain" signal. The classic application is "ducking": the background music is compressed whenever a voice-over signal is active, automatically lowering the music volume under speech. It requires `filter_complex` with two audio inputs: the signal to compress and the sidechain trigger.

## Quick Start

```sh
# Duck music under voice: music is compressed when voice is loud
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300[aout]" \
  -map "[aout]" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before compression. |
| mode | int | `downward` | `downward` (compress loud peaks) or `upward` (boost quiet signals). |
| threshold | double | `0.125` | Sidechain level at which compression begins (linear amplitude). |
| ratio | double | `2.0` | Compression ratio above the threshold. Range: 1–20. |
| attack | double | `20.0` | Time in ms for compression to engage when sidechain exceeds threshold. |
| release | double | `250.0` | Time in ms for compression to release when sidechain drops below threshold. |
| makeup | double | `1.0` | Post-compression gain multiplier. |
| knee | double | `2.828` | Soft-knee width in dB around the threshold. |
| link | int | `average` | Level detection link: `average` (mean of all channels) or `maximum`. |
| detection | int | `rms` | Sidechain level detection: `rms` or `peak`. |
| level_sc | double | `1.0` | Gain applied to the sidechain signal before level detection. |
| mix | double | `1.0` | Wet/dry mix (1.0 = fully compressed). |

## Examples

### Duck music when voice is active

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=6:attack=10:release=200[aout]" \
  -map "[aout]" output.mp3
```

### Aggressive ducking (ratio 20:1 ≈ limiting)

```sh
ffmpeg -i bg_music.mp3 -i narration.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.01:ratio=20:attack=5:release=300[out]" \
  -map "[out]" output.mp3
```

### Also normalise output volume after ducking

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300:makeup=2[out]" \
  -map "[out]" output.mp3
```

## Notes

- The first input (`[0:a]`) is the audio to be compressed; the second (`[1:a]`) is the sidechain trigger (e.g. voice). The sidechain audio is NOT included in the output.
- `threshold` uses linear amplitude. For dBFS conversion: `linear = 10^(dBFS/20)`. A threshold of 0.02 ≈ -34 dBFS is suitable for activating on speech.
- `attack` and `release` are key for natural-sounding ducking: fast attack (5–20 ms), medium-slow release (200–500 ms).
- To duck on every audio channel simultaneously, use `link=average`; to trigger on only the loudest channel, use `link=maximum`.
