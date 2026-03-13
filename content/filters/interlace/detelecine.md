+++
title = "detelecine"
description = "Apply inverse telecine using a known pulldown pattern to reconstruct the original progressive frames from telecined video."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "telecine", "ivtc", "deinterlace"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["telecine", "fieldmatch", "pullup"]
parameters = ["first_field", "pattern", "start_frame"]
cohort = 3
source_file = "libavfilter/vf_detelecine.c"
+++

The `detelecine` filter performs pattern-based inverse telecine — the exact reverse of the `telecine` filter. It requires knowing the pulldown pattern and phase (start frame) of the telecined stream. When the pattern is known (e.g., content was encoded by the same FFmpeg pipeline using `telecine`), `detelecine` provides a perfect lossless inversion. For content of unknown pattern, use `fieldmatch` + `decimate` instead.

## Quick Start

```sh
# Reverse 3:2 pulldown with known pattern
ffmpeg -i ntsc_telecined.ts -vf "detelecine" -r 24000/1001 progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| first_field | int | `top` | First field: `top` or `bottom`. Must match the `telecine` setting. |
| pattern | string | `23` | Pulldown pattern. Must exactly match the pattern used during `telecine`. |
| start_frame | int | `0` | Position of the first frame relative to the pattern, if the stream is cut. |

## Examples

### Reverse classic 3:2 pulldown

```sh
ffmpeg -i ntsc.ts -vf detelecine -r 24000/1001 film.mp4
```

### Reverse PAL Euro pulldown

```sh
ffmpeg -i pal.ts -vf "detelecine=pattern=222222222223" -r 24 film.mp4
```

### Handle cut stream with known phase offset

```sh
# If the clip was cut 3 frames into the pattern cycle:
ffmpeg -i cut_clip.ts -vf "detelecine=start_frame=3" -r 24000/1001 film.mp4
```

## Notes

- `detelecine` only works reliably when the pattern and phase are known; for broadcast captures of unknown origin, use `fieldmatch` + `decimate` or `pullup` instead.
- The `start_frame` parameter is essential when processing a mid-stream cut — incorrect values produce combed output.
- The output framerate will be variable unless you specify `-r` explicitly; set it to match the original pre-telecine rate.
