+++
title = "concat"
description = "Concatenate multiple audio/video segments end-to-end into a single continuous stream."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["concat", "join", "segment"]

[extra]
filter_type = "video"
since = ""
see_also = ["trim", "split", "setpts"]
parameters = ["n", "v", "a", "unsafe"]
cohort = 1
+++

The `concat` filter joins multiple synchronized video (and optionally audio) segments sequentially, producing a single continuous output stream. Unlike file-level concatenation, `concat` works inside the filtergraph, which allows you to filter each segment independently before joining. All segments must start at timestamp 0, have the same stream count per type, and matching resolution and format (or be explicitly normalized beforehand). The filter handles slight audio/video duration mismatches by padding the shorter stream with silence.

## Quick Start

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" \
  -map "[v]" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| n | int | `2` | Number of segments (input groups) to concatenate. |
| v | int | `1` | Number of video output streams (must equal the number of video streams per segment). |
| a | int | `0` | Number of audio output streams (must equal the number of audio streams per segment). |
| unsafe | bool | `0` | Allow segments with different formats to be concatenated without failing. |

### Input/output pad layout

The filter has `n x (v + a)` inputs and `v + a` outputs. Inputs are ordered: all streams for segment 1 first, then segment 2, etc. Within each segment, video streams come before audio streams.

## Examples

### Concatenate two video-only clips

Join two clips that share the same resolution and format.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" \
  -map "[outv]" output.mp4
```

### Concatenate two clips with audio

Handle both video and audio streams from each segment.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Concatenate three clips with bilingual audio

Each segment has one video stream and two audio streams.

```sh
ffmpeg -i open.mkv -i ep.mkv -i end.mkv \
  -filter_complex \
    "[0:0][0:1][0:2][1:0][1:1][1:2][2:0][2:1][2:2]concat=n=3:v=1:a=2[v][a1][a2]" \
  -map "[v]" -map "[a1]" -map "[a2]" output.mkv
```

### Normalize resolutions before concatenating

Scale both clips to the same resolution before `concat` to avoid errors.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex \
    "[0:v]scale=1280:720,setpts=PTS-STARTPTS[v1]; \
     [1:v]scale=1280:720,setpts=PTS-STARTPTS[v2]; \
     [v1][v2]concat=n=2:v=1:a=0[v]" \
  -map "[v]" output.mp4
```

## Notes

- Every segment must begin at timestamp 0. Insert `setpts=PTS-STARTPTS` (and `asetpts=PTS-STARTPTS` for audio) before `concat` if your segments were trimmed or have non-zero start times.
- All corresponding streams across segments must have the same resolution, pixel format, sample rate, and channel layout. Use `scale`, `format`, `aformat`, etc. to normalize before concatenating.
- The `concat` filter adjusts for slight duration differences between synchronized video and audio within a segment by padding the shorter stream; it cannot fix large desync issues.
- Variable frame rate output is produced if segments have different frame rates; ensure the muxer and player support VFR, or normalize with `fps` after `concat`.
