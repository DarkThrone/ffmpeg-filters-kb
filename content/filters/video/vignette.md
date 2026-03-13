+++
title = "vignette"
description = "Apply a natural lens vignette effect, darkening the corners and edges of the frame, or reverse an existing vignette."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["vignette", "effect", "color-grading"]

[extra]
filter_type = "video"
since = ""
see_also = ["exposure", "colorlevels"]
parameters = ["angle", "x0", "y0", "mode", "eval", "dither", "aspect"]
cohort = 2
+++

The `vignette` filter creates a natural-looking lens vignette by darkening pixels as they get farther from a configurable center point. The angle controls how pronounced the effect is, and a `backward` mode can reverse an existing vignette. The center position and angle support dynamic FFmpeg expressions evaluated per frame.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "vignette=PI/4" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| angle / a | string | `PI/5` | Lens angle expression in radians. Range: [0, PI/2]. Larger = stronger vignette. |
| x0 | string | `w/2` | X-coordinate of center (expression). Default = horizontal center. |
| y0 | string | `h/2` | Y-coordinate of center (expression). Default = vertical center. |
| mode | int | `forward` | `forward` (darken edges) or `backward` (brighten edges / reverse vignette). |
| eval | int | `init` | When to evaluate expressions: `init` (once) or `frame` (per frame). |
| dither | bool | `1` | Enable dithering to reduce banding. |
| aspect | rational | `1/1` | Vignette aspect ratio. Set to SAR of input for rectangular vignette. |

## Expression Variables

Available in `angle`, `x0`, `y0` expressions:

| Variable | Description |
|----------|-------------|
| `w`, `h` | Input width and height |
| `n` | Frame number (starts at 0) |
| `pts` | Presentation timestamp in timebase units |
| `t` | Presentation timestamp in seconds |
| `r` | Input frame rate |
| `tb` | Timebase |

## Examples

### Standard vignette (PI/4 angle)

```sh
ffmpeg -i input.mp4 -vf "vignette=PI/4" output.mp4
```

### Subtle vignette

```sh
ffmpeg -i input.mp4 -vf "vignette=PI/6" output.mp4
```

### Off-center vignette

```sh
ffmpeg -i input.mp4 -vf "vignette=angle=PI/4:x0=w*0.4:y0=h*0.4" output.mp4
```

### Reverse vignette (brightens edges)

```sh
ffmpeg -i input.mp4 -vf "vignette=mode=backward:angle=PI/4" output.mp4
```

### Animated flickering vignette

```sh
ffmpeg -i input.mp4 -vf "vignette='PI/4+random(1)*PI/50':eval=frame" output.mp4
```

## Notes

- `angle=PI/5` (default) is a subtle vignette; `PI/4` is moderate; `PI/3` is strong.
- `backward` mode reverses vignette — useful for correcting footage shot with a naturally-vignetted lens.
- Use `eval=frame` with dynamic expressions for animated vignettes; it is slower because all scalers must be recomputed per frame.
- `aspect` controls the shape: `1/1` gives a circular vignette; setting it to the input's SAR gives an elliptical (rectangular-following) vignette.
