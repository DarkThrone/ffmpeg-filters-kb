+++
title = "stereotools"
description = "Comprehensive stereo signal processor with M/S encoding/decoding, balance, phase inversion, delay, and stereo base control."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["stereo", "mid-side", "utility", "mastering"]

[extra]
filter_type = "audio"
since = ""
see_also = ["extrastereo", "channelmap", "channelsplit"]
parameters = ["level_in", "level_out", "balance_in", "balance_out", "mode", "slev", "mlev", "base", "delay", "phase"]
cohort = 2
+++

The `stereotools` filter provides a comprehensive set of stereo processing utilities in a single filter: M/S (Mid/Side) encoding and decoding, input/output level and balance control, phase inversion, inter-channel delay, stereo base adjustment, and soft clipping. It is especially useful for mastering, broadcast loudness normalization, and correcting stereo recordings made in M/S microphone technique.

## Quick Start

```sh
# Convert M/S microphone recording to L/R
ffmpeg -i ms_recording.wav -af "stereotools=mode=ms>lr" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1` | Input gain for both channels. Range: 0.015625–64. |
| level_out | double | `1` | Output gain for both channels. Range: 0.015625–64. |
| balance_in | double | `0` | Input balance (-1 = full left, +1 = full right). |
| balance_out | double | `0` | Output balance. |
| softclip | bool | `0` | Enable soft clipping (analog-style limiting). |
| mutel | bool | `0` | Mute left channel. |
| muter | bool | `0` | Mute right channel. |
| phasel | bool | `0` | Invert phase of left channel. |
| phaser | bool | `0` | Invert phase of right channel. |
| mode | int | `lr>lr` | Conversion mode (see below). |
| slev | double | `1` | Side signal level. Range: 0.015625–64. |
| mlev | double | `1` | Middle signal level. Range: 0.015625–64. |
| mpan | double | `0` | Middle signal pan (-1 to 1). |
| base | double | `0` | Stereo base (-1=inverted mono, 0=unchanged, 1=max width). |
| delay | double | `0` | Inter-channel delay in ms (±20 ms). |
| phase | double | `0` | Stereo phase in degrees (0–360). |
| bmode_in / bmode_out | int | `balance` | Balance mode: `balance`, `amplitude`, or `power`. |

### Mode Values

| Mode | Description |
|------|-------------|
| `lr>lr` | L/R to L/R (passthrough, default) |
| `lr>ms` | Encode L/R to M/S |
| `ms>lr` | Decode M/S to L/R |
| `lr>ll` | Duplicate left to both channels |
| `lr>rr` | Duplicate right to both channels |
| `lr>rl` | Swap L/R |

## Examples

### Decode M/S microphone recording

```sh
ffmpeg -i ms_mic.wav -af "stereotools=mode=ms>lr" lr_output.wav
```

### Karaoke effect (remove center/vocals)

```sh
ffmpeg -i music.mp3 -af "stereotools=mlev=0.015625" karaoke.mp3
```

### Widen stereo base

```sh
ffmpeg -i mix.mp3 -af "stereotools=base=0.5:slev=1.2" wider.mp3
```

### Fix phase issue on left channel

```sh
ffmpeg -i input.wav -af "stereotools=phasel=1" fixed.wav
```

### Swap L/R channels

```sh
ffmpeg -i input.wav -af "stereotools=mode=lr>rl" swapped.wav
```

## Notes

- `mode=ms>lr` is the key feature for M/S microphone recordings: Mid = sum (mono center), Side = difference (stereo width).
- `mlev=0.015625` (near zero) removes the center (Mid) signal, creating a karaoke-like effect that strips center-panned vocals.
- `base` adjusts stereo width without M/S conversion: `-1` = inverted mono, `0` = unchanged, `1` = maximum separation.
- `delay` (Haas effect) adds subtle timing offset between channels to widen perceived stereo space.
- Supports runtime commands for all options, enabling dynamic stereo processing automation.
