+++
title = "thistogram"
description = "Render a temporal histogram of pixel value distribution over time as a scrolling video, showing how the luma or color histogram evolves frame by frame."
date = 2024-01-01

[taxonomies]
category = ["visualization"]
tags = ["visualization", "video", "histogram", "analysis"]

[extra]
filter_type = "visualization"
since = ""
see_also = ["histogram", "waveform", "vectorscope"]
parameters = ["display_mode", "levels_mode", "components", "level_height", "scale_height", "fgopacity", "bgopacity", "colors_mode", "width", "envelope", "slide"]
cohort = 3
+++

The `thistogram` filter produces a temporal histogram — each column represents the pixel-value histogram of one video frame, and new columns scroll in from the right as the video plays. This creates a time-vs-level display that shows how the exposure and color distribution change over time. It is useful for spotting flicker, brightness ramps, color shifts, or inconsistent grading across a timeline.

## Quick Start

```sh
ffplay -i input.mp4 -vf thistogram
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| display_mode / d | int | `stack` | Overlay mode: `overlay` (histogram over video) or `stack` (side by side) or `parade`. |
| levels_mode / m | int | `linear` | Scale mode: `linear` or `logarithmic`. |
| components / c | int | `7` | Which color components to display (bitmask: 1=Y/R, 2=Cb/G, 4=Cr/B, 8=A). |
| level_height | int | `200` | Height of the histogram area in pixels. |
| scale_height | int | `12` | Height of the scale markers. |
| fgopacity / f | float | `0.7` | Foreground opacity. |
| bgopacity / b | float | `0.5` | Background opacity. |
| colors_mode / l | int | `colorful` | Color mode: `gray`, `color`, `colorful`, `levels`, `mono`, `acolor`, `xray`. |
| width / w | int | `0` | Width of display (0 = auto). |
| envelope / e | bool | `0` | Draw envelope around histogram. |
| slide | int | `replace` | Scroll mode: `replace`, `scroll`, `rscroll`, `frame`. |

## Examples

### Basic temporal histogram

```sh
ffplay -i input.mp4 -vf thistogram
```

### Logarithmic scale to see shadows better

```sh
ffplay -i input.mp4 -vf "thistogram=levels_mode=logarithmic"
```

### Luma only (component Y)

```sh
ffplay -i input.mp4 -vf "thistogram=components=1"
```

### Save temporal histogram video

```sh
ffmpeg -i input.mp4 -vf "thistogram=display_mode=stack:level_height=300" hist.mp4
```

## Notes

- `display_mode=overlay` draws the histogram over the video itself; `stack` adds it below.
- `components` bitmask: `1`=Y/R, `2`=Cb/G, `4`=Cr/B — combine by adding (e.g., `7` = all RGB).
- `slide=scroll` creates a waterfall/spectrogram style display where time scrolls left.
- For a per-frame static histogram display, use the `histogram` filter instead.
