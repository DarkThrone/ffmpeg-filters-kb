+++
title = "drawtext"
description = "Render text strings or text files onto video frames using the libfreetype library, with full font, color, position, and animation control."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["text", "overlay", "annotation"]

[extra]
filter_type = "video"
since = ""
see_also = ["drawbox", "overlay", "fade"]
parameters = ["text", "fontfile", "fontsize", "fontcolor", "x", "y", "box", "boxcolor", "borderw", "bordercolor", "shadowx", "shadowy", "alpha", "expansion", "enable"]
cohort = 1
source_file = "libavfilter/vf_drawtext.c"
+++

The `drawtext` filter renders arbitrary text onto video frames using libfreetype for font rasterization. It supports custom fonts, background boxes, borders, drop shadows, per-frame dynamic text via expansion expressions, and time-based enabling/disabling. This makes it suitable for burned-in subtitles, timecodes, debug overlays, scrolling credits, and watermarks. Requires FFmpeg compiled with `--enable-libfreetype` (and optionally `--enable-libfontconfig` for font name lookup).

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "drawtext=text='Hello World':fontsize=48:fontcolor=white:x=10:y=10" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | string | — | The text string to render. Mutually exclusive with `textfile`. |
| textfile | string | — | Path to a text file whose contents are rendered. |
| fontfile | string | — | Path to a TrueType or OpenType font file. |
| font | string | `Sans` | Font family name (requires libfontconfig). |
| fontsize | string (expr) | `16` | Font size in pixels. Accepts expressions. |
| fontcolor | color | `black` | Text foreground color. Supports `@alpha` suffix (e.g., `white@0.5`). |
| x | string (expr) | `0` | Horizontal position of the text anchor. Evaluated per frame. |
| y | string (expr) | `0` | Vertical position of the text anchor. Evaluated per frame. |
| box | bool | `0` | Draw a filled background box behind the text. |
| boxcolor | color | `white` | Background box color. |
| boxborderw | string | `0` | Box border width(s), specified as one to four values (top\|right\|bottom\|left). |
| borderw | int | `0` | Width of the outline border drawn around each glyph. |
| bordercolor | color | `black` | Color of the glyph outline border. |
| shadowx | int | `0` | Horizontal shadow offset in pixels. |
| shadowy | int | `0` | Vertical shadow offset in pixels. |
| shadowcolor | color | `black` | Shadow color. |
| alpha | string (expr) | `1` | Text opacity expression, `0.0` (transparent) to `1.0` (opaque). |
| expansion | int | `normal` | Text expansion mode: `none` (literal), `normal` (FFmpeg expressions), `strftime` (deprecated). |
| enable | string (expr) | — | Boolean expression to control when the text is shown (e.g., `between(t,5,10)`). |
| timecode | string | — | Starting timecode in `HH:MM:SS;FF` format for timecode overlays. |
| reload | int | `0` | Re-read `textfile` every N frames (0 = once at init). |
| fix_bounds | bool | `0` | Automatically adjust text position to prevent clipping at frame edges. |
| line_spacing | int | `0` | Extra spacing between lines in pixels. |
| start_number | int | `0` | Starting value for the `n` (frame number) variable. |

## Expression Variables

When `expansion=normal` (default), the text string itself can contain `%{...}` expressions, and the position/alpha options can use:

| Variable | Description |
|----------|-------------|
| `w` / `tw` | Width of the rendered text |
| `h` / `th` | Height of the rendered text |
| `main_w` / `W` | Video frame width |
| `main_h` / `H` | Video frame height |
| `n` | Frame number |
| `t` | Timestamp in seconds |
| `pts` | Presentation timestamp in timebase units |
| `r` | Input frame rate |
| `x` / `y` | Current computed text position |
| `lh` | Line height |
| `lw` | Line width |
| `max_glyph_w` / `max_glyph_h` | Maximum glyph dimensions |

Within the `text` string with `expansion=normal`, use `%{pts}`, `%{n}`, `%{gmtime}`, etc.

## Examples

### Burned-in timestamp

Display the current timestamp in the top-left corner, updating every frame.

```sh
ffmpeg -i input.mp4 \
  -vf "drawtext=text='%{pts\\:hms}':fontsize=24:fontcolor=white:box=1:boxcolor=black@0.5:x=10:y=10" \
  output.mp4
```

### Centered white title with shadow

Render a title centered horizontally and positioned 50 pixels from the top, with a drop shadow for readability.

```sh
ffmpeg -i input.mp4 \
  -vf "drawtext=text='My Film':fontfile=/path/to/font.ttf:fontsize=64:fontcolor=white:shadowx=3:shadowy=3:x=(w-tw)/2:y=50" \
  output.mp4
```

### Scrolling credits (bottom to top)

Animate the y position over time so text scrolls upward from the bottom.

```sh
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Credits line 1\nLine 2\nLine 3':fontsize=32:fontcolor=white:x=(w-tw)/2:y=h-t*50" \
  output.mp4
```

### Show text only between 5 and 15 seconds

Use the `enable` expression to show the annotation only during a specific time window.

```sh
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Special Event':fontsize=40:fontcolor=yellow:x=50:y=50:enable='between(t,5,15)'" \
  output.mp4
```

### Fade-in text using alpha expression

Make the text gradually appear over the first 3 seconds using an alpha expression.

```sh
ffmpeg -i input.mp4 \
  -vf "drawtext=text='Fading In':fontsize=48:fontcolor=white:x=100:y=100:alpha='min(t/3,1)'" \
  output.mp4
```

## Notes

- Escape colons in the text string with `\\:` when using the `-vf` shorthand, or use `-filter_complex` with quoted strings for complex text.
- The `fontfile` path must be absolute or resolvable from the working directory. If `libfontconfig` is enabled, use the `font` option with a font family name instead.
- `drawtext` is CPU-intensive for complex expressions evaluated per frame; consider `enable` to limit rendering to visible periods.
- For overlaying external subtitle files, use the `subtitles` filter instead — it handles proper UTF-8 rendering and subtitle timing automatically.
