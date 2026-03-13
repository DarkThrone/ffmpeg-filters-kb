+++
title = "interlace"
description = "Interleave fields from consecutive progressive frames to produce interlaced video, halving the frame rate while preserving spatial resolution."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "broadcast", "fields"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["tinterlace", "fieldorder", "yadif"]
parameters = ["scan", "lowpass"]
cohort = 3
source_file = "libavfilter/vf_tinterlace.c"
+++

The `interlace` filter converts progressive video to interlaced output by interleaving alternating lines from two consecutive input frames. This halves the output frame rate while keeping the full spatial resolution. It is used for broadcast delivery when a progressive source needs to be encoded as interlaced (e.g., 50p → 25i, 60p → 30i). A vertical low-pass filter is available to prevent interlace twitter artifacts.

## Quick Start

```sh
# Convert 50fps progressive to 25i interlaced
ffmpeg -i input_50fps.mp4 -vf interlace output_25i.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scan | int | `tff` | Field order: `tff` (top field first) or `bff` (bottom field first). |
| lowpass | int | `linear` | Vertical low-pass filter: `off`, `linear`, `complex`. |

## Examples

### 50fps progressive to 25i TFF (PAL broadcast)

```sh
ffmpeg -i source_50fps.mp4 -vf interlace -r 25 broadcast.ts
```

### 60fps progressive to 30i BFF

```sh
ffmpeg -i source_60fps.mp4 -vf "interlace=scan=bff" -r 30 broadcast.ts
```

### With complex low-pass to reduce moiré

```sh
ffmpeg -i input_50fps.mp4 -vf "interlace=lowpass=complex" -r 25 output.ts
```

## Notes

- `scan=tff` (top-field-first) is standard for most broadcast formats; use `bff` for formats that specify bottom-field-first (e.g., some DV/DVCPro).
- `lowpass=complex` is better at retaining detail with less twitter than `linear`, but is slightly more expensive.
- This filter interleaves fields from frames j and j+1 — the output frame contains lines 0,2,4… from frame j and lines 1,3,5… from frame j+1.
- For a more feature-rich version with additional modes, see `tinterlace`.
