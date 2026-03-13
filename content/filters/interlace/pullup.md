+++
title = "pullup"
description = "Reverse 3:2 pulldown (inverse telecine) to reconstruct progressive frames from NTSC-telecined video using look-ahead field matching."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "telecine", "deinterlace", "ivtc"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["fieldmatch", "decimate", "dejudder"]
parameters = ["jl", "jr", "jt", "jb", "sb", "mp"]
cohort = 3
+++

The `pullup` filter performs inverse telecine (IVTC) — it reconstructs the original 24fps or 25fps progressive frames from 29.97fps 3:2 pulldown telecined video. Unlike pattern-based approaches, `pullup` uses look-ahead field matching, making it robust to mixed content (24p telecined + 30i interlaced). The output has variable framerate; use `fps=24000/1001` after `pullup` for NTSC, or `fps=25` for PAL.

## Quick Start

```sh
# Inverse telecine NTSC (29.97i → 23.976p)
ffmpeg -i telecined.ts -vf "pullup,fps=24000/1001" progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| jl | int | `8` | Junk pixels to ignore on the left (units: 8 pixels). |
| jr | int | `8` | Junk pixels to ignore on the right (units: 8 pixels). |
| jt | int | `4` | Junk lines to ignore at top (units: 2 lines). |
| jb | int | `4` | Junk lines to ignore at bottom (units: 2 lines). |
| sb | int | `0` | Strict breaks: `1` = fewer false matches but may drop frames; `-1` = more permissive. |
| mp | int | `l` | Metric plane: `l` (luma), `u` (Cb), `v` (Cr). |

## Examples

### Inverse telecine NTSC film

```sh
ffmpeg -i film_telecined.ts -vf "pullup,fps=24000/1001" -c:v libx264 film.mp4
```

### Inverse telecine PAL

```sh
ffmpeg -i pal_pulldown.mxf -vf "pullup,fps=25" progressive.mp4
```

### With strict breaks for cleaner output

```sh
ffmpeg -i input.ts -vf "pullup=sb=1,fps=24000/1001" clean.mp4
```

## Notes

- `pullup` produces variable-framerate output — always follow with `fps` to regularize the frame rate.
- For content that is a mix of telecined and interlaced video, `fieldmatch` + `yadif` + `decimate` is a more flexible alternative.
- The "junk" parameters (`jl`, `jr`, `jt`, `jb`) help ignore logo bugs or letterbox areas that might confuse field matching.
- `mp=l` (luma, the default) is best for most content; use chroma plane only to save CPU on clean sources.
