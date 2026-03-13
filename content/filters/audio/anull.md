+++
title = "anull"
description = "Pass audio through unchanged — a no-op filter useful for testing and filter graph construction."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["passthrough", "testing", "filter", "noop"]

[extra]
filter_type = "audio"
since = ""
see_also = ["asplit", "aformat", "atrim"]
parameters = []
cohort = 1
source_file = "libavfilter/af_anull.c"
+++

The `anull` filter passes every audio sample to its output without modification. It has no parameters and introduces no latency or processing overhead. Its primary uses are as a placeholder in filter graphs during development, as a no-op endpoint when a filter is syntactically required but no transformation is desired, and in testing pipelines to verify that audio passes through a graph correctly.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "anull" output.mp3
```

## Parameters

This filter has no parameters.

## Examples

### Verify that audio passes through a filter graph

```sh
ffmpeg -i input.mp3 -af "anull" -f null -
```

### Use as a placeholder while building a graph

Replace `anull` with the intended filter once it is determined:

```sh
ffmpeg -i input.mp3 -af "anull" output.mp3
```

### Combine with other filters in a complex graph

`anull` can serve as a labelled passthrough node in a `filter_complex` graph:

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]anull[out]" -map "[out]" output.mp3
```

## Notes

- `anull` is the audio equivalent of the `null` video filter.
- It incurs no measurable performance overhead — the filter framework may optimize it away entirely.
- Using `anull` in a production pipeline is harmless but unnecessary; it can be removed without any change to the output.
