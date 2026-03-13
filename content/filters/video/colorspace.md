+++
title = "colorspace"
description = "Convert between color spaces including primaries, transfer functions, and matrix coefficients."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["color", "color-space", "hdr"]

[extra]
filter_type = "video"
since = ""
see_also = ["colormatrix", "tonemap"]
parameters = ["all", "space", "range", "primaries", "trc", "format"]
cohort = 2
+++

The `colorspace` filter performs comprehensive colorspace conversions, handling the matrix coefficients, color primaries, transfer function (gamma/PQ/HLG), and output pixel format together. It is more complete than `colormatrix` (which only handles the YCbCr matrix) and is suited for accurate conversions between SD, HD, and HDR standards.

## Quick Start

```sh
# Convert from BT.601 (SD) to BT.709 (HD)
ffmpeg -i sd.mp4 -vf "colorspace=all=bt709" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| all | int | Shortcut to set all properties simultaneously. Values: `bt601`, `bt709`, `bt2020-10`, `bt2020-12`, `bt2020-cl`, `smpte-170m`, `smpte-240m`, `bt470m`, `bt470bg`. |
| space | int | Output color matrix (YCbCr coefficients). Same values as `all`. |
| range | int | Output color range: `tv` (limited, 16–235 for 8-bit), `pc` (full, 0–255). |
| primaries | int | Output color primaries. Values: `bt470m`, `bt470bg`, `bt709`, `bt2020`. |
| trc | int | Output transfer characteristics (gamma). Values: `bt709`, `bt601`, `smpte240m`, `bt2020-10`, `bt2020-12`, `smpte2084`, `iec61966-2-1` (sRGB), `arib-std-b67` (HLG). |
| format | pixel_fmt | Output pixel format (e.g. `yuv420p`, `yuv420p10le`). |
| fast | bool | Use fast conversion (less accurate). |
| dither | int | Dithering method: `none`, `fsb` (Floyd-Steinberg). |

## Examples

### SD to HD color matrix conversion

```sh
ffmpeg -i sd.mp4 -vf "colorspace=all=bt709" hd.mp4
```

### Convert from SDR BT.709 to HLG (HDR)

```sh
ffmpeg -i sdr.mp4 -vf "colorspace=trc=arib-std-b67:primaries=bt2020:space=bt2020" hlg.mp4
```

### Full range to limited range

```sh
ffmpeg -i full_range.mp4 -vf "colorspace=range=tv" limited.mp4
```

### BT.2020 10-bit for HDR delivery

```sh
ffmpeg -i input.mp4 -vf "colorspace=all=bt2020-10:format=yuv420p10le" output_hdr.mp4
```

## Notes

- `all=bt709` is a convenient shortcut that sets space, primaries, and trc together to BT.709 standards — appropriate for most HD delivery.
- For HDR workflows, the transfer characteristic (`trc`) is critical: `smpte2084` is PQ (HDR10), `arib-std-b67` is HLG.
- `colorspace` converts between standards; it does not perform tone mapping. For HDR-to-SDR, chain with `tonemap`.
- Always set the output pixel format explicitly with `format=` when the downstream encoder requires a specific format (e.g. `yuv420p` for H.264).
