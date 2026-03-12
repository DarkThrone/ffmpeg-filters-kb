+++
title = "volume"
description = "Adjust the input audio volume using a scalar value, dB notation, or a dynamic expression."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["volume", "gain", "dynamics", "expression"]

[extra]
filter_type = "audio"
since = ""
see_also = ["dynaudnorm", "acompressor", "afade"]
parameters = ["volume", "precision", "eval", "replaygain", "replaygain_preamp", "replaygain_noclip"]
cohort = 1
+++

The `volume` filter changes the loudness of an audio stream by multiplying each sample by a configurable gain factor. It accepts simple numeric values, decibel strings like `6dB`, or full mathematical expressions that can reference per-frame variables such as timestamps. Use it whenever you need static level adjustment, loudness matching, or time-varying gain automation.

## Quick Start

```sh
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| volume | string | 1.0 | Volume adjustment expression. Accepts a linear multiplier (`0.5`), dB value (`-6dB`), or any AVExpr expression. |
| precision | int | float | Mathematical precision: `fixed` (8-bit fixed, limits formats to U8/S16/S32), `float` (32-bit, FLT), `double` (64-bit, DBL). |
| eval | int | once | When to evaluate the expression: `once` (at init or on command) or `frame` (every frame). |
| replaygain | int | drop | Behaviour when ReplayGain side data is present: `drop`, `ignore`, `track`, `album`. |
| replaygain_preamp | double | 0.0 | Pre-amplification in dB applied on top of the ReplayGain gain value. |
| replaygain_noclip | bool | true | When enabled, limits the gain to prevent clipping when using ReplayGain. |

## Expression Variables

When `eval=frame` is set, the `volume` expression is re-evaluated for every incoming audio frame. The following variables are available:

| Variable | Description |
|----------|-------------|
| `n` | Frame number, starting at 0. |
| `t` | Frame timestamp in seconds. |
| `nb_samples` | Number of samples in the current frame. |
| `nb_channels` | Number of audio channels. |
| `nb_consumed_samples` | Total samples consumed by the filter so far. |
| `pts` | Frame PTS (presentation timestamp). |
| `sample_rate` | Input sample rate. |
| `startpts` | PTS at the start of the stream. |
| `startt` | Time at the start of the stream. |
| `tb` | Timestamp timebase. |
| `volume` | The last volume value that was set. |

Note: when `eval=once`, only `sample_rate` and `tb` are valid; all other variables evaluate to NaN.

## Examples

### Halve the volume (three equivalent forms)

All three expressions produce the same result — a 6 dB reduction:

```sh
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
ffmpeg -i input.mp4 -af "volume=1/2" output.mp4
ffmpeg -i input.mp4 -af "volume=-6.0206dB" output.mp4
```

### Boost volume by 6 dB with fixed-point precision

```sh
ffmpeg -i input.mp4 -af "volume=6dB:precision=fixed" output.mp4
```

### Fade volume to silence over 5 seconds starting at t=10

The expression evaluates to 1 before the 10-second mark, then linearly ramps to 0 over the following 5 seconds:

```sh
ffmpeg -i input.mp4 -af "volume='if(lt(t,10),1,max(1-(t-10)/5,0))':eval=frame" output.mp4
```

### Apply ReplayGain track gain from metadata

```sh
ffmpeg -i input.flac -af "volume=replaygain=track" output.flac
```

### Gradually increase volume from silence to full over the first 3 seconds

```sh
ffmpeg -i input.mp3 -af "volume='min(t/3,1)':eval=frame" output.mp3
```

## Notes

- Output samples are always clipped to the maximum value for the chosen format; use `precision=double` for the most headroom when processing large gain boosts.
- When `eval=frame` is used, the expression is parsed and evaluated for every single frame, which adds measurable CPU overhead on long files or high sample rates.
- Setting `volume=0` produces silence but does not remove the stream; use `-an` if you want to drop audio entirely.
- The `volume` command can be sent at runtime via the `sendcmd` filter or the `avfilter_graph_send_command` API, allowing dynamic adjustment without re-encoding.
