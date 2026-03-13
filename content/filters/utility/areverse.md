+++
title = "areverse"
description = "Reverse an audio clip in time by buffering all samples and outputting them in reverse order."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "audio", "reverse", "timing"]

[extra]
filter_type = "utility"
since = ""
see_also = ["reverse", "atrim", "asetpts"]
parameters = []
cohort = 3
+++

The `areverse` filter plays audio backwards by buffering all samples in memory and emitting them in reverse order. It is the audio counterpart to the `reverse` video filter, and they are typically used together to create a fully reversed audio/video clip. Reverse audio is commonly used in music production (for reverse reverb effects), film sound design, and creative edits.

## Quick Start

```sh
# Reverse first 5 seconds of audio
ffmpeg -i input.wav -af "atrim=end=5,areverse" reversed.wav
```

## Parameters

None. `areverse` takes no options.

## Examples

### Reverse first 5 seconds of audio

```sh
ffmpeg -i input.mp3 -af "atrim=end=5,asetpts=PTS-STARTPTS,areverse" reversed.mp3
```

### Reverse an entire short clip

```sh
ffmpeg -i short.wav -af areverse reversed.wav
```

### Reverse audio and video together

```sh
ffmpeg -i clip.mp4 -vf reverse -af areverse reversed.mp4
```

### Reverse reverb effect (apply reverb then reverse for pre-reverb)

```sh
ffmpeg -i dry.wav -af "areverse,aecho=0.8:0.5:1000:0.5,areverse" reverse_reverb.wav
```

## Notes

- **Warning:** `areverse` buffers the entire audio in memory. For long files, trim first with `atrim=end=N`.
- Add `asetpts=PTS-STARTPTS` after `atrim` to reset audio timestamps before `areverse`.
- The reverse reverb technique: reverse the audio, apply reverb, reverse again — the reverb swells before each transient.
- Output duration matches input duration exactly.
