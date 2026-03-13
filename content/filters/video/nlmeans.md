+++
title = "nlmeans"
description = "Denoise video using the Non-Local Means algorithm for high-quality noise reduction."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["denoise", "noise-reduction"]

[extra]
filter_type = "video"
since = ""
see_also = ["hqdn3d", "atadenoise", "bm3d"]
parameters = ["s", "p", "pc", "r", "rc"]
cohort = 2
source_file = "libavfilter/vf_nlmeans.c"
+++

The `nlmeans` filter applies Non-Local Means denoising, a high-quality algorithm that compares small patches across the entire frame to identify similar regions and averages them to suppress noise. It produces excellent results, preserving fine detail and textures that simpler blur-based denoisers destroy. The trade-off is computational cost: it is significantly slower than `hqdn3d` or `atadenoise`.

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "nlmeans=s=4:p=7:r=15" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | double | `1.0` | Denoising strength. Higher = stronger denoising, less detail. Typical range: 1–10. |
| p | int | `7` | Patch size (side length in pixels). Must be odd. Range: 1–99. |
| pc | int | `0` | Patch size for chroma planes. 0 = use `p`. |
| r | int | `15` | Research window size (side length). Must be odd. Larger = better quality, much slower. |
| rc | int | `0` | Research window for chroma. 0 = use `r`. |

## Examples

### Moderate denoising

Good for slightly noisy footage — preserves detail while smoothing grain.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=3:p=7:r=15" output.mp4
```

### Aggressive denoising for very grainy footage

```sh
ffmpeg -i grainy.mp4 -vf "nlmeans=s=8:p=7:r=21" output.mp4
```

### Denoise luma more than chroma

Chroma noise is often less visible; using smaller patch/search for chroma is faster.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=4:p=7:r=15:pc=3:rc=9" output.mp4
```

### Fast preview mode (small search window)

Reduce `r` to speed up processing at the cost of quality.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=4:p=5:r=9" output.mp4
```

## Notes

- `s` is the primary quality knob: start at 3–4 for moderate noise and increase by 2 until noise is acceptable. Values above 8 tend to over-smooth fine textures.
- Computational cost scales with `r²`: doubling the research window quadruples processing time. The default `r=15` is a good balance.
- `nlmeans` is better than `hqdn3d` at preserving high-frequency texture and edges, making it preferred for film grain preservation vs. noise reduction.
- For GPU-accelerated denoising in production workflows, consider `bm3d` which has a two-pass mode for even higher quality.
