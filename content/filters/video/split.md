+++
title = "split"
description = "Duplicate the input video stream into N identical output streams for use in branching filtergraphs."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["routing", "split", "filtergraph"]

[extra]
filter_type = "video"
since = ""
see_also = ["concat", "overlay", "select"]
parameters = ["outputs"]
cohort = 1
+++

The `split` filter takes a single input video stream and produces N identical copies of it. This is essential in filtergraph pipelines where the same source needs to feed multiple downstream filters simultaneously — for example, creating a preview thumbnail alongside the main encode, or constructing a side-by-side comparison. The audio equivalent is `asplit`. The default number of outputs is 2.

## Quick Start

```sh
ffmpeg -i input.mp4 -filter_complex "[0:v]split[a][b]; [a]scale=640:360[small]; [b]scale=1920:1080[large]" \
  -map "[small]" small.mp4 -map "[large]" large.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outputs | int | `2` | Number of output streams to produce. |

## Examples

### Split into two outputs for multi-resolution encoding

Decode once and encode to two different resolutions simultaneously.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[a][b]; [a]scale=1280:720[hd]; [b]scale=640:360[sd]" \
  -map "[hd]" hd.mp4 \
  -map "[sd]" sd.mp4
```

### Split and apply different filters to each branch

Apply different filters (e.g., grayscale and original) to two copies of the same stream.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][gray]; [gray]hue=s=0[bw]" \
  -map "[orig]" color.mp4 \
  -map "[bw]" bw.mp4
```

### Split into three outputs

Specify the count explicitly when you need more than two branches.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split=3[a][b][c]; [a]scale=1920:1080[fhd]; [b]scale=1280:720[hd]; [c]scale=640:360[sd]" \
  -map "[fhd]" fhd.mp4 -map "[hd]" hd.mp4 -map "[sd]" sd.mp4
```

### Crop one branch and stack side by side

Use split to create a side-by-side comparison between original and cropped versions.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][tocrop]; [tocrop]crop=iw/2:ih:0:0[cropped]; [orig][cropped]hstack" \
  output.mp4
```

## Notes

- Each output branch receives reference-counted frames from the same decoded source, so `split` does not significantly increase memory usage for read-only operations.
- When downstream branches apply different filters, each branch may buffer frames independently, which can increase memory for high-resolution or long-GOP content.
- The audio equivalent, `asplit`, works identically for audio streams.
- `split` is required in filtergraph syntax; simply connecting one pad to two different filters is not valid — you must use `split` explicitly.
