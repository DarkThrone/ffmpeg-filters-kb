+++
title = "fieldorder"
description = "Convert interlaced video between top-field-first (TFF) and bottom-field-first (BFF) field order."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["interlace", "field-order", "conversion"]

[extra]
filter_type = "video"
since = ""
see_also = ["yadif", "bwdif", "idet"]
parameters = ["order"]
cohort = 2
source_file = "libavfilter/vf_fieldorder.c"
+++

The `fieldorder` filter changes the field dominance of interlaced video from top-field-first (TFF) to bottom-field-first (BFF) or vice versa. It shifts the picture content by one line and fills the gap with content from the adjacent field, consistent with broadcast field-order conversion. If the input is not interlaced, or is already in the requested field order, the filter passes the video through unchanged.

## Quick Start

```sh
# Convert to bottom-field-first (for DV output)
ffmpeg -i input.ts -vf "fieldorder=bff" output.dv
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| order | int | `tff` | Output field order: `tff` (top field first) or `bff` (bottom field first). |

## Examples

### Convert to bottom-field-first for DV

PAL DV requires bottom-field-first.

```sh
ffmpeg -i broadcast.ts -vf "fieldorder=bff" output.dv
```

### Convert to top-field-first for broadcast

```sh
ffmpeg -i dv_capture.dv -vf "fieldorder=tff" broadcast.ts
```

### Use in a deinterlace+re-interlace pipeline

```sh
ffmpeg -i input.ts -vf "yadif=1,fieldorder=tff" output.ts
```

## Notes

- `fieldorder` only affects interlaced content — progressive video is passed through without modification.
- The conversion works by shifting image content up or down by one line and filling the vacated line with neighboring field content.
- PAL DV format is bottom-field-first; most broadcast standards (DVB, ATSC) are top-field-first.
- Use `idet` to determine the existing field order before applying `fieldorder`.
- This filter sets the `tff` / `bff` flag in the output stream metadata in addition to physically rearranging the lines.
