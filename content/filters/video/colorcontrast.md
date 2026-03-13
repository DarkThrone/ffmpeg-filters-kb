+++
title = "colorcontrast"
description = "Adjust contrast between opposing color pairs (red-cyan, green-magenta, blue-yellow) in video."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "contrast", "grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["eq", "colorbalance"]
parameters = ["rc", "gm", "by", "rcw", "gmw", "byw", "pl"]
cohort = 2
source_file = "libavfilter/vf_colorcontrast.c"
+++

The `colorcontrast` filter adjusts the contrast between complementary color pairs: red vs. cyan, green vs. magenta, and blue vs. yellow. Positive values push colors toward the primary and away from its complement; negative values do the opposite. Each pair also has a weight parameter (`rcw`, `gmw`, `byw`) to control influence on the final result.

## Quick Start

```sh
# Boost red-cyan contrast slightly
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rc | float | `0.0` | Red-cyan contrast. Positive=more red/less cyan; negative=more cyan/less red. Range: -1–1. |
| gm | float | `0.0` | Green-magenta contrast. Positive=more green; negative=more magenta. |
| by | float | `0.0` | Blue-yellow contrast. Positive=more blue; negative=more yellow. |
| rcw | float | `0.0` | Weight of red-cyan contrast in the final result. Range: 0–1. |
| gmw | float | `0.0` | Weight of green-magenta contrast in the final result. |
| byw | float | `0.0` | Weight of blue-yellow contrast in the final result. |
| pl | float | `0.0` | Amount of preserved luminance. Range: 0–1. |

## Examples

### Cool teal-and-orange look

Boost red-cyan contrast (push reds warmer) and add blue-yellow contrast.

```sh
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.3:by=-0.2:rcw=0.3:byw=0.2" output.mp4
```

### Increase green-magenta separation

```sh
ffmpeg -i nature.mp4 -vf "colorcontrast=gm=0.2:gmw=0.4" output.mp4
```

### Full complementary contrast enhancement

```sh
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.15:gm=0.1:by=0.1:rcw=0.3:gmw=0.3:byw=0.3" output.mp4
```

## Notes

- `rcw`, `gmw`, `byw` act as blend weights between the adjusted and original; setting them to 0 means no effect even if the adjustment values are non-zero.
- `pl` (preserve luminance) prevents color contrast adjustments from shifting the overall brightness of the image.
- This filter is particularly useful for subtle creative grading rather than technical correction; for technical color fixes, `colorbalance` or `colorlevels` are more precise.
- The range [-1, 1] for each contrast parameter; extreme values will significantly distort hues.
