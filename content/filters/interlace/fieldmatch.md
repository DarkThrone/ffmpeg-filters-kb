+++
title = "fieldmatch"
description = "Match fields for inverse telecine, reconstructing progressive frames from telecined video while leaving genuinely interlaced frames flagged for downstream deinterlacing."
date = 2024-01-01

[taxonomies]
category = ["interlace"]
tags = ["interlace", "video", "telecine", "ivtc", "deinterlace"]

[extra]
filter_type = "interlace"
since = ""
see_also = ["decimate", "pullup", "yadif"]
parameters = ["order", "mode", "ppsrc", "field", "mchroma", "y0", "y1", "scthresh", "combmatch", "cthresh", "blockx", "blocky", "combpel"]
cohort = 3
+++

The `fieldmatch` filter performs field matching for inverse telecine — it identifies which fields from consecutive frames belong together to reconstruct the original progressive frames, based on algorithms from the AviSynth TFM/TIVTC project. Unlike `pullup`, `fieldmatch` separates matching from frame dropping, so a decimation filter (`decimate`) must follow to remove the duplicate frames. This separation allows inserting a deinterlacer (like `yadif`) between them to handle mixed content.

## Quick Start

```sh
# Complete IVTC pipeline: match + decimate
ffmpeg -i telecined.ts -vf "fieldmatch,decimate" progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| order | int | `auto` | Field order: `auto`, `bff`, `tff`. |
| mode | int | `pc_n` | Matching strategy: `pc`, `pc_n`, `pc_u`, `pc_n_ub`, `pcn`, `pcn_ub`. |
| ppsrc | bool | `0` | Use second stream as pre-processed reference for better matching. |
| field | int | `auto` | Which field to match from: `auto`, `bottom`, `top`. |
| mchroma | bool | `1` | Include chroma in match comparisons. |
| y0 | int | `0` | Top line of exclusion band (e.g., to ignore logo area). |
| y1 | int | `0` | Bottom line of exclusion band. |
| scthresh | double | `12.0` | Scene change threshold. |
| combmatch | int | `sc` | Comb matching: `none`, `sc`, `full`. |
| cthresh | int | `9` | Combing detection threshold. |
| blockx | int | `16` | Block width for combing detection. |
| blocky | int | `16` | Block height for combing detection. |
| combpel | int | `80` | Number of combed pixels to flag a frame as combed. |

## Examples

### Basic IVTC: fieldmatch + decimate

```sh
ffmpeg -i input.ts -vf "fieldmatch,decimate" output.mp4
```

### With deinterlacer fallback for mixed content

```sh
ffmpeg -i input.ts -vf "fieldmatch,yadif=deint=interlaced,decimate" output.mp4
```

### Using a pre-processed stream for better matching

```sh
ffmpeg -i input.ts \
  -filter_complex "[0:v]yadif=mode=1[pp];[0:v][pp]fieldmatch=ppsrc=1,decimate[out]" \
  -map "[out]" output.mp4
```

## Notes

- `fieldmatch` does NOT drop duplicate frames — always follow with `decimate` to get constant 24fps output.
- Insert `yadif=deint=interlaced` between `fieldmatch` and `decimate` to deinterlace the combed frames `fieldmatch` couldn't reconstruct.
- `mode=pc_n` is the default and balances jerkiness risk vs. quality; `pcn_ub` is most aggressive.
- For variable framerate input (mixed 24p/30i), prepend `dejudder,fps=30000/1001` before `fieldmatch`.
