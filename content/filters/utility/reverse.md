+++
title = "reverse"
description = "Reverse a video clip in time by buffering all frames and outputting them in reverse order."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "reverse", "timing"]

[extra]
filter_type = "utility"
since = ""
see_also = ["areverse", "setpts", "trim"]
parameters = []
cohort = 3
+++

The `reverse` filter plays a video clip backwards by buffering all frames in memory and then emitting them in reverse order. It requires the complete clip to be buffered before any output is produced. This is commonly used for creative reverse effects, slow-motion reversal, or generating mirror/palindrome edits. Always trim the input first to limit memory usage.

## Quick Start

```sh
# Reverse the first 5 seconds of a video
ffmpeg -i input.mp4 -vf "trim=end=5,reverse" reversed.mp4
```

## Parameters

None. `reverse` takes no options.

## Examples

### Reverse the first 5 seconds

```sh
ffmpeg -i input.mp4 -vf "trim=end=5,setpts=PTS-STARTPTS,reverse" reversed.mp4
```

### Reverse an entire short clip

```sh
ffmpeg -i short_clip.mp4 -vf reverse reversed.mp4
```

### Create a boomerang effect (forward + reverse)

```sh
ffmpeg -i clip.mp4 \
  -filter_complex "[0:v]split[a][b];[b]reverse[rev];[a][rev]concat=n=2:v=1:a=0" \
  boomerang.mp4
```

### Reverse with audio

```sh
ffmpeg -i clip.mp4 -vf reverse -af areverse reversed_av.mp4
```

## Notes

- **Warning:** `reverse` buffers the entire clip in memory. For long videos, trim first with `trim=end=N`.
- Always add `setpts=PTS-STARTPTS` after `trim` to reset timestamps before passing to `reverse`.
- Use both `reverse` and `areverse` together to reverse audio and video simultaneously.
- This is a single-pass operation — the output duration matches the input duration exactly.
