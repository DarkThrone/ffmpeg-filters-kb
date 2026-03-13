+++
title = "copy"
description = "Pass video frames through unchanged — a null operation useful for testing and filter graph anchoring."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["utility", "passthrough"]

[extra]
filter_type = "video"
since = ""
see_also = ["null"]
parameters = []
cohort = 2
source_file = "libavfilter/vf_copy.c"
+++

The `copy` filter passes every video frame through without any modification. It has no parameters and performs no transformation. Its primary uses are: verifying that a filter graph is connected correctly, benchmarking the overhead of the filter graph itself, and forcing a frame copy when sharing the same buffer between multiple filter chains would cause issues.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "copy" output.mp4
```

## Examples

### Passthrough with re-encode

```sh
ffmpeg -i input.mp4 -vf "copy" -c:v libx264 output.mp4
```

### Force a copy in filter_complex

```sh
ffmpeg -i input.mp4 -filter_complex "[0:v]copy[out]" -map "[out]" output.mp4
```

## Notes

- `copy` is the video equivalent of the `anull` audio filter: it does nothing to the data but is a valid node in a filter graph.
- In most cases you do not need `copy`; `-vf ""` (empty filter) or simply omitting `-vf` achieves the same result.
- It can be useful for benchmarking: `ffmpeg -i input.mp4 -vf "copy" -f null -` measures the muxing/filter overhead without any actual processing.
