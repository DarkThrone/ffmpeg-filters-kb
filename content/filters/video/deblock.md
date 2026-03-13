+++
title = "deblock"
description = "Remove blocking artifacts from heavily compressed video by detecting and smoothing block edges."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["deblock", "compression", "artifact-removal"]

[extra]
filter_type = "video"
since = ""
see_also = ["smartblur", "median"]
parameters = ["filter", "block", "alpha", "beta", "gamma", "delta", "planes"]
cohort = 2
source_file = "libavfilter/vf_deblock.c"
+++

The `deblock` filter removes the blocky artifacts introduced by strong video compression (such as low-bitrate H.264 or MPEG-2). It detects block boundaries by looking for step edges at regular intervals and smooths them, with configurable thresholds to avoid blurring actual scene edges.

## Quick Start

```sh
ffmpeg -i blocky.mp4 -vf "deblock" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filter | int | `strong` | Filter type: `weak` or `strong`. Strong gives more deblocking. |
| block | int | `8` | Block size in pixels. Range: 4–512. Should match compression block size. |
| alpha | float | `0.098` | Detection threshold at exact block edge. 0 disables. |
| beta | float | `0.05` | Detection threshold near block edge (below/left). |
| gamma | float | `0.05` | Detection threshold near block edge (above). |
| delta | float | `0.05` | Detection threshold near block edge (right). |
| planes | int | `15` | Bitmask of planes to filter (15 = all). |

## Examples

### Standard deblocking for H.264 video

```sh
ffmpeg -i compressed.mp4 -vf "deblock=filter=strong:block=8" output.mp4
```

### Weak filter for mild artifacts

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=weak:block=4" output.mp4
```

### Aggressive deblocking with custom thresholds

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=strong:block=4:alpha=0.12:beta=0.07:gamma=0.06:delta=0.05" output.mp4
```

### Deblock only luma plane

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=strong:block=8:planes=1" output.mp4
```

### Target 16×16 macroblocks (MPEG-2)

```sh
ffmpeg -i mpeg2.mpg -vf "deblock=block=16:filter=strong" output.mp4
```

## Notes

- Set `block` to match the encoder's block size: 8×8 for H.264/H.265, 16×16 for MPEG-2.
- Higher threshold values (`alpha`, `beta`, `gamma`, `delta`) give stronger deblocking but risk blurring real edges. Start with defaults.
- Setting any threshold to 0 disables deblocking along that specific edge direction.
- `strong` filter works at both the block edge and within adjacent blocks; `weak` only smooths the edge itself.
