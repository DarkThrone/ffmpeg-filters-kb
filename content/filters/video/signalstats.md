+++
title = "signalstats"
description = "Compute broadcast-standard signal quality metrics (Y/U/V min/max/avg, saturation, hue) for each frame and output them as metadata."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["analysis", "broadcast", "statistics", "QC"]

[extra]
filter_type = "video"
since = ""
see_also = ["waveform", "vectorscope", "histogram"]
parameters = ["stat", "out", "color"]
cohort = 2
source_file = "libavfilter/vf_signalstats.c"
+++

The `signalstats` filter computes per-frame statistics about the video signal — luma (Y), chroma (U/V), saturation, and hue levels — and attaches them as `lavfi.signalstats.*` frame metadata. It is designed for digitization QC of analog video and can also visually highlight out-of-range pixels. The statistics are output to the FFmpeg log and can be captured with tools like `ffprobe`.

## Quick Start

```sh
# Print signal stats for every frame
ffmpeg -i input.mp4 -vf "signalstats" -f null - 2>&1 | grep signalstats
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stat | flags | (none) | Additional statistics to compute: `tout` (temporal outliers), `vrep` (vertical line repetition), `brng` (out-of-range values). |
| out | int | (none) | Highlight filter: `tout`, `vrep`, or `brng`. Marks detected pixels in the output frame. |
| color / c | color | `yellow` | Color used to highlight detected pixels when `out` is set. |

## Metadata Fields

| Field | Range | Description |
|-------|-------|-------------|
| YMIN, YMAX | 0–255 | Min/max luma value |
| YLOW, YHIGH | 0–255 | Luma at 10th/90th percentile |
| YAVG | 0–255 | Average luma |
| UMIN–UMAX, VMIN–VMAX | 0–255 | Min/max chroma |
| SATMIN–SATMAX | 0–181 | Min/max saturation |
| HUEMED, HUEAVG | 0–360 | Median/average hue |
| YDIF, UDIF, VDIF | 0–255 | Frame-to-frame difference per plane |

## Examples

### Dump all frame stats to CSV

```sh
ffprobe -f lavfi -i "movie=input.mp4,signalstats" \
  -show_frames -select_streams v \
  -print_format csv -show_entries frame_tags=lavfi.signalstats.YAVG \
  > luma_avg.csv
```

### Highlight out-of-range pixels visually

```sh
ffmpeg -i input.mp4 -vf "signalstats=out=brng:color=red" output.mp4
```

### Check temporal outliers (noise spikes)

```sh
ffmpeg -i input.mp4 -vf "signalstats=stat=tout:out=tout" output.mp4
```

### QC check: find frames with illegal luma levels

```sh
ffprobe -f lavfi -i "movie=input.mp4,signalstats" \
  -show_frames -select_streams v \
  -show_entries frame_tags=lavfi.signalstats.YMIN,lavfi.signalstats.YMAX 2>/dev/null
```

## Notes

- Legal broadcast luma range is 16–235 (8-bit); `brng` detects pixels outside the 0–255 nominal range (i.e. super-black or super-white).
- `vrep` (vertical line repetition) detects tape dropout artifacts common in VHS/Betamax digitization.
- `tout` (temporal outliers) detects pixels that differ dramatically from the previous frame — a sign of noise or tape damage.
- All statistics are attached to frames as `lavfi.signalstats.*` metadata; use `ffprobe -show_frames` to extract them to CSV or JSON.
