+++
title = "bwdif"
description = "Deinterlace video using the motion-adaptive Bob Weaver Deinterlacing Filter for superior quality."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["deinterlace", "interlace", "motion-adaptive"]

[extra]
filter_type = "video"
since = ""
see_also = ["yadif"]
parameters = ["mode", "parity", "deint"]
cohort = 2
source_file = "libavfilter/vf_bwdif.c"
+++

The `bwdif` filter ("Bob Weaver Deinterlacing Filter") is a motion-adaptive deinterlacer that uses temporal and spatial information to reconstruct missing lines. It generally produces cleaner results than `yadif` on fast motion, with fewer combing artifacts. It accepts the same parameters as `yadif` and can be used as a drop-in replacement.

## Quick Start

```sh
ffmpeg -i interlaced.mp4 -vf "bwdif" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `1` | Output mode: `0`=send_frame (one output per input frame), `1`=send_field (one output per field, doubles frame rate). |
| parity | int | `-1` | Field parity: `0`=top field first, `1`=bottom field first, `-1`=auto-detect. |
| deint | int | `0` | Which frames to deinterlace: `0`=all, `1`=only flagged interlaced frames. |

## Examples

### Standard deinterlacing

One progressive frame per input frame (default mode=1 outputs per field — use mode=0 for 1:1).

```sh
ffmpeg -i interlaced.mp4 -vf "bwdif=mode=0" output.mp4
```

### Double-rate output (field-based)

Output one frame per field for smooth high-frame-rate playback.

```sh
ffmpeg -i interlaced.ts -vf "bwdif=mode=1" -r 50 output.mp4
```

### Explicit BFF parity

```sh
ffmpeg -i bff_source.mp4 -vf "bwdif=mode=0:parity=1" output.mp4
```

## Notes

- `bwdif` is generally preferred over `yadif` when quality matters; it handles fast motion and fine diagonal edges better.
- The default `mode=1` (send_field) doubles the output frame rate. For 1:1 frame mapping, set `mode=0`.
- Like `yadif`, set `deint=1` to only deinterlace frames tagged as interlaced, passing through progressive frames unchanged.
- On hardware-accelerated pipelines (e.g. NVENC), use the vendor-specific deinterlacer instead, as software filters run on CPU.
