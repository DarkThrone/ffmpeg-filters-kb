+++
title = "cropdetect"
description = "Auto-detect the optimal crop parameters to remove black borders from video."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["detection", "crop", "analysis"]

[extra]
filter_type = "video"
since = ""
see_also = ["crop"]
parameters = ["limit", "round", "reset", "skip", "mode"]
cohort = 2
source_file = "libavfilter/vf_cropdetect.c"
+++

The `cropdetect` filter analyzes video frames to find the borders of non-black (or non-static) content and outputs the corresponding `crop` filter parameters as frame metadata. It does **not** crop the video itself — it detects what the crop values should be. The detected values are printed to the log; you then run a second pass using `crop` with those values.

## Quick Start

```sh
# Step 1: Detect crop values
ffmpeg -i input.mp4 -vf "cropdetect" -f null -

# Step 2: Apply detected crop (e.g. if output showed crop=1920:800:0:140)
ffmpeg -i input.mp4 -vf "crop=1920:800:0:140" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| limit | float | `24.0` | Threshold below which a pixel is considered black. Range: 0–255. |
| round | int | `16` | Round detected dimensions to multiples of this value. 16 works well for H.264. |
| reset | int | `0` | Reset crop detection every N frames (0 = never reset). |
| skip | int | `2` | Number of initial frames to skip (often have logos or fade-ins). |
| reset_count | int | — | Alias for `reset`. |
| mode | int | `black` | Detection mode: `black` (detect black borders) or `mvedges` (detect static borders via motion vectors). |

## Examples

### Detect black borders in a letterboxed film

```sh
ffmpeg -i movie.mkv -vf "cropdetect=limit=24:round=2" -f null - 2>&1 | grep cropdetect
```

### Skip the first 60 frames (opening credits)

```sh
ffmpeg -i input.mp4 -vf "cropdetect=skip=60" -f null -
```

### Detect and apply crop in one command (using shell variable)

```sh
CROP=$(ffmpeg -i input.mp4 -vf "cropdetect" -f null - 2>&1 | awk '/crop=/{print $NF}' | tail -1)
ffmpeg -i input.mp4 -vf "$CROP" output.mp4
```

### Use mvedges mode for content with non-black borders

```sh
ffmpeg -i input.mp4 -vf "cropdetect=mode=mvedges" -f null -
```

## Notes

- `cropdetect` outputs lines like `[Parsed_cropdetect] t:3.003 crop=1920:800:0:140` to stderr. The crop values stabilize after a few frames once a consistent border is found.
- `limit=24` works well for 8-bit video; for 10-bit sources, you may need `limit=96` (values scale with bit depth).
- `round=16` ensures the crop dimensions are multiples of 16, which is required for most H.264 encoders (macroblock alignment).
- After detection, pass the `crop=W:H:X:Y` string directly to a second `ffmpeg` invocation with `-vf "crop=W:H:X:Y"`.
