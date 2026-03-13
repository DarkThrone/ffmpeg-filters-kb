+++
title = "life"
description = "Simulate Conway's Game of Life (or generalized life rules) and render each generation as a video frame."
date = 2024-01-01

[taxonomies]
category = ["sources"]
tags = ["source", "generative", "simulation", "art"]

[extra]
filter_type = "source"
since = ""
see_also = ["cellauto", "mandelbrot"]
parameters = ["rule", "size", "rate", "filename", "random_fill_ratio", "stitch", "life_color", "death_color", "mold"]
cohort = 3
+++

The `life` source simulates John Conway's Game of Life — a 2D cellular automaton where each cell lives or dies based on its neighbor count. Each video frame shows one generation. The initial grid can be loaded from a file, or generated randomly. The rule is configurable using the `S/B` notation, allowing other "Life-like" cellular automata beyond the standard `S23/B3` rule.

## Quick Start

```sh
ffplay -f lavfi "life=size=640x480:rate=10"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second (generations per second). |
| rule | string | `S23/B3` | Survival/birth rule. `S` = neighbor counts to survive, `B` = to be born. |
| filename / f | string | — | Load initial grid from a text file. |
| random_fill_ratio / ratio | double | `1/φ ≈ 0.618` | Density of random initial grid. |
| random_seed / seed | int64 | random | Seed for random initial grid. |
| stitch | bool | `1` | Wrap edges (toroidal grid). |
| mold | int | `0` | Speed at which dead cells fade (0 = instant). |
| life_color | color | `white` | Color for alive cells. |
| death_color | color | `black` | Color for dead cells. |
| mold_color | color | `green` | Color for recently-dead cells when `mold > 0`. |

## Examples

### Default Conway's Life

```sh
ffplay -f lavfi "life=size=640x480:rate=10"
```

### Colorized life with mold effect

```sh
ffplay -f lavfi "life=size=640x480:rate=10:life_color=yellow:death_color=#1a1a2e:mold=5:mold_color=#4a4e69"
```

### HighLife rule (produces self-replicating patterns)

```sh
ffplay -f lavfi "life=size=640x480:rate=10:rule=S23/B36"
```

### Load a specific starting pattern

```sh
ffplay -f lavfi "life=f=glider.cells:rate=10:size=64x64"
```

### Record 30 seconds of Life simulation

```sh
ffmpeg -f lavfi -i "life=size=800x600:rate=30" -t 30 life.mp4
```

## Notes

- Default rule `S23/B3` is Conway's original: a cell survives with 2 or 3 neighbors; a dead cell is born with exactly 3.
- Alternative rules: `S23/B36` (HighLife — self-replicates), `S2/B36` (2x2), `S12345/B3` (Maze).
- Lower `rate` = slower playback (fewer generations/second); increase for faster animation.
- `mold > 0` makes dead cells fade gradually, creating a visual trail of past activity.
- Initial grid files use plaintext format (`.cells`): non-whitespace = alive, newline = new row.
