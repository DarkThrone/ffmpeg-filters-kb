+++
title = "null"
description = "Pass the input video through unchanged — a no-op filter useful for testing and filtergraph construction."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["utility", "passthrough"]

[extra]
filter_type = "video"
since = ""
see_also = ["select", "setpts", "format"]
parameters = []
cohort = 1
+++

The `null` filter passes every video frame from input to output without any modification. It is a no-op and has no effect on the video content, timestamps, or metadata. Its primary uses are in testing filtergraph pipelines, as a placeholder when a filter is conditionally needed, and as a required endpoint when using `-filter_complex` without a terminal filter.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "null" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Pass-through for testing pipeline overhead

Measure the encoding overhead of a filtergraph without any actual filtering.

```sh
ffmpeg -i input.mp4 -vf "null" output.mp4
```

### Use as a placeholder in a conditional pipeline

Insert `null` as a no-op stage while developing or debugging a filtergraph that will later use a real filter.

```sh
ffmpeg -i input.mp4 -vf "null,scale=1280:720" output.mp4
```

### Terminate a filter_complex branch

In a complex filtergraph, route an unused output to `nullsink` (the sink version) to avoid errors.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[main][discard]; [discard]nullsink" \
  -map "[main]" output.mp4
```

## Notes

- `null` has zero processing cost and is completely transparent to the frame pipeline.
- The audio equivalent is `anull`.
- When using `-filter_complex`, if a labeled output is not mapped to an output file, use `nullsink` (not `null`) to consume and discard the unused stream.
- The filter is also useful for benchmarking decoders: `ffmpeg -i input.mp4 -vf "null" -f null -` discards all output and measures decode throughput.
