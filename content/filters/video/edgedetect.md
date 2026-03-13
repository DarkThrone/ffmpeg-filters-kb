+++
title = "edgedetect"
description = "Detect and visualize edges in video using Canny edge detection or color mixing."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["edge-detection", "analysis", "effect"]

[extra]
filter_type = "video"
since = ""
see_also = []
parameters = ["high", "low", "mode", "planes"]
cohort = 2
+++

The `edgedetect` filter detects edges in video frames using the Canny algorithm, with multiple output modes for creative and analytical use. In `wires` mode, it produces a classic edge-detection output (bright lines on black). In `colormix` mode, it blends the edge signal with the original video for an artistic effect.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.1:high=0.4" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| high | double | `0.12` | High threshold for Canny hysteresis (0–1). Pixels above this are definite edges. |
| low | double | `0.08` | Low threshold for Canny hysteresis. Pixels between low and high are edges only if adjacent to a definite edge. |
| mode | int | `wires` | Output mode: `wires` (edges on black bg), `colormix` (blend edges with source), `canny` (raw Canny output). |
| planes | flags | `7` | Which planes to apply edge detection on. 1=Y, 2=Cb, 4=Cr. |

## Examples

### Classic white edges on black background

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.05:high=0.2:mode=wires" output.mp4
```

### Artistic colormix edge effect

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.1:high=0.3:mode=colormix" output.mp4
```

### Fine detail edge map for luma only

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.02:high=0.1:planes=1" output.mp4
```

### High threshold for strong edges only

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.2:high=0.5" output.mp4
```

## Notes

- The Canny algorithm uses hysteresis: pixels above `high` are strong edges; pixels above `low` that are connected to strong edges are also kept. This produces cleaner, continuous edge lines than a simple threshold.
- Lower `low`/`high` values detect more (and weaker) edges; higher values detect only the strongest edges.
- `mode=wires` is most useful for visualization and artistic effects; `mode=canny` outputs the raw Canny gradient for analytical use.
- Combine with `negate` after `wires` mode for dark-edge-on-light-background sketch effect.
