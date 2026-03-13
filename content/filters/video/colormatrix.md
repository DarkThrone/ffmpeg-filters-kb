+++
title = "colormatrix"
description = "Convert between different color matrix standards such as BT.601, BT.709, and BT.2020."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "color-space"]

[extra]
filter_type = "video"
since = ""
see_also = ["colorspace"]
parameters = ["src", "dst"]
cohort = 2
+++

The `colormatrix` filter converts video between YCbCr color matrix standards. It is used to correct footage tagged with the wrong matrix or to prepare video for a specific delivery standard. Common uses include converting SD footage from BT.601 to BT.709 for HD deliverables, or handling legacy SMPTE 240M material.

## Quick Start

```sh
# Convert from SD (BT.601) to HD (BT.709)
ffmpeg -i sd_footage.mp4 -vf "colormatrix=bt601:bt709" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| src | int | Source color matrix. Options: `bt601`, `bt709`, `smpte240m`, `fcc`, `bt2020`. |
| dst | int | Destination color matrix. Same options as `src`. |

## Examples

### Convert SD to HD color matrix

```sh
ffmpeg -i sd.mp4 -vf "colormatrix=bt601:bt709" hd.mp4
```

### Convert to BT.2020 for HDR workflow

```sh
ffmpeg -i hd.mp4 -vf "colormatrix=bt709:bt2020" hdr_prep.mp4
```

### Fix incorrectly tagged footage

Footage recorded in SD but tagged as BT.709 — correct by applying BT.709→BT.601.

```sh
ffmpeg -i wrongly_tagged.mp4 -vf "colormatrix=bt709:bt601" corrected.mp4
```

## Notes

- `colormatrix` only changes the YCbCr matrix coefficients; it does not change the transfer function (gamma) or primary chromaticities. For a complete colorspace conversion, use `colorspace`.
- BT.601 is standard for SD (480i/576i); BT.709 is standard for HD (720p/1080p); BT.2020 is for UHD/HDR.
- After applying `colormatrix`, update the stream metadata with `-colorspace` and `-color_primaries` flags so players render correctly.
- Visually, the difference between BT.601 and BT.709 appears mostly in skin tones and reds — one will look slightly more saturated than the other.
