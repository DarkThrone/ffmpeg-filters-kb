+++
title = "scdet"
description = "Detect scene changes in video and output scene change scores as frame metadata."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["scene-detection", "analysis"]

[extra]
filter_type = "video"
since = ""
see_also = ["select"]
parameters = ["threshold", "sc_pass"]
cohort = 2
source_file = "libavfilter/vf_scdet.c"
+++

The `scdet` filter detects scene changes in video by computing the difference between consecutive frames. It writes a `lavfi.scene_score` metadata value (0–100) to each frame. Frames with a score above the threshold are considered scene changes and can be extracted or processed separately by chaining with the `select` filter.

## Quick Start

```sh
# Detect scene changes and print timestamps to stderr
ffmpeg -i input.mp4 -vf "scdet" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| threshold / t | double | `10.0` | Scene change score threshold (0–100). Frames above this score are flagged as scene changes. |
| sc_pass / s | bool | `0` | If true, only pass frames that are flagged as scene changes to the output. |

## Examples

### Detect and log all scene changes

```sh
ffmpeg -i input.mp4 -vf "scdet=threshold=10" -f null - 2>&1 | grep "scene_score"
```

### Extract only scene change frames as JPEG thumbnails

Use `scdet` to detect, then `select` to filter.

```sh
ffmpeg -i input.mp4 \
  -vf "scdet=threshold=8,select='gte(scene_score,8)'" \
  -vsync vfr scene_%04d.jpg
```

### Adjust threshold for detecting only large scene changes

```sh
ffmpeg -i documentary.mp4 -vf "scdet=threshold=25" -f null -
```

### Output only scene change frames (sc_pass mode)

```sh
ffmpeg -i input.mp4 -vf "scdet=t=10:s=1" -vsync vfr scenes_%04d.png
```

## Notes

- `lavfi.scene_score` is set on every frame; values approaching 100 indicate very different consecutive frames (hard cuts). Values of 10–20 are typical for gradual transitions.
- Lower threshold → more scene changes detected (including gradual transitions and camera moves); higher threshold → only hard cuts.
- The `select` filter can read the `scene_score` metadata: `select='gt(scene_score\\,0.3)'` (note the backslash escape in shell).
- `sc_pass=1` drops all non-scene-change frames — use with `-vsync vfr` to preserve timestamps when outputting image sequences.
