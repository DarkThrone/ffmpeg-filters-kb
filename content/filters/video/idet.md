+++
title = "idet"
description = "Detect whether video is interlaced or progressive, and identify field order (top-first or bottom-first) and repeated fields."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["interlace", "analysis", "detection"]

[extra]
filter_type = "video"
since = ""
see_also = ["yadif", "bwdif", "fieldorder"]
parameters = ["intl_thres", "prog_thres", "rep_thres", "half_life", "analyze_interlaced_flag"]
cohort = 2
+++

The `idet` filter analyzes video frames and reports whether the content is interlaced (top-field-first or bottom-field-first), progressive, or contains repeated fields (a sign of telecine). It outputs frame classification metadata and cumulative statistics, making it useful for quality control and automated pipeline decisions about whether to apply deinterlacing.

## Quick Start

```sh
# Analyze interlacing and print statistics to stderr
ffmpeg -i input.mp4 -vf "idet" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| intl_thres | float | `1.04` | Threshold for classifying a frame as interlaced. |
| prog_thres | float | `1.5` | Threshold for classifying a frame as progressive. |
| rep_thres | float | `3.0` | Threshold for detecting repeated fields (telecine). |
| half_life | float | `0` | Frames after which a past frame's contribution is halved. 0 = all frames have equal weight. |
| analyze_interlaced_flag | int | `0` | Frames to analyze to verify the interlaced flag accuracy. |

## Examples

### Detect interlacing and print results

```sh
ffmpeg -i input.ts -vf "idet" -f null - 2>&1 | tail -5
```

### Use idet to clean up incorrect interlaced flags

```sh
ffmpeg -i input.mp4 -vf "idet=analyze_interlaced_flag=20" -f null -
```

### Pipe idet results for scripting

```sh
ffmpeg -i input.mp4 -vf "idet" -f null - 2>&1 | grep "Multi frame detection"
```

### Conditional deinterlace pipeline

```sh
# First check, then apply yadif if interlaced
ffmpeg -i input.ts -vf "idet,yadif=mode=0:deint=interlaced" output.mp4
```

## Notes

- `idet` logs per-frame metadata (`lavfi.idet.single.*` and `lavfi.idet.multiple.*`) and prints cumulative statistics at end-of-stream.
- Single-frame detection classifies each frame independently; multiple-frame detection incorporates history for more stable results.
- `half_life=0` means all frames are weighted equally forever; set a small value (e.g. 1 second worth of frames) for a sliding-window view.
- When `analyze_interlaced_flag > 0`, `idet` verifies whether the stream's built-in interlaced flag is accurate; if inaccurate, it is cleared.
- Chain with `yadif=deint=interlaced` to deinterlace only the frames idet identifies as interlaced.
