+++
title = "lenscorrection"
description = "Correct barrel or pincushion lens distortion using radial correction coefficients."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["lens", "correction", "distortion"]

[extra]
filter_type = "video"
since = ""
see_also = ["perspective"]
parameters = ["cx", "cy", "k1", "k2", "i", "fc"]
cohort = 2
+++

The `lenscorrection` filter corrects radial lens distortion — barrel distortion (convex, fisheye-like) or pincushion distortion (concave, telephoto-like) — using quadratic and quartic correction coefficients. The correction is applied around a configurable optical center. This is useful for correcting wide-angle or action camera footage shot with a fisheye lens.

## Quick Start

```sh
# Fix barrel distortion (GoPro/wide-angle)
ffmpeg -i fisheye.mp4 -vf "lenscorrection=k1=-0.227:k2=-0.022" corrected.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cx | double | `0.5` | X-coordinate of the optical center (0–1 relative to width). 0.5 = center. |
| cy | double | `0.5` | Y-coordinate of the optical center (0–1 relative to height). |
| k1 | double | `0.0` | Quadratic radial distortion coefficient. Negative = fix barrel, positive = fix pincushion. |
| k2 | double | `0.0` | Quartic radial distortion coefficient. Fine-tuning for higher-order distortion. |
| i | int | `nearest` | Interpolation method: `nearest`, `bilinear`, or `lanczos`. |
| fc | color | `black@0` | Fill color for border areas created by correction. |

## Examples

### Fix GoPro/wide-angle barrel distortion

Typical GoPro correction values (adjust for your lens).

```sh
ffmpeg -i gopro.mp4 -vf "lenscorrection=k1=-0.227:k2=-0.022" output.mp4
```

### Fix pincushion distortion (telephoto lens)

```sh
ffmpeg -i telephoto.mp4 -vf "lenscorrection=k1=0.1:k2=0.02" output.mp4
```

### Correct with bilinear interpolation

```sh
ffmpeg -i input.mp4 -vf "lenscorrection=k1=-0.15:k2=-0.01:i=bilinear" output.mp4
```

### Shift optical center for off-center lens

```sh
ffmpeg -i input.mp4 -vf "lenscorrection=cx=0.52:cy=0.49:k1=-0.2" output.mp4
```

## Notes

- Negative `k1` corrects barrel distortion (the most common case for wide-angle lenses). Positive `k1` corrects pincushion.
- `k2` is a higher-order term that helps with lenses that have complex distortion profiles. Start with `k1` alone and add `k2` only if the correction is uneven near the edges.
- Calibration values for specific cameras/lenses can be found in databases like the lensfun library or by using calibration tools like OpenCV.
- Correction will produce black borders at the edges; use `crop` afterward to remove them, or `scale` to fill the frame.
