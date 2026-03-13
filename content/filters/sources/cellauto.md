+++
title = "cellauto"
description = "Generate video from an elementary cellular automaton (Wolfram rules), producing evolving 1D patterns scrolled into a 2D video."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "generative", "cellular-automaton", "art"]

[extra]
filter_type = "source"
since = ""
see_also = ["life", "mandelbrot"]
parameters = ["rule", "size", "rate", "pattern", "random_fill_ratio", "scroll", "stitch"]
cohort = 3
+++

The `cellauto` source generates video from a 1D elementary cellular automaton using Wolfram's rule numbering (0–255). Each frame row is computed from the previous one using the selected rule, then scrolled upward to fill the frame. The initial state can be a specific pattern string/file or a random seed. Wolfram's Rule 110 (the default) is particularly famous for producing complex, aperiodic patterns.

## Quick Start

```sh
ffplay -f lavfi "cellauto=size=800x400:rule=110"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rule | int | `110` | Wolfram rule number (0–255). |
| size / s | image_size | `320x518` | Output frame size. Width should match the pattern width. |
| rate / r | video_rate | `25` | Frames per second. |
| pattern / p | string | — | Initial row as a string (non-whitespace = alive cell). |
| filename / f | string | — | Read initial row from a file. |
| random_fill_ratio / ratio | double | `1/φ ≈ 0.618` | Fill ratio for random initial state. |
| random_seed / seed | int64 | random | Seed for random initial state. |
| scroll | bool | `1` | Scroll pattern upward when frame is full; if 0 wraps from top. |
| start_full / full | bool | `1` | Pre-fill the entire frame before first output. |
| stitch | bool | `1` | Stitch left and right edges together (toroidal boundary). |

## Examples

### Rule 30 (chaotic, used in randomness)

```sh
ffplay -f lavfi "cellauto=size=800x400:rule=30"
```

### Rule 110 with a single live cell in the center

```sh
ffplay -f lavfi "cellauto=size=800x400:rule=110:pattern=1"
```

### Rule 90 (Sierpinski triangle)

```sh
ffplay -f lavfi "cellauto=size=800x400:rule=90:pattern=1:stitch=0"
```

### Record 10 seconds

```sh
ffmpeg -f lavfi -i "cellauto=size=800x400:rule=110" -t 10 cellauto.mp4
```

## Notes

- Wolfram rules classify into 4 classes: Class 1 (all die), Class 2 (periodic), Class 3 (chaotic — e.g. Rule 30), Class 4 (complex — e.g. Rule 110).
- Rule 110 is proven Turing-complete and produces intricate but non-random structures.
- Rule 90 with a single center cell and `stitch=0` produces the Sierpinski triangle fractal.
- The initial `pattern` string: each non-whitespace character = alive cell; spaces = dead.
