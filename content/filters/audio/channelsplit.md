+++
title = "channelsplit"
description = "Split a multi-channel audio stream into separate per-channel mono streams for independent processing or routing."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["channel", "routing", "utility", "multichannel"]

[extra]
filter_type = "audio"
since = ""
see_also = ["channelmap", "amerge", "join"]
parameters = ["channel_layout", "channels"]
cohort = 2
source_file = "libavfilter/af_channelsplit.c"
+++

The `channelsplit` filter splits a multi-channel audio stream into separate single-channel mono streams — one output per channel. This enables routing individual channels to different outputs, applying per-channel processing, or extracting specific channels (e.g. just the LFE from a 5.1 mix). It is a multiple-output filter and requires `-filter_complex`.

## Quick Start

```sh
# Split stereo into L and R
ffmpeg -i stereo.mp3 -filter_complex channelsplit out.mkv
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| channel_layout | chlayout | `stereo` | Channel layout of the input stream (e.g. `stereo`, `5.1`, `7.1`). |
| channels | string | `all` | Channels to extract, or `all`. E.g. `FL+FR`, `LFE`. |

## Examples

### Split stereo into separate L/R files

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex 'channelsplit=channel_layout=stereo[L][R]' \
  -map '[L]' left.wav \
  -map '[R]' right.wav
```

### Split 5.1 into 6 individual channel files

```sh
ffmpeg -i surround.wav \
  -filter_complex 'channelsplit=channel_layout=5.1[FL][FR][FC][LFE][SL][SR]' \
  -map '[FL]' front_left.wav \
  -map '[FR]' front_right.wav \
  -map '[FC]' center.wav \
  -map '[LFE]' lfe.wav \
  -map '[SL]' side_left.wav \
  -map '[SR]' side_right.wav
```

### Extract only the LFE channel

```sh
ffmpeg -i surround.wav \
  -filter_complex 'channelsplit=channel_layout=5.1:channels=LFE[lfe]' \
  -map '[lfe]' lfe.wav
```

### Merge L and R back together after independent processing

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex 'channelsplit=channel_layout=stereo[L][R];[L]highpass=f=200[Lp];[R]lowpass=f=8000[Rp];[Lp][Rp]amerge' \
  output.mp3
```

## Notes

- Specifying a `channel_layout` that doesn't match the actual input will result in a mismatch error — use `ffprobe` to check input channel layout first.
- Use `channels=all` (default) to extract every channel individually; use a named subset like `FL+FR` to extract only specific channels.
- The number and order of output pads matches the channels in the order specified by `channels`.
- To recombine split channels, use `amerge` (merge into multi-channel) or `join` (with explicit mapping).
