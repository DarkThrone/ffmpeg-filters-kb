+++
title = "yadif"
description = "Deinterlace video using the 'Yet Another Deinterlacing Filter' with spatial and temporal analysis."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["deinterlace", "interlace"]

[extra]
filter_type = "video"
since = ""
see_also = ["bwdif"]
parameters = ["mode", "parity", "deint"]
cohort = 2
source_file = "libavfilter/vf_yadif.c"
+++

The `yadif` filter ("Yet Another Deinterlacing Filter") removes interlacing artifacts from video by blending or reconstructing missing lines using spatial and temporal information from adjacent frames. It is the most commonly used deinterlacing filter in FFmpeg, offering a good balance of quality and speed. For higher quality, see `bwdif`.

## Quick Start

```sh
ffmpeg -i interlaced.mp4 -vf "yadif" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `0` | Output mode: `0`=send_frame (one output per input frame), `1`=send_field (one output per field, doubles frame rate), `2`=send_frame_nospatial (skip spatial check), `3`=send_field_nospatial. |
| parity | int | `-1` | Field parity: `0`=top field first (tff), `1`=bottom field first (bff), `-1`=auto-detect (recommended). |
| deint | int | `0` | Which frames to deinterlace: `0`=all frames, `1`=only frames marked as interlaced. |

## Examples

### Basic deinterlacing (one output frame per input frame)

```sh
ffmpeg -i interlaced.mp4 -vf "yadif=0" output.mp4
```

### Double-rate deinterlacing (one frame per field)

Outputs twice as many frames; useful for producing smooth 50/60fps from 25/30i.

```sh
ffmpeg -i interlaced.mp4 -vf "yadif=1" output.mp4
```

### Deinterlace only flagged interlaced frames

Pass progressive frames through unchanged.

```sh
ffmpeg -i mixed.mp4 -vf "yadif=deint=1" output.mp4
```

### Deinterlace with explicit top-field-first parity

```sh
ffmpeg -i interlaced.ts -vf "yadif=mode=0:parity=0" output.mp4
```

## Notes

- `mode=0` (send_frame) is the standard choice: it outputs the same number of frames as the input, with each interlaced frame reconstructed into one progressive frame.
- `mode=1` (send_field) outputs one frame per field, doubling the frame rate. Use with `-r` or `fps` to set the output frame rate.
- When `parity=-1` (auto), yadif reads the field order from the container metadata. If the interlacing is undetected, set it explicitly with `parity=0` (tff) or `parity=1` (bff).
- For broadcast material or high-quality deinterlacing, `bwdif` produces better motion rendering, especially on fast motion.
