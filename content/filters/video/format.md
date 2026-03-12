+++
title = "format"
description = "Convert the input video to one of the specified pixel formats, letting libavfilter select the best match for the downstream filter."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["format", "pixel-format", "color"]

[extra]
filter_type = "video"
since = ""
see_also = ["scale", "setsar", "paletteuse"]
parameters = ["pix_fmts", "color_spaces", "color_ranges", "alpha_modes"]
cohort = 1
+++

The `format` filter requests that libavfilter convert the input video to one of the listed pixel formats. If the input is already in one of the specified formats, it passes through unchanged. When multiple formats are listed (pipe-separated), libavfilter chooses the best match for the next filter in the chain. This is useful for ensuring an encoder or filter receives a format it supports, or for explicitly controlling color space and range metadata.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "format=pix_fmts=yuv420p" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pix_fmts | string | — | Pipe-separated list of pixel format names (e.g., `yuv420p\|nv12\|rgb24`). |
| color_spaces | string | — | Pipe-separated list of color space names (e.g., `bt709\|bt470bg`). |
| color_ranges | string | — | Pipe-separated list of color range names: `tv` (limited) or `pc` (full). |
| alpha_modes | string | — | Pipe-separated list of alpha modes: `straight` or `premultiplied`. |

## Examples

### Force yuv420p for H.264 encoding

Most H.264 encoders require `yuv420p`. Inserting `format` before the encoder ensures compatibility.

```sh
ffmpeg -i input.png -vf "format=pix_fmts=yuv420p" -c:v libx264 output.mp4
```

### Allow the filter to choose among several formats

Provide a preference list so libavfilter picks the best match for the next stage without a hard requirement.

```sh
ffmpeg -i input.mp4 -vf "format=pix_fmts=yuv420p|yuv444p|nv12" output.mp4
```

### Convert to full-range (PC) color

Override the color range metadata to signal full-range (0-255) levels.

```sh
ffmpeg -i input.mp4 -vf "format=color_ranges=pc" output.mp4
```

### Ensure straight (un-premultiplied) alpha

Normalize alpha mode for compositing filters that require straight alpha.

```sh
ffmpeg -i input.mov -vf "format=alpha_modes=straight" output.mov
```

## Notes

- The `format` filter only converts between pixel formats that libswscale supports. Conversions between very different color spaces may introduce visible quality loss.
- Specifying multiple formats in `pix_fmts` lets FFmpeg choose the most efficient conversion path; a single format forces an exact conversion.
- To explicitly tag color space/range metadata without pixel conversion, use `setparams` or encoder options instead.
- For removing an alpha channel, convert to a format without alpha (e.g., `yuv420p`) — the alpha data is discarded.
