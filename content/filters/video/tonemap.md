+++
title = "tonemap"
description = "Apply tone mapping to convert between different dynamic ranges, including HDR to SDR conversion."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["hdr", "tone-mapping", "color"]

[extra]
filter_type = "video"
since = ""
see_also = ["colorspace", "colormatrix"]
parameters = ["tonemap", "param", "desat", "peak"]
cohort = 2
+++

The `tonemap` filter applies a tone mapping operator to convert video between different dynamic ranges, most commonly from HDR (High Dynamic Range) to SDR (Standard Dynamic Range). It compresses the wide luminance range of HDR content into the narrower range displayable on standard monitors while preserving highlight detail and overall image appearance.

## Quick Start

```sh
# HDR to SDR with hable tone mapping
ffmpeg -i hdr.mp4 -vf "tonemap=hable" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tonemap | int | `none` | Tone mapping algorithm: `none`, `linear`, `gamma`, `reinhard`, `hable`, `mobius`. |
| param | double | `(varies)` | Algorithm-specific parameter (e.g. gamma exponent for `gamma`, knee for `mobius`). |
| desat | double | `2.0` | Desaturation strength for out-of-gamut colours. 0=no desaturation. Range: 0–10. |
| peak | double | `0.0` | Override for the signal peak (in nits). 0 = auto-detect from metadata. |

### Tone mapping algorithms

| Algorithm | Description |
|-----------|-------------|
| `none` | No tone mapping (passthrough). |
| `linear` | Linear scaling. `param` sets the scale factor. |
| `gamma` | Power-law gamma. `param` sets the exponent. |
| `reinhard` | Classic photographic Reinhard operator. |
| `hable` | Hable ("Uncharted 2") filmic tone mapper — popular, preserves highlights. |
| `mobius` | Smooth Möbius transform. `param` controls the knee transition (default 0.3). |

## Examples

### HDR to SDR with Hable operator

```sh
ffmpeg -i hdr_input.mp4 -vf "tonemap=hable" output_sdr.mp4
```

### Reinhard tone mapping with reduced desaturation

```sh
ffmpeg -i hdr.mp4 -vf "tonemap=reinhard:desat=1.0" output.mp4
```

### Full HDR pipeline with colorspace conversion

Convert from BT.2020 / SMPTE 2084 (PQ) to BT.709 before tone mapping.

```sh
ffmpeg -i hdr.mp4 \
  -vf "zscale=transfer=linear,tonemap=hable,zscale=transfer=bt709,format=yuv420p" \
  output_sdr.mp4
```

### Override peak luminance for HDR10

```sh
ffmpeg -i hdr10.mp4 -vf "tonemap=hable:peak=1000" output.mp4
```

## Notes

- `tonemap` alone converts luminance values; for a complete HDR-to-SDR pipeline you also need colorspace and transfer function conversion. Use `zscale` (from the `libzimg` library) for accurate colorimetry.
- `hable` is generally the best-looking default for cinematic content; `reinhard` is simpler but can look flat.
- `desat` controls how out-of-gamut colours (very saturated highlights) are desaturated. Values of 2–4 work well for most content.
- If the source has HDR10 metadata, `peak=0` (auto) reads the mastering display luminance; override with `peak=1000` for a 1000-nit display.
