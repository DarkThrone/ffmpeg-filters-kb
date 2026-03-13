+++
title = "vmafmotion"
description = "Compute the VMAF motion score per frame — a per-frame motion metric that is one component of the VMAF video quality model."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "quality", "vmaf", "motion"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["psnr", "ssim", "siti"]
parameters = ["stats_file"]
cohort = 3
source_file = "libavfilter/vf_vmafmotion.c"
+++

The `vmafmotion` filter computes the VMAF motion score — a per-frame temporal motion metric that is one of the sub-features used in Netflix's VMAF (Video Multi-method Assessment Fusion) model. It measures the mean absolute difference between consecutive frames after a low-pass filter. The filter passes video through unchanged and logs the mean motion score at the end. Per-frame scores can be written to a file.

## Quick Start

```sh
# Print average VMAF motion score
ffmpeg -i input.mp4 -vf vmafmotion -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file | string | — | Path to write per-frame motion scores. Use `-` to write to stdout. |

## Examples

### Print average motion score to log

```sh
ffmpeg -i input.mp4 -vf vmafmotion -f null - 2>&1 | grep motion
```

### Save per-frame scores to a file

```sh
ffmpeg -i input.mp4 -vf "vmafmotion=stats_file=motion.txt" -f null -
```

### Print to stdout (pipe to awk for averaging)

```sh
ffmpeg -i input.mp4 -vf "vmafmotion=stats_file=-" -f null - 2>/dev/null | \
  awk '{sum+=$NF; n++} END {print "mean:", sum/n}'
```

## Notes

- The VMAF motion score is correlated with perceived motion blur and temporal complexity — high scores indicate fast-moving content.
- This is a **single-stream** filter (no reference video needed), unlike full VMAF which requires a reference/distorted pair.
- For full VMAF quality measurement, use the `libvmaf` filter with a reference stream.
- Scores are typically in the range 0–20; action scenes often score 5–15, static content near 0.
