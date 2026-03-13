+++
title = "tinterlace"
description = "Perform temporal field interlacing with multiple modes — merge progressive frames into interlaced output, drop fields, or pad with blank lines."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "broadcast", "fields"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["interlace", "fieldorder", "telecine"]
parameters = ["mode", "flags", "scan", "lowpass"]
cohort = 3
source_file = "libavfilter/vf_tinterlace.c"
+++

The `tinterlace` filter provides fine-grained temporal field interlacing with multiple operational modes. It can weave fields from consecutive frames into interlaced output (`merge`), drop alternate frames, pad frames with blank lines, or interleave in various patterns. It is the multi-mode predecessor to the simpler `interlace` filter and offers more flexibility for broadcast encoding workflows.

## Quick Start

```sh
# Merge progressive 50fps frames into 25i interlaced
ffmpeg -i progressive_50fps.mp4 -vf tinterlace -r 25 interlaced.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `merge` | Interlacing mode (see table below). |
| flags | flags | — | Additional flags: `vlpf` (vertical low-pass filter). |
| scan | int | `tff` | Field order for modes that need it: `tff` or `bff`. |
| lowpass | int | `linear` | Vertical low-pass filter: `off`, `linear`, `complex`. |

## Modes

| Mode | Value | Description |
|------|-------|-------------|
| `merge` | 0 | Weave odd frames (upper field) + even frames (lower field); halves framerate, doubles height. |
| `drop_even` | 1 | Output only odd frames, drop even; halves framerate. |
| `drop_odd` | 2 | Output only even frames, drop odd; halves framerate. |
| `pad` | 3 | Expand each frame to full height with alternate blank lines; same framerate. |
| `interleave_top` | 4 | Interleave top field from odd, bottom from even. |
| `interleave_bottom` | 5 | Interleave bottom field from odd, top from even. |
| `interlacex2` | 6 | Move fields to separate frames; doubles framerate. |
| `mergex2` | 7 | Same as `merge` but keep framerate by doubling. |

## Examples

### Merge progressive frames into interlaced

```sh
ffmpeg -i 50fps_progressive.mp4 -vf "tinterlace=mode=merge" -r 25 output.ts
```

### Apply vertical low-pass to reduce twitter

```sh
ffmpeg -i input.mp4 -vf "tinterlace=mode=merge:lowpass=complex" output.ts
```

### Drop even frames for simple frame rate conversion

```sh
ffmpeg -i 60fps.mp4 -vf "tinterlace=mode=drop_even" 30fps.mp4
```

## Notes

- `lowpass=complex` reduces interlace twitter and moiré better than `linear` but at a slight sharpness cost.
- For simple progressive-to-interlaced encoding, the simpler `interlace` filter is often sufficient.
- `mode=merge` is the classic interlacing operation used for broadcast delivery.
