+++
title = "afade"
description = "Apply a fade-in or fade-out effect to an audio stream with a choice of curve shapes."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["fade", "volume", "editing", "transition"]

[extra]
filter_type = "audio"
since = ""
see_also = ["volume", "atrim", "apad"]
parameters = ["type", "start_sample", "nb_samples", "start_time", "duration", "curve", "silence", "unity"]
cohort = 1
source_file = "libavfilter/af_afade.c"
+++

The `afade` filter smoothly ramps audio volume from silence to full (fade-in) or from full to silence (fade-out) over a configurable time range. It supports a wide variety of curve shapes — linear, sinusoidal, logarithmic, exponential, and others — giving precise control over the character of the transition. Use it to open and close clips cleanly or to create professional-sounding intro and outro segments.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type | int | in | Fade direction: `in` (silence to full volume) or `out` (full volume to silence). (alias: `t`) |
| start_sample | int64 | 0 | Sample index at which the fade begins. (alias: `ss`) |
| nb_samples | int64 | 44100 | Number of samples over which the fade is applied. (alias: `ns`) |
| start_time | duration | 0 | Time at which the fade begins. Overrides `start_sample` if set. (alias: `st`) |
| duration | duration | — | Duration of the fade. Overrides `nb_samples` if set. (alias: `d`) |
| curve | int | tri | Shape of the fade curve. Options: `tri` (linear), `qsin` (quarter sine), `hsin` (half sine), `esin` (exponential sine), `log` (logarithmic), `ipar` (inverted parabola), `qua` (quadratic), `cub` (cubic), `squ` (square root), `cbr` (cubic root), `par` (parabola), `exp` (exponential), `iqsin`, `ihsin`, `dese`, `desi`, `losi`, `sinc`, `isinc`, `quat`, `quatr`, `qsin2`, `hsin2`, `nofade`. (alias: `c`) |
| silence | double | 0.0 | Initial gain for fade-in (or final gain for fade-out). Default 0.0 = complete silence. |
| unity | double | 1.0 | Target gain for fade-in (or initial gain for fade-out). Default 1.0 = original volume. |

## Examples

### Fade in over the first 3 seconds

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3" output.mp3
```

### Fade out over the last 5 seconds of a 60-second clip

```sh
ffmpeg -i input.mp3 -af "afade=t=out:st=55:d=5" output.mp3
```

### Fade in with a logarithmic curve (sounds more natural to the ear)

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=5:curve=log" output.mp3
```

### Apply both a fade-in and fade-out in one command

Chain two `afade` filters — the first fades in over 2 seconds, the second fades out over the last 3 seconds of a 30-second clip:

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=2,afade=t=out:st=27:d=3" output.mp3
```

### Fade in the first 15 seconds and fade out the last 25 of a 900-second file

```sh
ffmpeg -i input.mp3 -af "afade=t=in:ss=0:d=15,afade=t=out:st=875:d=25" output.mp3
```

## Notes

- When using `start_time` and `duration` together, both must be set in compatible units (seconds or time duration strings).
- The `curve=tri` (linear) default is perceptually uneven — a linear ramp in amplitude does not sound like a smooth fade to most listeners. `qsin` (quarter sine) or `log` are generally more natural-sounding.
- For sample-accurate editing, use `start_sample` and `nb_samples` rather than `start_time` and `duration`, which depend on accurate timestamps.
- All parameters are available as real-time commands via `sendcmd`, allowing fade automation without re-encoding.
