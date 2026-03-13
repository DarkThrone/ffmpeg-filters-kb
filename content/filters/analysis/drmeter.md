+++
title = "drmeter"
description = "Measure the Dynamic Range (DR) of an audio file using the crest factor method, reporting DR values per segment."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "audio", "dynamic range", "loudness"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["ebur128", "replaygain", "volumedetect"]
parameters = ["length"]
cohort = 3
source_file = "libavfilter/af_drmeter.c"
+++

The `drmeter` filter computes the Dynamic Range score popularized by the DR Loudness War database. It splits the audio into segments, computes the crest factor (peak-to-RMS ratio) for each, and derives a DR value. Higher DR indicates more dynamic, less compressed audio (DR14+ = very dynamic; DR8–13 = typical modern mastering; DR<8 = heavily limited). The audio passes through unchanged.

## Quick Start

```sh
# Measure dynamic range of a music file
ffmpeg -i music.flac -af drmeter -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| length | double | `3.0` | Window length in seconds for segment splitting. |

## Examples

### Basic DR measurement

```sh
ffmpeg -i album_track.flac -af drmeter -f null - 2>&1 | grep -i dr
```

### Shorter segments for more detail

```sh
ffmpeg -i music.wav -af "drmeter=length=1" -f null -
```

### Compare two masters

```sh
for f in original.wav loudness_war.wav; do
  echo "=== $f ===" && ffmpeg -i "$f" -af drmeter -f null - 2>&1 | grep DR
done
```

## Notes

- DR14+ is found in acoustic, jazz, and classical recordings with natural dynamics.
- DR8–13 is typical of modern pop/rock mastering.
- DR<8 indicates heavy brick-wall limiting or compression — associated with "loudness war" releases.
- The segment length (`length`) affects measurement granularity; 3 seconds is the conventional default matching the DR database tool.
