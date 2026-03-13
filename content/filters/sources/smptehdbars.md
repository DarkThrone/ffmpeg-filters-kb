+++
title = "smptehdbars"
description = "Generate SMPTE RP 219-2002 high-definition color bars for HD broadcast calibration and signal testing."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["test", "broadcast", "color-bars", "source", "hd"]

[extra]
filter_type = "source"
since = ""
see_also = ["smptebars", "pal100bars"]
parameters = ["size", "rate", "duration"]
cohort = 3
+++

The `smptehdbars` source generates SMPTE RP 219-2002 high-definition color bars — the HD standard for broadcast monitor calibration and signal testing. It differs from SD `smptebars` in structure: it includes 75% color bars in the upper section, a three-level ramp in the lower left, and a cyan/grey/yellow segment for white balance and gamut testing.

## Quick Start

```sh
ffplay -f lavfi "smptehdbars=size=1920x1080:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### 1080i25 HD color bars

```sh
ffplay -f lavfi "smptehdbars=size=1920x1080:rate=25"
```

### 1080p29.97 HD color bars

```sh
ffplay -f lavfi "smptehdbars=size=1920x1080:rate=30000/1001"
```

### Generate HD bars with 1 kHz tone for broadcast leader

```sh
ffmpeg -f lavfi -i "smptehdbars=size=1920x1080:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 60 hd_leader.mxf
```

## Notes

- Based on SMPTE RP 219-2002 (HD) — use `smptebars` for SD (SMPTE EG 1-1990).
- The HD pattern layout differs from SD: upper 75% color bars, lower-left ramp (sub-black to white), lower-center blue-only bars, lower-right signal qualifier.
- Pair with `vectorscope` to verify that the color bars hit their target positions on the scope.
