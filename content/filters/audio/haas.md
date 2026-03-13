+++
title = "haas"
description = "Apply the Haas effect (precedence effect) to create stereo width from mono or narrow-stereo audio using inter-channel delays."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "effect", "stereo", "width", "delay"]

[extra]
filter_type = "audio"
since = ""
see_also = ["earwax", "apulsator", "extrastereo"]
parameters = ["level_in", "level_out", "side_gain", "middle_source", "middle_phase", "left_delay", "left_balance", "left_gain", "left_phase", "right_delay", "right_balance", "right_gain", "right_phase"]
cohort = 3
+++

The `haas` filter implements the Haas effect (also called the precedence effect) — a psychoacoustic technique that creates a sense of stereo width by introducing a small delay (typically 1–40ms) between channels. Applied to mono audio, it makes the signal appear to come from a wider soundstage. The filter gives independent control over the delay, gain, balance, and phase of each output channel.

## Quick Start

```sh
# Apply Haas effect to mono signal for stereo widening
ffmpeg -i mono.wav -af "haas" stereo.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain (linear). |
| level_out | double | `1.0` | Output gain (linear). |
| side_gain | double | `1.0` | Gain applied to the side (difference) component. |
| middle_source | int | `mid` | Middle source: `left`, `right`, `mid`, `side`. |
| middle_phase | bool | `false` | Invert phase of the middle channel. |
| left_delay | double | `2.05` | Left channel delay in milliseconds. |
| left_balance | double | `-1.0` | Left channel balance (−1 = full left). |
| left_gain | double | `1.0` | Left channel gain. |
| left_phase | bool | `false` | Invert phase of left channel. |
| right_delay | double | `2.12` | Right channel delay in milliseconds. |
| right_balance | double | `1.0` | Right channel balance (+1 = full right). |
| right_gain | double | `1.0` | Right channel gain. |
| right_phase | bool | `true` | Invert phase of right channel (default enabled). |

## Examples

### Basic stereo widening of mono signal

```sh
ffmpeg -i mono.wav -af haas widened.wav
```

### Custom delays for more pronounced effect

```sh
ffmpeg -i input.wav -af "haas=left_delay=5:right_delay=8" wider.wav
```

### Use left channel as middle source

```sh
ffmpeg -i input.wav -af "haas=middle_source=left" output.wav
```

### Stereo widening with gain adjustment

```sh
ffmpeg -i input.wav -af "haas=level_out=0.8:side_gain=1.5" output.wav
```

## Notes

- The Haas effect works best on **mono** or narrow-stereo signals; apply to a mid/side split for controlled widening of existing stereo.
- Delays under 40ms are perceived as stereo width (precedence effect); delays over 40ms become audible echoes.
- The asymmetric default delays (2.05ms left, 2.12ms right) add a subtle natural asymmetry.
- For simple time-based stereo effects, compare with `earwax` (HRTF-based) and `apulsator` (LFO-based panning).
