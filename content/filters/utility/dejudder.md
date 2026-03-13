+++
title = "dejudder"
description = "Remove judder from video with uneven frame durations, typically introduced by inverse telecine or mixed-cadence sources."
date = 2024-01-01

[taxonomies]
category = ["utility"]
tags = ["utility", "video", "judder", "timing", "telecine"]

[extra]
filter_type = "utility"
since = ""
see_also = ["pullup", "fieldmatch", "decimate"]
parameters = ["cycle"]
cohort = 3
source_file = "libavfilter/vf_dejudder.c"
+++

The `dejudder` filter removes judder from video that has uneven frame durations due to telecine conversion or mixed-cadence sources. Judder is the irregular motion stutter that appears when 24fps film is converted to 29.97fps (NTSC) without proper 3:2 cadence handling — frames alternate between 2-field and 3-field durations. `dejudder` detects the repeating cadence pattern and smooths the output timing. It may change the container's recorded frame rate.

## Quick Start

```sh
# Remove NTSC telecine judder
ffmpeg -i juddering.ts -vf "pullup,dejudder" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cycle | int | `4` | Length of the judder cycle in frames. `4` = 24→30fps NTSC; `5` = 25→30fps PAL; `20` = mixed. |

## Examples

### Remove NTSC 3:2 pulldown judder

```sh
ffmpeg -i ntsc_judder.ts -vf "pullup,dejudder" clean.mp4
```

### Remove PAL 25→30 pulldown judder

```sh
ffmpeg -i pal_judder.ts -vf "dejudder=cycle=5" clean.mp4
```

### Full IVTC pipeline with dejudder

```sh
ffmpeg -i telecined.ts -vf "fieldmatch,dejudder,fps=30000/1001,decimate" progressive.mp4
```

## Notes

- `dejudder` on its own does not remove duplicate frames — it only corrects the timing. Pair with `decimate` or `fps` to also remove duplicates.
- `cycle=4` is for the classic 24fps NTSC conversion (2 frames at 2 fields, 1 frame at 3 fields repeating over 4 frames).
- Aside from frame rate changes in metadata, `dejudder` has no effect on constant-frame-rate video.
- This filter is safe to apply as part of a post-`pullup` pipeline to clean up any residual timing irregularities.
