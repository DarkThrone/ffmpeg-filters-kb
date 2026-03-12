+++
title = "apad"
description = "Pad the end of an audio stream with silence to reach a minimum length or to match a video stream duration."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["padding", "silence", "sync", "editing"]

[extra]
filter_type = "audio"
since = ""
see_also = ["atrim", "afade", "aresample"]
parameters = ["packet_size", "pad_len", "whole_len", "pad_dur", "whole_dur"]
cohort = 1
+++

The `apad` filter appends silence to the end of an audio stream. It can add a fixed number of samples, extend the stream to a minimum total length, or pad indefinitely. Its most common use is in combination with the `-shortest` FFmpeg option to prevent audio from ending before a longer video track.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "apad=pad_dur=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| packet_size | int | 4096 | Size of each silence packet in samples. |
| pad_len | int64 | — | Number of silence samples to append. Mutually exclusive with `whole_len`. |
| whole_len | int64 | — | Minimum total number of samples in the output. Silence is appended until this count is reached. Mutually exclusive with `pad_len`. |
| pad_dur | duration | — | Duration of silence to append (e.g., `2.5` seconds). Mutually exclusive with `whole_dur`. |
| whole_dur | duration | — | Minimum total duration of the output. Silence is appended until this duration is reached. Mutually exclusive with `pad_dur`. |

## Examples

### Add 1024 samples of silence to the end

```sh
ffmpeg -i input.wav -af "apad=pad_len=1024" output.wav
```

### Ensure the output is at least 10000 samples long

```sh
ffmpeg -i input.wav -af "apad=whole_len=10000" output.wav
```

### Add 2 seconds of silence at the end

```sh
ffmpeg -i input.mp3 -af "apad=pad_dur=2" output.mp3
```

### Pad audio to match a video's duration when using -shortest

This is the canonical use case: pad audio silence so it outlasts the video, then let `-shortest` trim both to the video length:

```sh
ffmpeg -i video.mp4 -i audio.mp3 \
  -filter_complex "[1:a]apad[aout]" \
  -map 0:v -map "[aout]" -shortest output.mp4
```

### Ensure a minimum total duration of 30 seconds

```sh
ffmpeg -i input.mp3 -af "apad=whole_dur=30" output.mp3
```

## Notes

- If none of `pad_len`, `whole_len`, `pad_dur`, or `whole_dur` is set, `apad` will append silence indefinitely — this is intentional when used with `-shortest` to guarantee the audio outlasts the video.
- `pad_dur` and `whole_dur` are mutually exclusive; setting both causes an error.
- `pad_len` and `whole_len` are also mutually exclusive.
- Note: in FFmpeg 4.4 and earlier, setting `pad_dur=0` or `whole_dur=0` also triggered infinite padding. In later versions, a zero value is treated as "disabled".
