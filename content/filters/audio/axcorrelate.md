+++
title = "axcorrelate"
description = "Compute the normalized cross-correlation between two audio streams over a sliding window, producing a correlation signal (-1 to +1) useful for sync detection."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["audio", "analysis", "correlation", "sync", "stereo"]

[extra]
filter_type = "audio"
since = ""
see_also = ["aphasemeter", "ebur128", "silencedetect"]
parameters = ["size", "algo"]
cohort = 3
source_file = "libavfilter/af_axcorrelate.c"
+++

The `axcorrelate` filter computes the normalized windowed cross-correlation between two input audio streams. The output value for each window ranges from −1 to +1: `+1` means the two inputs are identical in that window, `0` means uncorrelated, and `−1` means they are exactly out of phase (cancel each other when summed). It is used for audio synchronization detection, checking mono compatibility, and analyzing the relationship between two recordings of the same event.

## Quick Start

```sh
# Check correlation between left and right channels of stereo audio
ffmpeg -i stereo.wav -af "channelsplit,axcorrelate=size=1024" correlation.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size | int | `256` | Segment size in samples (2–131072). Larger = smoother, less time resolution. |
| algo | int | `best` | Algorithm: `slow` (accurate), `fast` (assumes zero mean), `best` (auto-select). |

## Examples

### Stereo channel correlation check

```sh
ffmpeg -i stereo.wav -af "channelsplit,axcorrelate=size=1024:algo=fast" correlation.wav
```

### Check sync between two recordings

```sh
ffmpeg -i recording1.wav -i recording2.wav \
  -filter_complex "[0:a][1:a]axcorrelate=size=4096" correlation.wav
```

### Print correlation values to stdout

```sh
ffmpeg -i stereo.wav \
  -af "channelsplit,axcorrelate=size=512,metadata=print:file=-" \
  -f null - 2>/dev/null
```

## Notes

- Output of `+1` throughout indicates the two streams are identical (or one is a scaled copy of the other).
- Output near `−1` means the streams cancel when summed to mono — problematic for broadcast mono downmix.
- `algo=fast` assumes signal mean is zero (valid for typical audio) and is significantly faster than `algo=slow`.
- For stereo phase visualization, `aphasemeter` provides a Lissajous display of the same relationship.
