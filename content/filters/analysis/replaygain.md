+++
title = "replaygain"
description = "Scan audio and compute ReplayGain track gain and peak values for loudness normalization tagging."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "audio", "loudness", "normalization"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["ebur128", "volumedetect", "loudnorm"]
parameters = ["track_gain", "track_peak"]
cohort = 3
+++

The `replaygain` filter scans an audio stream and computes the ReplayGain track gain (in dB) and track peak values according to the ReplayGain 2.0 specification. The audio passes through unmodified; the results are printed at the end of the stream and exported as filter options. The computed values can then be written as tags to audio files so players can apply consistent loudness normalization without re-encoding.

## Quick Start

```sh
# Compute ReplayGain for a track
ffmpeg -i music.flac -af replaygain -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| track_gain | float | *(read-only)* | Exported track gain in dB after stream end. |
| track_peak | float | *(read-only)* | Exported track peak amplitude after stream end. |

## Examples

### Measure ReplayGain and print to stderr

```sh
ffmpeg -i music.mp3 -af replaygain -f null - 2>&1 | grep -E "track_gain|track_peak"
```

### Batch scan a folder

```sh
for f in *.flac; do
  echo "$f:" && ffmpeg -i "$f" -af replaygain -f null - 2>&1 | grep track_gain
done
```

### Combined with ebur128 for comparison

```sh
ffmpeg -i music.flac -af "replaygain,ebur128" -f null -
```

## Notes

- ReplayGain targets **89 dB SPL** (equivalent to −14 LUFS approximately), while EBU R128 targets −23 LUFS. They produce different normalization values for the same file.
- The filter only measures; use a tagging tool (e.g., `metaflac`, `mp3gain`) or `ffmpeg -metadata` to write the computed values into the file.
- `track_gain` is a negative value for loud content (e.g., `-3.2 dB`) and positive for quiet content.
- For streaming and broadcast use, `ebur128` + `loudnorm` following the −23 LUFS EBU R128 target is generally preferred over ReplayGain.
