+++
title = "ssim"
description = "Calculate the Structural Similarity Index (SSIM) between two video streams as a perceptual quality metric."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["quality-metric", "analysis"]

[extra]
filter_type = "video"
since = ""
see_also = ["psnr"]
parameters = ["stats_file"]
cohort = 2
source_file = "libavfilter/vf_ssim.c"
+++

The `ssim` filter computes the Structural Similarity Index Measure (SSIM) between two video streams — typically an original and a processed/compressed copy. SSIM is a perceptual quality metric that models human visual perception better than PSNR by comparing luminance, contrast, and structure. It produces values between 0 and 1, where 1 is identical and values above 0.95 are generally considered high quality.

## Quick Start

```sh
# Compare original and encoded; print SSIM to stderr
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file / f | string | — | File path to write per-frame SSIM statistics. Prints summary to stderr if omitted. |

## Examples

### Print SSIM to stderr

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim" -f null -
```

### Save per-frame SSIM values to a file

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim=stats_file=ssim.log" -f null -
```

### Compare two codec settings side by side

```sh
# Encode at two quality levels
ffmpeg -i original.mp4 -c:v libx264 -crf 23 crf23.mp4
ffmpeg -i original.mp4 -c:v libx264 -crf 35 crf35.mp4

# Compare both against original
ffmpeg -i original.mp4 -i crf23.mp4 -filter_complex "[0:v][1:v]ssim=f=ssim_23.log" -f null -
ffmpeg -i original.mp4 -i crf35.mp4 -filter_complex "[0:v][1:v]ssim=f=ssim_35.log" -f null -
```

### Compute SSIM and PSNR in a single pass

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v]split[a][b];[1:v]split[c][d];[a][c]psnr;[b][d]ssim" \
  -f null -
```

## Notes

- SSIM values: 1.0 = identical, >0.95 = high quality, 0.90–0.95 = acceptable, <0.90 = noticeable degradation.
- SSIM is generally more aligned with human perception than PSNR, especially for compression artifacts and blur.
- The first input (`[0:v]`) is the reference; the second (`[1:v]`) is the test stream. The first stream passes through unchanged to the output.
- Use `-f null -` as the output to discard the video and only collect statistics.
