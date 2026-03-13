+++
title = "decimate"
description = "Drop duplicate frames from video to achieve the target frame rate, used as the second stage of inverse telecine after fieldmatch."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "telecine", "ivtc", "framerate"]

[extra]
filter_type = "utility"
since = ""
see_also = ["fieldmatch", "pullup", "fps"]
parameters = ["cycle", "dupthresh", "scthresh", "blockx", "blocky", "ppsrc", "chroma", "mixed"]
cohort = 3
+++

The `decimate` filter removes duplicate frames at regular intervals to reduce frame rate — the second stage of a `fieldmatch` + `decimate` IVTC pipeline. For every N frames (cycle), it identifies the most similar consecutive frame pair and drops one, effectively converting 29.97fps telecined video back to 23.976fps progressive. It can also be used independently to reduce frame rate by dropping duplicate frames in any content.

## Quick Start

```sh
# IVTC: match fields then drop duplicates (30i → 24p)
ffmpeg -i telecined.ts -vf "fieldmatch,decimate" progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cycle | int | `5` | Number of frames per group; one frame per group is dropped. Default 5 converts 30fps to 24fps. |
| dupthresh | double | `1.1` | Threshold below which a frame is considered a duplicate. |
| scthresh | double | `15.0` | Scene change detection threshold; prevents dropping across cuts. |
| blockx | int | `32` | Block width for difference metric calculations. |
| blocky | int | `32` | Block height for difference metric calculations. |
| ppsrc | bool | `0` | Use second stream as pre-processed reference for duplicate detection. |
| chroma | bool | `1` | Include chroma in duplicate detection. |
| mixed | bool | `false` | Handle input with mixed decimated and non-decimated content. |

## Examples

### Full IVTC pipeline

```sh
ffmpeg -i telecined_ntsc.ts -vf "fieldmatch,decimate" -r 24000/1001 progressive.mp4
```

### With yadif fallback for mixed content

```sh
ffmpeg -i mixed.ts -vf "fieldmatch,yadif=deint=interlaced,decimate" output.mp4
```

### Pre-processed source for better detection

```sh
ffmpeg -i input.ts \
  -filter_complex "[0:v]yadif=1[pp];[0:v][pp]fieldmatch=ppsrc=1,decimate=ppsrc=1[out]" \
  -map "[out]" output.mp4
```

### Drop every 5th duplicate frame independently

```sh
ffmpeg -i 30fps_video.mp4 -vf "decimate=cycle=5" 24fps_video.mp4
```

## Notes

- `cycle=5` = drop 1 in 5 frames: 30fps → 24fps, or 29.97fps → 23.976fps.
- A high `dupthresh` (e.g., 3.0) is more permissive about calling frames duplicates; lower values are stricter.
- Scene change detection (`scthresh`) prevents incorrectly dropping the first frame of a new scene.
- Currently requires constant frame rate input — for VFR input, prepend `fps=30000/1001` first.
