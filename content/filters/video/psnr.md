+++
title = "psnr"
description = "Calculate the Peak Signal-to-Noise Ratio (PSNR) quality metric between two video streams."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["quality-metric", "analysis"]

[extra]
filter_type = "video"
since = ""
see_also = ["ssim"]
parameters = ["stats_file", "stats_version", "output_max"]
cohort = 2
+++

The `psnr` filter computes the Peak Signal-to-Noise Ratio between two video streams — typically an original and a compressed or processed version. Higher PSNR (in dB) indicates less distortion. The filter outputs per-frame PSNR values to a file or stderr while passing the first stream through unchanged, making it useful for codec quality evaluation and comparison.

## Quick Start

```sh
# Compare original and encoded video; print PSNR to stderr
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file / f | string | — | Path to a file where per-frame PSNR statistics are written. If omitted, summary is printed to stderr. |
| stats_version | int | `1` | Format version for the stats file (1 or 2). Version 2 adds more columns. |
| output_max | bool | `0` | If enabled, also log the maximum PSNR value. |

## Examples

### Print PSNR summary to stderr

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr" -f null -
```

### Save per-frame PSNR to a log file

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr=stats_file=psnr.log" -f null -
```

### Compare H.264 encodings at different CRF values

```sh
# Encode at CRF 23
ffmpeg -i original.mp4 -c:v libx264 -crf 23 encoded_23.mp4

# Compare
ffmpeg -i original.mp4 -i encoded_23.mp4 \
  -filter_complex "[0:v][1:v]psnr=f=psnr_23.log" -f null -
```

### PSNR alongside SSIM

Compute both metrics in a single pass.

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v]split[a][b];[1:v]split[c][d];[a][c]psnr;[b][d]ssim" -f null -
```

## Notes

- PSNR is reported in dB. Values above 40 dB are generally considered visually lossless; 30–40 dB is acceptable quality; below 30 dB is noticeably degraded.
- The first input (`[0:v]`) is the reference; the second (`[1:v]`) is the test. The first stream is passed through to the output unchanged.
- Use `-f null -` as the output to discard the video output and only collect statistics.
- PSNR correlates imperfectly with perceptual quality — `ssim` is a better perceptual metric for most use cases.
