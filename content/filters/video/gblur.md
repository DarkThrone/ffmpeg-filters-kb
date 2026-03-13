+++
title = "gblur"
description = "Apply a Gaussian blur to video with configurable sigma and plane selection."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["blur", "gaussian"]

[extra]
filter_type = "video"
since = ""
see_also = ["boxblur", "smartblur", "nlmeans"]
parameters = ["sigma", "steps", "planes", "sigmaV"]
cohort = 2
+++

The `gblur` filter applies a Gaussian blur to video frames. Unlike `boxblur`, it uses a proper Gaussian kernel (approximated with iterative box passes), which produces a smoother, more natural-looking blur. It supports independent horizontal and vertical sigma values and can target specific planes.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "gblur=sigma=2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sigma | float | `0.5` | Gaussian sigma (blur radius). Higher values = more blur. |
| steps | int | `1` | Number of box blur passes used to approximate the Gaussian. More steps = more accurate, more CPU. |
| planes | int | `0xf` | Bitmask of planes to filter: 1=Y/R, 2=Cb/G, 4=Cr/B, 8=A. Default `0xf` blurs all planes. |
| sigmaV | float | `0` | Vertical sigma. If 0 (default), uses the same value as `sigma` (symmetric blur). |

## Examples

### Subtle background softening

```sh
ffmpeg -i input.mp4 -vf "gblur=sigma=1" output.mp4
```

### Strong blur for mosaic or privacy effect

```sh
ffmpeg -i input.mp4 -vf "gblur=sigma=8" output.mp4
```

### Blur luma only, preserve chroma

```sh
ffmpeg -i input.mp4 -vf "gblur=sigma=2:planes=1" output.mp4
```

### Asymmetric horizontal/vertical blur

Blur more in the horizontal direction than vertical.

```sh
ffmpeg -i input.mp4 -vf "gblur=sigma=4:sigmaV=1" output.mp4
```

## Notes

- Sigma roughly corresponds to blur radius in pixels; `sigma=1` is subtle, `sigma=5` is heavy, `sigma=10+` is extreme.
- Increasing `steps` improves quality but is rarely necessary for `sigma < 5`; default steps=1 is fine for most uses.
- For a simple rectangular blur, `boxblur` is faster. For edge-preserving blur, use `smartblur` or `nlmeans`.
- `gblur` can be used before encoding to reduce high-frequency noise and improve compression efficiency.
