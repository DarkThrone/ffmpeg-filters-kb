+++
title = "telecine"
description = "Apply telecine (3:2 pulldown) to progressive video, converting 24fps film content to 29.97fps interlaced video for NTSC broadcast."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "telecine", "broadcast", "ntsc"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["detelecine", "tinterlace", "fieldmatch"]
parameters = ["first_field", "pattern"]
cohort = 3
source_file = "libavfilter/vf_telecine.c"
+++

The `telecine` filter applies a pulldown pattern to progressive video, creating the 3:2 field sequence used when converting 24fps film to 29.97fps NTSC broadcast. Each progressive frame is repeated across fields according to the pattern: the classic `23` pattern repeats two frames as 2 fields and one as 3 fields. The filter can also apply non-standard pulldown patterns for other conversion ratios (25→30, 18→30, etc.).

## Quick Start

```sh
# Apply 3:2 pulldown: 24fps progressive → 29.97fps telecined
ffmpeg -i film_24fps.mp4 -vf telecine -r 30000/1001 ntsc_telecined.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| first_field | int | `top` | First output field: `top` (tff) or `bottom` (bff). |
| pattern | string | `23` | Pulldown pattern — string of digits indicating field repeat counts per frame. |

## Pulldown Patterns

| Pattern | Usage |
|---------|-------|
| `23` | 24fps → NTSC 30i (classic 3:2 pulldown) |
| `2332` | 24fps → NTSC 30i (preferred, smoother) |
| `33` | 20fps → NTSC 30i |
| `334` | 18fps → NTSC 30i |
| `222222222223` | 24fps → PAL 25i (Euro pulldown) |

## Examples

### Classic 3:2 pulldown (24fps to 29.97fps)

```sh
ffmpeg -i film.mp4 -vf telecine -r 30000/1001 ntsc.ts
```

### Preferred 2332 pattern for 24p

```sh
ffmpeg -i film.mp4 -vf "telecine=pattern=2332" -r 30000/1001 ntsc.ts
```

### PAL Euro pulldown (24fps to 25fps interlaced)

```sh
ffmpeg -i film.mp4 -vf "telecine=pattern=222222222223" -r 25 pal.ts
```

### Bottom field first (for certain tape formats)

```sh
ffmpeg -i film.mp4 -vf "telecine=first_field=bottom" -r 30000/1001 ntsc_bff.ts
```

## Notes

- The pattern digits indicate how many fields each input frame contributes; total divided by 2 gives output frames per input frame.
- The `23` pattern produces judder on 24fps content when displayed on 60Hz displays — `2332` distributes the cadence more evenly.
- To reverse telecine on the output later, use `detelecine` with the same pattern.
