+++
title = "volumedetect"
description = "Analyze audio and report mean volume, maximum volume, and a histogram of sample levels at the end of the stream."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "audio", "loudness", "volume"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["ebur128", "replaygain", "volume"]
parameters = []
cohort = 3
+++

The `volumedetect` filter scans an audio stream and prints the mean volume (RMS), maximum sample volume, and a histogram of level distribution at the end of the stream. It is the simplest way to determine how much headroom a file has before clipping — essential before normalizing with the `volume` filter. The audio passes through unchanged; there are no parameters to configure.

## Quick Start

```sh
# Detect volume stats for a file
ffmpeg -i input.wav -af volumedetect -f null -
```

## Parameters

None. `volumedetect` has no configurable options.

## Examples

### Print volume stats for a file

```sh
ffmpeg -i input.mp3 -af volumedetect -f null - 2>&1 | grep volume
```

### Determine safe normalization gain

```sh
# max_volume will show the headroom; use it as input to -af volume
ffmpeg -i input.wav -af volumedetect -f null - 2>&1 | grep max_volume
# Then normalize:
ffmpeg -i input.wav -af "volume=6dB" normalized.wav
```

### Batch volume scan

```sh
for f in *.mp3; do
  echo "$f:" && ffmpeg -i "$f" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
done
```

### Check whether audio will clip at a given gain

```sh
# If max_volume is -4dB, adding more than +4dB will clip
ffmpeg -i loud.wav -af volumedetect -f null - 2>&1 | grep max_volume
```

## Notes

- Output includes `mean_volume` (RMS in dBFS), `max_volume` (peak sample in dBFS), and a histogram like `histogram_4db: 6` (6 samples within −4 to −5 dBFS).
- If `max_volume` is, say, −4 dB, you can safely apply up to +4 dB gain without clipping.
- For broadcast loudness compliance, use `ebur128` instead — it measures integrated loudness (LUFS), not peak.
- Only supports 16-bit signed integer samples natively; the filter adds an implicit format conversion if needed.
