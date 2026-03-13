# FFmpeg Filters — Complete Reference

This file contains the full documentation for all FFmpeg filters in this
knowledge base, organized by category. It is intended for LLM ingestion,
semantic search indexing, and offline reference.

**Total filters documented:** 193

**Categories:**
- [Video Filters](#video) — 91 filters
- [Audio Filters](#audio) — 47 filters
- [Test Sources](#sources) — 16 filters
- [Visualization](#visualization) — 10 filters
- [Analysis & QC](#analysis) — 12 filters
- [Interlace & Telecine](#interlace) — 7 filters
- [Utility & Timing](#utility) — 10 filters

---

## Video Filters

### atadenoise

> Adaptive Temporal Averaging Denoiser that reduces video noise by averaging across multiple frames using adaptive thresholds.

**Source:** [libavfilter/vf_atadenoise.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_atadenoise.c)

The `atadenoise` filter reduces noise by averaging pixel values across multiple frames, adapting to scene content to avoid blurring in-motion areas. Per-plane thresholds (`a` and `b`) control sensitivity: threshold A reacts to abrupt changes (scene cuts, fast motion), while threshold B handles slow continuous changes (grain, sensor noise).

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "atadenoise" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| 0a | float | `0.02` | Threshold A for 1st plane (abrupt change sensitivity). Range: 0–0.3. |
| 0b | float | `0.04` | Threshold B for 1st plane (continuous change sensitivity). Range: 0–5. |
| 1a | float | `0.02` | Threshold A for 2nd plane. |
| 1b | float | `0.04` | Threshold B for 2nd plane. |
| 2a | float | `0.02` | Threshold A for 3rd plane. |
| 2b | float | `0.04` | Threshold B for 3rd plane. |
| s | int | `9` | Number of frames to average (must be odd, range 5–129). |
| p | flags | all | Planes to filter. |
| a | int | `parallel` | Algorithm variant: `parallel` or `serial`. |
| 0s / 1s / 2s | float | `32767` | Per-plane spatial sigma (pixel weight). 0 disables filtering. |

## Examples

### Mild denoising (default parameters)

```sh
ffmpeg -i grainy.mp4 -vf "atadenoise" output.mp4
```

### Stronger temporal denoising over 15 frames

```sh
ffmpeg -i film_grain.mp4 -vf "atadenoise=s=15:0a=0.05:0b=0.08" output.mp4
```

### Denoise only luma plane

```sh
ffmpeg -i input.mp4 -vf "atadenoise=p=1" output.mp4
```

### Higher thresholds for very noisy footage

```sh
ffmpeg -i vhs.mp4 -vf "atadenoise=0a=0.1:0b=0.2:1a=0.05:1b=0.1:s=9" output.mp4
```

## Notes

- Larger `s` (more frames) gives stronger denoising but requires more memory and can cause ghosting in fast-motion scenes.
- Threshold A controls sensitivity to sudden changes (fast motion, cuts) — keep it low to avoid motion blur artifacts.
- Threshold B controls sensitivity to slow drift (sensor noise, flicker) — increase it to remove more continuous noise.
- `parallel` mode is generally faster than `serial`, but `serial` can produce slightly better results by evaluating both sides of the frame window.

---

### blend

> Blend two video inputs together using compositing modes such as overlay, screen, multiply, and more.

**Source:** [libavfilter/vf_blend.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_blend.c)

The `blend` filter composites two video streams using Photoshop-style blending modes. It takes two inputs and applies a per-pixel blend operation to combine them. Each component can have a separate mode and opacity, or all components can share a single `all_mode`. This enables creative effects, colour grading, diffusion glow, and light leaks.

## Quick Start

```sh
# Overlay second video on first
ffmpeg -i base.mp4 -i overlay.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=overlay" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_mode | int | `normal` | Blend mode for all components. See mode list below. |
| all_opacity | float | `1.0` | Opacity of the blend (0=first input only, 1=fully blended). |
| all_expr | string | — | Custom blend expression per pixel. Variables: `X`, `Y`, `W`, `H`, `N`, `T`, `A` (top), `B` (bottom). |
| c0_mode | int | — | Blend mode for component 0 only. |
| c1_mode | int | — | Blend mode for component 1 only. |
| c2_mode | int | — | Blend mode for component 2 only. |
| c3_mode | int | — | Blend mode for component 3 (alpha) only. |

### Available blend modes

`normal`, `addition`, `grainmerge`, `and`, `average`, `burn`, `darken`, `difference`, `grainextract`, `divide`, `dodge`, `reflect`, `exclusion`, `extremity`, `freeze`, `glow`, `hardlight`, `hardmix`, `heat`, `lighten`, `linearlight`, `negation`, `or`, `overlay`, `phoenix`, `pinlight`, `softlight`, `screen`, `subtract`, `vividlight`, `xor`, `softdifference`, `geometric`, `harmonic`, `bleach`

## Examples

### Screen blend for glow effect

```sh
ffmpeg -i base.mp4 -i glow.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=screen:all_opacity=0.6" output.mp4
```

### Multiply blend for dark overlay

```sh
ffmpeg -i base.mp4 -i texture.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=multiply" output.mp4
```

### Difference blend for motion detection

Pixels that haven't changed appear black; changed pixels appear bright.

```sh
ffmpeg -i frame_a.mp4 -i frame_b.mp4 \
  -filter_complex "[0:v][1:v]blend=all_mode=difference" output.mp4
```

### Custom expression blend

Blend only the bright parts of the second stream.

```sh
ffmpeg -i base.mp4 -i overlay.mp4 \
  -filter_complex "[0:v][1:v]blend=all_expr='if(gt(B,128),B,A)'" output.mp4
```

## Notes

- `blend` requires two inputs in the same size and format. Use `scale` and `format` to match them before blending.
- `all_mode=normal:all_opacity=0.5` is equivalent to a 50% crossfade between the two streams.
- For per-frame temporal blending (blending consecutive frames of the same stream), use `tblend`.
- The `all_expr` custom mode supports the same FFmpeg expression syntax as `geq`, with `A` = top layer pixel and `B` = bottom layer pixel.

---

### bm3d

> Denoise video using Block-Matching 3D filtering for high-quality noise suppression.

**Source:** [libavfilter/vf_bm3d.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_bm3d.c)

The `bm3d` filter implements Block-Matching 3D denoising, one of the highest-quality denoising algorithms. It works by finding similar blocks throughout the frame, stacking them into a 3D array, and applying collaborative filtering in the transform domain. It supports a two-pass mode: a fast `basic` estimate followed by a high-quality `final` pass that uses the first estimate as a reference for even better denoising.

## Quick Start

```sh
# Single-pass BM3D
ffmpeg -i noisy.mp4 -vf "bm3d=sigma=5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sigma | float | `1.0` | Denoising strength. Higher = stronger. Typical range: 1–20. |
| block | int | `16` | Local patch (block) size. Must be a power of 2. |
| bstep | int | `4` | Step between processed blocks. Smaller = better quality, slower. |
| group | int | `1` | Maximum number of similar blocks per group. |
| range | int | `9` | Block matching search range. |
| mstep | int | `1` | Step for block matching search. |
| thmse | float | `0.0` | Block matching threshold. 0 = auto. |
| hdthr | float | `2.7` | Hard threshold for 3D transform. |
| estim | int | `basic` | Estimation mode: `basic` or `final`. |
| ref | bool | `0` | If true, expects a reference stream (second input) for final estimation. |
| planes | int | `7` | Bitmask of planes to filter. |

## Examples

### Single-pass with moderate strength

```sh
ffmpeg -i input.mp4 -vf "bm3d=sigma=4" output.mp4
```

### Two-pass BM3D for best quality

**Step 1**: Generate basic estimate and save to a pipe-accessible stream.

```sh
ffmpeg -i noisy.mp4 \
  -filter_complex "[0:v]split[noisy1][noisy2];[noisy1]bm3d=sigma=6:estim=basic[basic];[noisy2][basic]bm3d=sigma=6:estim=final:ref=1[out]" \
  -map "[out]" output.mp4
```

### Light denoising to preserve film grain

```sh
ffmpeg -i film.mp4 -vf "bm3d=sigma=2:block=8" output.mp4
```

## Notes

- Two-pass mode (basic → final) produces significantly better results than single-pass: the `basic` estimate provides a reference that guides the `final` pass to be more accurate.
- `sigma` is the key quality knob: values of 3–6 work well for typical camera noise; 8–15 for strong noise (ISO 3200+ photography).
- `bstep=1` (overlap every pixel) gives best quality at the cost of much higher CPU usage. Default `bstep=4` is a practical compromise.
- BM3D is slower than `hqdn3d` or `atadenoise` but produces less smearing and better preservation of texture.

---

### boxblur

> Apply a box (average) blur to video with separate radius and power settings per plane.

**Source:** [libavfilter/vf_boxblur.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_boxblur.c)

The `boxblur` filter blurs video by averaging each pixel with its rectangular neighbourhood (a box blur). It applies the blur `power` times for each plane, with separate `radius` and `power` settings for luma, chroma, and alpha. Radii can be expressions referencing video dimensions.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "boxblur=2:1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_radius / lr | string | `2` | Luma blur radius in pixels. Can be an expression using `w`, `h`, `min(w,h)`, etc. |
| luma_power / lp | int | `2` | Number of times the box blur is applied to the luma plane. |
| chroma_radius / cr | string | — | Chroma blur radius. Defaults to `luma_radius`. |
| chroma_power / cp | int | — | Chroma blur iterations. Defaults to `luma_power`. |
| alpha_radius / ar | string | — | Alpha blur radius. Defaults to `luma_radius`. |
| alpha_power / ap | int | — | Alpha blur iterations. Defaults to `luma_power`. |

## Examples

### Gentle blur

```sh
ffmpeg -i input.mp4 -vf "boxblur=1:1" output.mp4
```

### Radius proportional to video size

Use 2% of the smaller dimension as the blur radius.

```sh
ffmpeg -i input.mp4 -vf "boxblur=lr='min(w,h)*0.02':lp=1" output.mp4
```

### Blur chroma more than luma

Smooth colour noise while keeping sharpness.

```sh
ffmpeg -i input.mp4 -vf "boxblur=lr=1:lp=1:cr=3:cp=2" output.mp4
```

### Heavy blur for background defocus

```sh
ffmpeg -i input.mp4 -vf "boxblur=5:3" output.mp4
```

## Notes

- A box blur applied once is fast but produces visible square artifacts. Increasing `power` (applying the blur multiple times) approximates a Gaussian blur.
- Radius expressions can use `iw`/`ih` (input width/height), `ow`/`oh` (output width/height), and `min(iw,ih)`.
- For a smoother, more natural blur, `gblur` (Gaussian) is generally preferred; `boxblur` is faster for large radii.
- Setting `chroma_power=0` skips chroma blurring entirely, leaving colour saturation fully sharp.

---

### bwdif

> Deinterlace video using the motion-adaptive Bob Weaver Deinterlacing Filter for superior quality.

**Source:** [libavfilter/vf_bwdif.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_bwdif.c)

The `bwdif` filter ("Bob Weaver Deinterlacing Filter") is a motion-adaptive deinterlacer that uses temporal and spatial information to reconstruct missing lines. It generally produces cleaner results than `yadif` on fast motion, with fewer combing artifacts. It accepts the same parameters as `yadif` and can be used as a drop-in replacement.

## Quick Start

```sh
ffmpeg -i interlaced.mp4 -vf "bwdif" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `1` | Output mode: `0`=send_frame (one output per input frame), `1`=send_field (one output per field, doubles frame rate). |
| parity | int | `-1` | Field parity: `0`=top field first, `1`=bottom field first, `-1`=auto-detect. |
| deint | int | `0` | Which frames to deinterlace: `0`=all, `1`=only flagged interlaced frames. |

## Examples

### Standard deinterlacing

One progressive frame per input frame (default mode=1 outputs per field — use mode=0 for 1:1).

```sh
ffmpeg -i interlaced.mp4 -vf "bwdif=mode=0" output.mp4
```

### Double-rate output (field-based)

Output one frame per field for smooth high-frame-rate playback.

```sh
ffmpeg -i interlaced.ts -vf "bwdif=mode=1" -r 50 output.mp4
```

### Explicit BFF parity

```sh
ffmpeg -i bff_source.mp4 -vf "bwdif=mode=0:parity=1" output.mp4
```

## Notes

- `bwdif` is generally preferred over `yadif` when quality matters; it handles fast motion and fine diagonal edges better.
- The default `mode=1` (send_field) doubles the output frame rate. For 1:1 frame mapping, set `mode=0`.
- Like `yadif`, set `deint=1` to only deinterlace frames tagged as interlaced, passing through progressive frames unchanged.
- On hardware-accelerated pipelines (e.g. NVENC), use the vendor-specific deinterlacer instead, as software filters run on CPU.

---

### chromakey

> Remove a chroma key color from video (green/blue screen) by making matching pixels transparent.

**Source:** [libavfilter/vf_chromakey.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_chromakey.c)

The `chromakey` filter removes a chroma key color (typically green or blue) from video by making matching pixels transparent. It operates in YUV color space, which is more robust on compressed video formats than the RGB-based `colorkey`. This is the standard way to remove green screen and blue screen backgrounds in FFmpeg.

## Quick Start

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.1:0.1" keyed.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | color | `black` | The chroma key color. Accepts hex `0xRRGGBB` or named colors. Common: `0x00FF00` (green), `0x0000FF` (blue). |
| similarity | float | `0.01` | Color range to key out (YUV distance). Range: 0.01–1. Higher = more aggressive keying. |
| blend | float | `0.0` | Blending factor at the key boundary for soft edges. Range: 0–1. |
| yuv | bool | `0` | If enabled, the `color` parameter is specified in YUV values instead of RGB. |

## Examples

### Basic green screen removal

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.1:0.1" keyed.mp4
```

### Blue screen removal

```sh
ffmpeg -i bluescreen.mp4 -vf "chromakey=0x0000FF:0.15:0.05" keyed.mp4
```

### Composite over a new background

```sh
ffmpeg -i background.mp4 -i greenscreen.mp4 \
  -filter_complex "[1:v]chromakey=0x00FF00:0.1:0.1[fg];[0:v][fg]overlay" \
  output.mp4
```

### Adjust similarity for a spill-heavy key

Increase similarity to catch green spill on hair and edges.

```sh
ffmpeg -i greenscreen.mp4 -vf "chromakey=0x00FF00:0.25:0.15" keyed.mp4
```

## Notes

- `similarity` determines how broadly the key color is matched in YUV space. Values of 0.1–0.2 are typical for clean studio footage; increase up to 0.3–0.4 for compressed or poorly lit backgrounds.
- `blend` adds a soft transition at the edge, reducing aliasing but potentially showing some background colour at the border.
- `chromakey` works in YUV and is more resilient to H.264/H.265 chroma subsampling than `colorkey` (RGB). Prefer it for encoded footage.
- For best results, key before any other color correction — adjust the key color to the exact value of your screen.

---

### colorbalance

> Adjust the color balance of video by modifying red, green, and blue channel intensities in shadows, midtones, and highlights.

**Source:** [libavfilter/vf_colorbalance.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorbalance.c)

The `colorbalance` filter adjusts the intensity of red, green, and blue channels independently across three tonal regions: shadows (darkest pixels), midtones (medium pixels), and highlights (brightest pixels). Each adjustment is a value from -1.0 to 1.0, where positive shifts the balance toward the primary color and negative shifts it toward the complementary color. This makes it analogous to the Color Balance tool in photo editing applications.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rs=0.1:gs=-0.05:bs=-0.1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rs | float | `0` | Red channel adjustment in shadows. Range: [-1.0, 1.0]. |
| gs | float | `0` | Green channel adjustment in shadows. |
| bs | float | `0` | Blue channel adjustment in shadows. |
| rm | float | `0` | Red channel adjustment in midtones. |
| gm | float | `0` | Green channel adjustment in midtones. |
| bm | float | `0` | Blue channel adjustment in midtones. |
| rh | float | `0` | Red channel adjustment in highlights. |
| gh | float | `0` | Green channel adjustment in highlights. |
| bh | float | `0` | Blue channel adjustment in highlights. |
| pl | bool | `0` | Preserve lightness when adjusting color balance. Prevents color shifts from altering overall brightness. |

## Examples

### Add a warm sunset tone

Boost reds and reduce blues in midtones and highlights to create a warm, golden look.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rm=0.2:rh=0.1:bm=-0.15:bh=-0.1" output.mp4
```

### Add a cool cinematic look

Shift shadows toward blue and highlights toward teal for a common film grade.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=bs=0.2:gs=0.05:rh=-0.1:gh=0.05:bh=0.1" output.mp4
```

### Add red cast to shadows only

A subtle red-shadow treatment often used for dramatic film looks.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=rs=0.3" output.mp4
```

### Correct a blue color cast

Remove an unwanted blue cast from shadows while preserving midtones and highlights.

```sh
ffmpeg -i input.mp4 -vf "colorbalance=bs=-0.2:bm=-0.1" output.mp4
```

## Notes

- All range values are [-1.0, 1.0]; values outside this range are clamped. Setting all values to `0` (the default) passes the video through unchanged.
- Use `pl=1` (preserve lightness) when making strong color balance adjustments to prevent the overall brightness of the image from shifting.
- `colorbalance` adjusts the RGB channels after YUV-to-RGB conversion; it works on the pixel values directly and does not distinguish between chroma and luma.
- For finer tonal control, consider `curves` which allows per-channel spline adjustments, or combine `colorbalance` with `eq` for brightness/contrast alongside color adjustments.

---

### colorchannelmixer

> Adjust colors by mixing color channels using a 4×4 matrix transformation.

**Source:** [libavfilter/vf_colorchannelmixer.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorchannelmixer.c)

The `colorchannelmixer` filter remixes the R, G, B, and A channels of video by applying a 4×4 matrix transformation. Each output channel is computed as a weighted sum of all four input channels, enabling complex color grading operations such as channel swapping, cross-processing effects, and colorspace approximations. It is one of the most flexible color manipulation tools in FFmpeg.

## Quick Start

```sh
# Classic sepia tone
ffmpeg -i input.mp4 -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rr | double | `1` | Red gain for the red output channel. |
| rg | double | `0` | Green gain for the red output channel. |
| rb | double | `0` | Blue gain for the red output channel. |
| ra | double | `0` | Alpha gain for the red output channel. |
| gr | double | `0` | Red gain for the green output channel. |
| gg | double | `1` | Green gain for the green output channel. |
| gb | double | `0` | Blue gain for the green output channel. |
| ga | double | `0` | Alpha gain for the green output channel. |
| br | double | `0` | Red gain for the blue output channel. |
| bg | double | `0` | Green gain for the blue output channel. |
| bb | double | `1` | Blue gain for the blue output channel. |
| ba | double | `0` | Alpha gain for the blue output channel. |
| ar | double | `0` | Red gain for the alpha output channel. |
| ag | double | `0` | Green gain for the alpha output channel. |
| ab | double | `0` | Blue gain for the alpha output channel. |
| aa | double | `1` | Alpha gain for the alpha output channel. |

## Examples

### Sepia tone

Classic photographic sepia by mixing channels toward warm brown tones.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131" output.mp4
```

### Swap red and blue channels

Infrared-like effect by exchanging the red and blue channels.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=0:rb=1:br=1:bb=0" output.mp4
```

### Remove the red channel

Set the red output entirely to zero.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=0" output.mp4
```

### Cross-process look

Shift red toward yellow and blue toward cyan for a film cross-process effect.

```sh
ffmpeg -i input.mp4 -vf "colorchannelmixer=rr=1:rg=0.1:bg=-0.1:bb=1:gg=0.9:gb=0.1" output.mp4
```

## Notes

- The parameters are listed in row-major order: first the four coefficients for the red output (rr rg rb ra), then green (gr gg gb ga), blue (br bg bb ba), alpha (ar ag ab aa).
- The identity matrix (no change) is `rr=1:gg=1:bb=1:aa=1` with all off-diagonal values at 0 (the default).
- Values outside [0, 1] are valid and can produce saturating effects, but may clip the output.
- For simpler hue/saturation adjustments, `huesaturation` or `colorbalance` may be more intuitive.

---

### colorcontrast

> Adjust contrast between opposing color pairs (red-cyan, green-magenta, blue-yellow) in video.

**Source:** [libavfilter/vf_colorcontrast.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorcontrast.c)

The `colorcontrast` filter adjusts the contrast between complementary color pairs: red vs. cyan, green vs. magenta, and blue vs. yellow. Positive values push colors toward the primary and away from its complement; negative values do the opposite. Each pair also has a weight parameter (`rcw`, `gmw`, `byw`) to control influence on the final result.

## Quick Start

```sh
# Boost red-cyan contrast slightly
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rc | float | `0.0` | Red-cyan contrast. Positive=more red/less cyan; negative=more cyan/less red. Range: -1–1. |
| gm | float | `0.0` | Green-magenta contrast. Positive=more green; negative=more magenta. |
| by | float | `0.0` | Blue-yellow contrast. Positive=more blue; negative=more yellow. |
| rcw | float | `0.0` | Weight of red-cyan contrast in the final result. Range: 0–1. |
| gmw | float | `0.0` | Weight of green-magenta contrast in the final result. |
| byw | float | `0.0` | Weight of blue-yellow contrast in the final result. |
| pl | float | `0.0` | Amount of preserved luminance. Range: 0–1. |

## Examples

### Cool teal-and-orange look

Boost red-cyan contrast (push reds warmer) and add blue-yellow contrast.

```sh
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.3:by=-0.2:rcw=0.3:byw=0.2" output.mp4
```

### Increase green-magenta separation

```sh
ffmpeg -i nature.mp4 -vf "colorcontrast=gm=0.2:gmw=0.4" output.mp4
```

### Full complementary contrast enhancement

```sh
ffmpeg -i input.mp4 -vf "colorcontrast=rc=0.15:gm=0.1:by=0.1:rcw=0.3:gmw=0.3:byw=0.3" output.mp4
```

## Notes

- `rcw`, `gmw`, `byw` act as blend weights between the adjusted and original; setting them to 0 means no effect even if the adjustment values are non-zero.
- `pl` (preserve luminance) prevents color contrast adjustments from shifting the overall brightness of the image.
- This filter is particularly useful for subtle creative grading rather than technical correction; for technical color fixes, `colorbalance` or `colorlevels` are more precise.
- The range [-1, 1] for each contrast parameter; extreme values will significantly distort hues.

---

### colorize

> Overlay a solid color tint on video while preserving the original luminance.

**Source:** [libavfilter/vf_colorize.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorize.c)

The `colorize` filter applies a colored tint to video, similar to the duotone or colorize feature in Photoshop. It maps the video luminance through a specified hue and saturation, replacing all color information while keeping the lightness structure of the original. The `mix` parameter blends between the original and the colorized result.

## Quick Start

```sh
# Sepia-like warm orange tint
ffmpeg -i input.mp4 -vf "colorize=hue=30:saturation=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hue | float | `0.0` | Target hue in degrees. Range: 0–360. 0=red, 60=yellow, 120=green, 180=cyan, 240=blue, 300=magenta. |
| saturation | float | `0.5` | Saturation of the colorize effect. Range: 0–1. 0=grayscale, 1=fully colored. |
| lightness | float | `0.0` | Lightness shift. Range: -1–1. |
| mix | float | `1.0` | Blend between original (0) and fully colorized (1). |

## Examples

### Sepia tone

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=30:saturation=0.4:lightness=0.1" output.mp4
```

### Cold blue tint

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=210:saturation=0.5" output.mp4
```

### Subtle green tint (night vision feel)

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=120:saturation=0.3:mix=0.7" output.mp4
```

### 50% blend for soft color wash

```sh
ffmpeg -i input.mp4 -vf "colorize=hue=45:saturation=0.6:mix=0.5" output.mp4
```

## Notes

- `hue=0` (red) with `saturation=0.4` and `lightness=0.05` produces a classic sepia look.
- `saturation=0` is equivalent to desaturation — full grayscale with no tint.
- Unlike `hue` (which rotates existing colors), `colorize` replaces ALL chroma with a single uniform hue.
- `mix=0.5` is often more appealing than a full 1.0 colorize, as it retains some of the original color character.

---

### colorkey

> Remove a specific RGB color from video by making matching pixels transparent.

**Source:** [libavfilter/vf_colorkey.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorkey.c)

The `colorkey` filter removes a specific color from video by making pixels that match the key color fully or partially transparent. Unlike `chromakey` which operates in YUV color space, `colorkey` works in RGB and is more accurate for exact color matching. It is useful for removing solid colored backgrounds in title cards, motion graphics, and screen recordings.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "colorkey=0x00FF00:0.3:0.1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | color | `black` | The key color to remove. Accepts hex `0xRRGGBB` or color names. |
| similarity | float | `0.01` | Radius of colors to match. 0=exact match only, 1=all colors match. Range: 0–1. |
| blend | float | `0.0` | Softness of the edge. 0=hard cut, 1=gradual fade at boundary. Range: 0–1. |

## Examples

### Remove a green screen

```sh
ffmpeg -i greenscreen.mp4 -vf "colorkey=0x00FF00:0.3:0.1" keyed.mp4
```

### Remove white background from title card

```sh
ffmpeg -i title.mp4 -vf "colorkey=white:0.2:0.05" keyed.mp4
```

### Composite keyed video over background

Use `overlay` after `colorkey` to place the subject over a new background.

```sh
ffmpeg -i background.mp4 -i subject.mp4 \
  -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[keyed];[0:v][keyed]overlay" \
  output.mp4
```

### Soft key with blend for anti-aliased edges

```sh
ffmpeg -i input.mp4 -vf "colorkey=0x00B140:0.35:0.15" output.mp4
```

## Notes

- `colorkey` operates in RGB color space, making it precise for exact solid colors but potentially less robust on compressed video than `chromakey` (YUV).
- Start with `similarity=0.3` and `blend=0.1` for green screen work; adjust based on the cleanliness of your key color.
- Compressed video (H.264, etc.) often has chroma noise around key colors — increase `similarity` or `blend` to compensate.
- For true chroma key work (Rec. 709 YCbCr), `chromakey` usually gives cleaner results on encoded footage.

---

### colorlevels

> Adjust input and output black/white levels per channel, similar to Levels in Photoshop.

**Source:** [libavfilter/vf_colorlevels.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorlevels.c)

The `colorlevels` filter adjusts the black point, white point, and output range of each color channel independently. Setting the input black and white points remaps the tonal range, allowing you to correct washed-out footage or fix colour casts. It is equivalent to the Levels adjustment tool in Photoshop or Lightroom.

## Quick Start

```sh
# Remap input range 0.06–0.94 to full output range
ffmpeg -i input.mp4 -vf "colorlevels=rimin=0.06:gimin=0.06:bimin=0.06:rimax=0.94:gimax=0.94:bimax=0.94" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rimin | double | `0.0` | Input black point for red channel. Range: 0–1. |
| gimin | double | `0.0` | Input black point for green channel. |
| bimin | double | `0.0` | Input black point for blue channel. |
| aimin | double | `0.0` | Input black point for alpha channel. |
| rimax | double | `1.0` | Input white point for red channel. Range: 0–1. |
| gimax | double | `1.0` | Input white point for green channel. |
| bimax | double | `1.0` | Input white point for blue channel. |
| aimax | double | `1.0` | Input white point for alpha channel. |
| romin | double | `0.0` | Output black point for red channel. |
| gomin | double | `0.0` | Output black point for green channel. |
| bomin | double | `0.0` | Output black point for blue channel. |
| aomin | double | `0.0` | Output black point for alpha channel. |
| romax | double | `1.0` | Output white point for red channel. |
| gomax | double | `1.0` | Output white point for green channel. |
| bomax | double | `1.0` | Output white point for blue channel. |
| aomax | double | `1.0` | Output white point for alpha channel. |

## Examples

### Fix washed-out footage

Remap the actual signal range (0.06–0.94) to the full 0–1 range.

```sh
ffmpeg -i washed_out.mp4 -vf "colorlevels=rimin=0.06:gimin=0.06:bimin=0.06:rimax=0.94:gimax=0.94:bimax=0.94" output.mp4
```

### Correct a blue colour cast

Reduce the blue white point to pull down highlights in the blue channel.

```sh
ffmpeg -i bluish.mp4 -vf "colorlevels=bimax=0.85" output.mp4
```

### Add a fade-to-black (output remapping)

Limit the output range to 0–0.8 for a faded, low-contrast look.

```sh
ffmpeg -i input.mp4 -vf "colorlevels=romax=0.8:gomax=0.8:bomax=0.8" output.mp4
```

### Lift blacks (output black point)

Set output minimum to 0.05 for a film-print faded-black look.

```sh
ffmpeg -i input.mp4 -vf "colorlevels=romin=0.05:gomin=0.05:bomin=0.05" output.mp4
```

## Notes

- `imax` = input white point: pixels at this value or above are mapped to output white. Setting it below 1.0 stretches highlights.
- `imin` = input black point: pixels at this value or below are mapped to output black. Setting it above 0.0 crushes shadows.
- Values are 0–1 regardless of bit depth; the filter scales internally.
- For per-channel tonal curves, `curves` provides finer control; for simple contrast/brightness, `eq` is faster.

---

### colormatrix

> Convert between different color matrix standards such as BT.601, BT.709, and BT.2020.

**Source:** [libavfilter/vf_colormatrix.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colormatrix.c)

The `colormatrix` filter converts video between YCbCr color matrix standards. It is used to correct footage tagged with the wrong matrix or to prepare video for a specific delivery standard. Common uses include converting SD footage from BT.601 to BT.709 for HD deliverables, or handling legacy SMPTE 240M material.

## Quick Start

```sh
# Convert from SD (BT.601) to HD (BT.709)
ffmpeg -i sd_footage.mp4 -vf "colormatrix=bt601:bt709" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| src | int | Source color matrix. Options: `bt601`, `bt709`, `smpte240m`, `fcc`, `bt2020`. |
| dst | int | Destination color matrix. Same options as `src`. |

## Examples

### Convert SD to HD color matrix

```sh
ffmpeg -i sd.mp4 -vf "colormatrix=bt601:bt709" hd.mp4
```

### Convert to BT.2020 for HDR workflow

```sh
ffmpeg -i hd.mp4 -vf "colormatrix=bt709:bt2020" hdr_prep.mp4
```

### Fix incorrectly tagged footage

Footage recorded in SD but tagged as BT.709 — correct by applying BT.709→BT.601.

```sh
ffmpeg -i wrongly_tagged.mp4 -vf "colormatrix=bt709:bt601" corrected.mp4
```

## Notes

- `colormatrix` only changes the YCbCr matrix coefficients; it does not change the transfer function (gamma) or primary chromaticities. For a complete colorspace conversion, use `colorspace`.
- BT.601 is standard for SD (480i/576i); BT.709 is standard for HD (720p/1080p); BT.2020 is for UHD/HDR.
- After applying `colormatrix`, update the stream metadata with `-colorspace` and `-color_primaries` flags so players render correctly.
- Visually, the difference between BT.601 and BT.709 appears mostly in skin tones and reds — one will look slightly more saturated than the other.

---

### colorspace

> Convert between color spaces including primaries, transfer functions, and matrix coefficients.

**Source:** [libavfilter/vf_colorspace.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colorspace.c)

The `colorspace` filter performs comprehensive colorspace conversions, handling the matrix coefficients, color primaries, transfer function (gamma/PQ/HLG), and output pixel format together. It is more complete than `colormatrix` (which only handles the YCbCr matrix) and is suited for accurate conversions between SD, HD, and HDR standards.

## Quick Start

```sh
# Convert from BT.601 (SD) to BT.709 (HD)
ffmpeg -i sd.mp4 -vf "colorspace=all=bt709" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| all | int | Shortcut to set all properties simultaneously. Values: `bt601`, `bt709`, `bt2020-10`, `bt2020-12`, `bt2020-cl`, `smpte-170m`, `smpte-240m`, `bt470m`, `bt470bg`. |
| space | int | Output color matrix (YCbCr coefficients). Same values as `all`. |
| range | int | Output color range: `tv` (limited, 16–235 for 8-bit), `pc` (full, 0–255). |
| primaries | int | Output color primaries. Values: `bt470m`, `bt470bg`, `bt709`, `bt2020`. |
| trc | int | Output transfer characteristics (gamma). Values: `bt709`, `bt601`, `smpte240m`, `bt2020-10`, `bt2020-12`, `smpte2084`, `iec61966-2-1` (sRGB), `arib-std-b67` (HLG). |
| format | pixel_fmt | Output pixel format (e.g. `yuv420p`, `yuv420p10le`). |
| fast | bool | Use fast conversion (less accurate). |
| dither | int | Dithering method: `none`, `fsb` (Floyd-Steinberg). |

## Examples

### SD to HD color matrix conversion

```sh
ffmpeg -i sd.mp4 -vf "colorspace=all=bt709" hd.mp4
```

### Convert from SDR BT.709 to HLG (HDR)

```sh
ffmpeg -i sdr.mp4 -vf "colorspace=trc=arib-std-b67:primaries=bt2020:space=bt2020" hlg.mp4
```

### Full range to limited range

```sh
ffmpeg -i full_range.mp4 -vf "colorspace=range=tv" limited.mp4
```

### BT.2020 10-bit for HDR delivery

```sh
ffmpeg -i input.mp4 -vf "colorspace=all=bt2020-10:format=yuv420p10le" output_hdr.mp4
```

## Notes

- `all=bt709` is a convenient shortcut that sets space, primaries, and trc together to BT.709 standards — appropriate for most HD delivery.
- For HDR workflows, the transfer characteristic (`trc`) is critical: `smpte2084` is PQ (HDR10), `arib-std-b67` is HLG.
- `colorspace` converts between standards; it does not perform tone mapping. For HDR-to-SDR, chain with `tonemap`.
- Always set the output pixel format explicitly with `format=` when the downstream encoder requires a specific format (e.g. `yuv420p` for H.264).

---

### colortemperature

> Adjust the color temperature of video by shifting toward warm (low K) or cool (high K) tones.

**Source:** [libavfilter/vf_colortemperature.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_colortemperature.c)

The `colortemperature` filter adjusts the white balance of a video by simulating the effect of different color temperatures of light. Lower Kelvin values (2000–4000K) produce warm amber/orange tones (like candlelight or tungsten), while higher values (7000–10000K) produce cool blue tones (like a cloudy sky). It is useful for correcting footage shot under the wrong white balance preset.

## Quick Start

```sh
# Warm up footage to 3200K (tungsten warmth)
ffmpeg -i input.mp4 -vf "colortemperature=temperature=3200" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| temperature | float | `6500.0` | Color temperature in Kelvin. Range: 1000–40000. Lower=warmer, higher=cooler. |
| mix | float | `1.0` | Blend between original (0) and fully adjusted (1). Range: 0–1. |
| pl | float | `0.0` | Preserve luminance: 0 = allow luminance shift, 1 = preserve original luminance. |

## Examples

### Correct cool daylight footage to neutral 6500K

```sh
ffmpeg -i cool_footage.mp4 -vf "colortemperature=temperature=6500" output.mp4
```

### Warm up to 3200K (golden hour / tungsten look)

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=3200:mix=1" warm.mp4
```

### Cool down to 8000K (overcast / moonlight)

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=8000" cool.mp4
```

### 50% blend for subtle warm grade

```sh
ffmpeg -i input.mp4 -vf "colortemperature=temperature=4000:mix=0.5" subtle_warm.mp4
```

## Notes

- 6500K is approximately "daylight"; 5500K is slightly warm (afternoon sun); 3200K is tungsten (very warm orange).
- `mix=1.0` applies the full effect; lower values allow gradual adjustment or blending between corrected and original.
- `pl=1.0` prevents the filter from changing the overall brightness of the image while shifting color temperature.
- For fine-tuning skin tones without changing the entire frame, combine with `huesaturation=colors=r`.

---

### concat

> Concatenate multiple audio/video segments end-to-end into a single continuous stream.

**Source:** [libavfilter/avf_concat.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_concat.c)

The `concat` filter joins multiple synchronized video (and optionally audio) segments sequentially, producing a single continuous output stream. Unlike file-level concatenation, `concat` works inside the filtergraph, which allows you to filter each segment independently before joining. All segments must start at timestamp 0, have the same stream count per type, and matching resolution and format (or be explicitly normalized beforehand). The filter handles slight audio/video duration mismatches by padding the shorter stream with silence.

## Quick Start

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" \
  -map "[v]" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| n | int | `2` | Number of segments (input groups) to concatenate. |
| v | int | `1` | Number of video output streams (must equal the number of video streams per segment). |
| a | int | `0` | Number of audio output streams (must equal the number of audio streams per segment). |
| unsafe | bool | `0` | Allow segments with different formats to be concatenated without failing. |

### Input/output pad layout

The filter has `n x (v + a)` inputs and `v + a` outputs. Inputs are ordered: all streams for segment 1 first, then segment 2, etc. Within each segment, video streams come before audio streams.

## Examples

### Concatenate two video-only clips

Join two clips that share the same resolution and format.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[outv]" \
  -map "[outv]" output.mp4
```

### Concatenate two clips with audio

Handle both video and audio streams from each segment.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" output.mp4
```

### Concatenate three clips with bilingual audio

Each segment has one video stream and two audio streams.

```sh
ffmpeg -i open.mkv -i ep.mkv -i end.mkv \
  -filter_complex \
    "[0:0][0:1][0:2][1:0][1:1][1:2][2:0][2:1][2:2]concat=n=3:v=1:a=2[v][a1][a2]" \
  -map "[v]" -map "[a1]" -map "[a2]" output.mkv
```

### Normalize resolutions before concatenating

Scale both clips to the same resolution before `concat` to avoid errors.

```sh
ffmpeg -i part1.mp4 -i part2.mp4 \
  -filter_complex \
    "[0:v]scale=1280:720,setpts=PTS-STARTPTS[v1]; \
     [1:v]scale=1280:720,setpts=PTS-STARTPTS[v2]; \
     [v1][v2]concat=n=2:v=1:a=0[v]" \
  -map "[v]" output.mp4
```

## Notes

- Every segment must begin at timestamp 0. Insert `setpts=PTS-STARTPTS` (and `asetpts=PTS-STARTPTS` for audio) before `concat` if your segments were trimmed or have non-zero start times.
- All corresponding streams across segments must have the same resolution, pixel format, sample rate, and channel layout. Use `scale`, `format`, `aformat`, etc. to normalize before concatenating.
- The `concat` filter adjusts for slight duration differences between synchronized video and audio within a segment by padding the shorter stream; it cannot fix large desync issues.
- Variable frame rate output is produced if segments have different frame rates; ensure the muxer and player support VFR, or normalize with `fps` after `concat`.

---

### copy

> Pass video frames through unchanged — a null operation useful for testing and filter graph anchoring.

**Source:** [libavfilter/vf_copy.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_copy.c)

The `copy` filter passes every video frame through without any modification. It has no parameters and performs no transformation. Its primary uses are: verifying that a filter graph is connected correctly, benchmarking the overhead of the filter graph itself, and forcing a frame copy when sharing the same buffer between multiple filter chains would cause issues.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "copy" output.mp4
```

## Examples

### Passthrough with re-encode

```sh
ffmpeg -i input.mp4 -vf "copy" -c:v libx264 output.mp4
```

### Force a copy in filter_complex

```sh
ffmpeg -i input.mp4 -filter_complex "[0:v]copy[out]" -map "[out]" output.mp4
```

## Notes

- `copy` is the video equivalent of the `anull` audio filter: it does nothing to the data but is a valid node in a filter graph.
- In most cases you do not need `copy`; `-vf ""` (empty filter) or simply omitting `-vf` achieves the same result.
- It can be useful for benchmarking: `ffmpeg -i input.mp4 -vf "copy" -f null -` measures the muxing/filter overhead without any actual processing.

---

### crop

> Crop the input video to a specified rectangular region.

**Source:** [libavfilter/vf_crop.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_crop.c)

The `crop` filter extracts a rectangular sub-region from each video frame by specifying the output width, height, and the top-left corner coordinates within the input frame. Width and height default to the full input dimensions, and coordinates default to the center, so you only need to specify what you want to change. All parameters accept arithmetic expressions evaluated either once at init or per-frame, enabling dynamic panning crops.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "crop=1280:720:0:0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| w (out_w) | string (expr) | `iw` | Width of the cropped output area. |
| h (out_h) | string (expr) | `ih` | Height of the cropped output area. |
| x | string (expr) | `(iw-ow)/2` | Horizontal position of the top-left corner. Evaluated per frame. |
| y | string (expr) | `(ih-oh)/2` | Vertical position of the top-left corner. Evaluated per frame. |
| keep_aspect | bool | 0 | Preserve the input display aspect ratio by adjusting the sample AR. |
| exact | bool | 0 | Enable exact cropping for subsampled formats instead of rounding to the nearest subsample boundary. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output (cropped) width |
| `oh` / `out_h` | Output (cropped) height |
| `x` | Current computed x offset |
| `y` | Current computed y offset |
| `a` | Input aspect ratio (`iw/ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `n` | Frame number, starting from 0 |
| `t` | Timestamp in seconds |

## Examples

### Crop a fixed region

Extract a 640x480 rectangle starting at column 100, row 50.

```sh
ffmpeg -i input.mp4 -vf "crop=640:480:100:50" output.mp4
```

### Center crop to square

Crop the largest centered square from any video by using the shorter dimension as both width and height.

```sh
ffmpeg -i input.mp4 -vf "crop=in_h:in_h" output.mp4
```

### Crop to 16:9 from center

Remove letterbox or pillarbox bars by cropping to a specific aspect ratio without knowing the exact pixel offset.

```sh
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4
```

### Animated pan crop (left to right)

Move the crop window from left to right across the frame over time, creating a horizontal pan effect.

```sh
ffmpeg -i input.mp4 -vf "crop=640:480:t*100:0" output.mp4
```

### Remove 10-pixel border from all sides

Trim an even border by shrinking width and height by 20 pixels each and placing the origin at (10, 10).

```sh
ffmpeg -i input.mp4 -vf "crop=iw-20:ih-20:10:10" output.mp4
```

## Notes

- The `x` and `y` expressions are evaluated per frame and can reference each other and the current timestamp `t`, enabling panning crops.
- If the evaluated `x` or `y` would push the crop region outside the input frame, FFmpeg clamps it to the nearest valid value automatically.
- For YUV formats with chroma subsampling, crop coordinates are rounded to subsample boundaries unless `exact=1` is set.
- `w` and `h` expressions are evaluated only once at init (or on command), not per frame; use `x`/`y` for animation.

---

### cropdetect

> Auto-detect the optimal crop parameters to remove black borders from video.

**Source:** [libavfilter/vf_cropdetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_cropdetect.c)

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

---

### curves

> Adjust component curves using cubic splines with named presets or custom control points.

**Source:** [libavfilter/vf_curves.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_curves.c)

The `curves` filter applies cubic spline tone curves to each color channel independently (or all together via `master`). It supports built-in presets for common looks and custom point lists for precise tonal control. It is the FFmpeg equivalent of the Curves tool in Photoshop or Lightroom.

## Quick Start

```sh
# Warm highlights, cool shadows
ffmpeg -i input.mp4 -vf "curves=r='0/0 0.5/0.56 1/1':b='0/0 0.5/0.44 1/1'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| preset | int | Named preset: `none`, `color_negative`, `cross_process`, `darker`, `increase_contrast`, `lighter`, `linear_contrast`, `medium_contrast`, `negative`, `strong_contrast`, `vintage`. |
| master / m | string | Master (applied to all channels) control points. Format: `x/y x/y ...` where each value is 0–1. |
| red / r | string | Red channel control points. |
| green / g | string | Green channel control points. |
| blue / b | string | Blue channel control points. |
| all | string | Alternative to `master`; sets all channels at once. |
| psfile | string | Path to a Photoshop `.acv` curves file. |

## Examples

### Apply a built-in vintage preset

```sh
ffmpeg -i input.mp4 -vf "curves=preset=vintage" output.mp4
```

### Increase contrast with S-curve

Lift shadows and push highlights apart for a contrast-boosting S-curve.

```sh
ffmpeg -i input.mp4 -vf "curves=master='0/0 0.25/0.18 0.5/0.5 0.75/0.82 1/1'" output.mp4
```

### Warm red/orange grade

Boost reds in highlights and reduce blues in shadows.

```sh
ffmpeg -i input.mp4 -vf "curves=r='0/0 0.5/0.55 1/1':b='0/0.05 0.5/0.45 1/0.9'" output.mp4
```

### Negative film look

Invert and adjust contrast for a film-negative effect.

```sh
ffmpeg -i input.mp4 -vf "curves=preset=color_negative" output.mp4
```

## Notes

- Control points are specified as space-separated `x/y` pairs, where `0/0` is the bottom-left (black) and `1/1` is the top-right (white). Points must be in ascending x order.
- At least 2 points are needed per curve; the curve is extrapolated outside the provided range.
- `preset` and custom per-channel points can be combined: the preset is applied first, then custom adjustments on top.
- For simple brightness/contrast/gamma, `eq` is faster. For full tonal sculpting, `curves` is more powerful.

---

### deband

> Remove banding artifacts from video caused by insufficient bit depth or heavy compression.

**Source:** [libavfilter/vf_deband.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_deband.c)

The `deband` filter removes banding artifacts — visible color steps or bands in smooth gradients — that result from insufficient bit depth, aggressive lossy compression, or converting from 10-bit to 8-bit. It works by detecting areas where neighboring pixels have a similar value and smoothing them, replacing hard boundaries with gradual transitions.

## Quick Start

```sh
ffmpeg -i banded.mp4 -vf "deband" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| 1thr | float | `0.02` | Threshold for plane 1 (Y/luma). Lower = more aggressive. Range: 0.00003–0.5. |
| 2thr | float | `0.02` | Threshold for plane 2 (Cb/U). |
| 3thr | float | `0.02` | Threshold for plane 3 (Cr/V). |
| 4thr | float | `0.02` | Threshold for plane 4 (alpha). |
| range | int | `16` | Sampling range. Larger = catches more distant banding but slower. Range: 1–64. |
| direction | float | `6.28` | LFO direction sweep angle in radians. Default 6.28 (full 360°) = random directions. |
| blur | bool | `true` | Apply a blur to the detected banding areas for smooth transitions. |
| coupling | bool | `false` | If true, deband all planes together based on the luma plane decision. |

## Examples

### Remove banding from 8-bit SDR content

```sh
ffmpeg -i banded.mp4 -vf "deband" output.mp4
```

### Aggressive debanding (for heavy banding)

```sh
ffmpeg -i heavily_banded.mp4 -vf "deband=1thr=0.04:2thr=0.04:3thr=0.04" output.mp4
```

### Large range for wide, smooth gradients

```sh
ffmpeg -i sky_gradient.mp4 -vf "deband=range=32" output.mp4
```

### Deband before re-encoding to prevent banding propagation

```sh
ffmpeg -i input.mp4 -vf "deband" -c:v libx264 -crf 18 output.mp4
```

## Notes

- The thresholds (`1thr`–`4thr`) control sensitivity: lower values debands more aggressively but may smear fine detail. `0.02` is a safe default; increase to `0.04`–`0.06` for severe banding.
- `range` controls how far apart the comparison pixels are sampled. Wider gradients benefit from larger ranges (16–32).
- `blur=true` (default) applies smoothing to the banded regions — disable it to see only the banding detection result.
- Dithering before encoding can prevent banding from occurring in the first place; `deband` fixes it after the fact.

---

### deblock

> Remove blocking artifacts from heavily compressed video by detecting and smoothing block edges.

**Source:** [libavfilter/vf_deblock.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_deblock.c)

The `deblock` filter removes the blocky artifacts introduced by strong video compression (such as low-bitrate H.264 or MPEG-2). It detects block boundaries by looking for step edges at regular intervals and smooths them, with configurable thresholds to avoid blurring actual scene edges.

## Quick Start

```sh
ffmpeg -i blocky.mp4 -vf "deblock" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filter | int | `strong` | Filter type: `weak` or `strong`. Strong gives more deblocking. |
| block | int | `8` | Block size in pixels. Range: 4–512. Should match compression block size. |
| alpha | float | `0.098` | Detection threshold at exact block edge. 0 disables. |
| beta | float | `0.05` | Detection threshold near block edge (below/left). |
| gamma | float | `0.05` | Detection threshold near block edge (above). |
| delta | float | `0.05` | Detection threshold near block edge (right). |
| planes | int | `15` | Bitmask of planes to filter (15 = all). |

## Examples

### Standard deblocking for H.264 video

```sh
ffmpeg -i compressed.mp4 -vf "deblock=filter=strong:block=8" output.mp4
```

### Weak filter for mild artifacts

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=weak:block=4" output.mp4
```

### Aggressive deblocking with custom thresholds

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=strong:block=4:alpha=0.12:beta=0.07:gamma=0.06:delta=0.05" output.mp4
```

### Deblock only luma plane

```sh
ffmpeg -i input.mp4 -vf "deblock=filter=strong:block=8:planes=1" output.mp4
```

### Target 16×16 macroblocks (MPEG-2)

```sh
ffmpeg -i mpeg2.mpg -vf "deblock=block=16:filter=strong" output.mp4
```

## Notes

- Set `block` to match the encoder's block size: 8×8 for H.264/H.265, 16×16 for MPEG-2.
- Higher threshold values (`alpha`, `beta`, `gamma`, `delta`) give stronger deblocking but risk blurring real edges. Start with defaults.
- Setting any threshold to 0 disables deblocking along that specific edge direction.
- `strong` filter works at both the block edge and within adjacent blocks; `weak` only smooths the edge itself.

---

### deshake

> Stabilize shaky video by detecting and compensating for small frame-to-frame motion.

**Source:** [libavfilter/vf_deshake.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_deshake.c)

The `deshake` filter reduces camera shake by detecting the motion between consecutive frames within a search region and applying an inverse transformation. It operates entirely within a single pass and is straightforward to use, though for best results on heavily shaken footage, the two-pass `vidstabdetect`/`vidstabtransform` workflow (from the `vid.stab` library) provides superior quality.

## Quick Start

```sh
ffmpeg -i shaky.mp4 -vf "deshake" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | int | `-1` | Left edge of the analysis rectangle. -1 = auto (full width). |
| y | int | `-1` | Top edge of the analysis rectangle. |
| w | int | `-1` | Width of the analysis rectangle. -1 = use full frame width. |
| h | int | `-1` | Height of the analysis rectangle. |
| rx | int | `16` | Maximum horizontal search range in pixels. |
| ry | int | `16` | Maximum vertical search range in pixels. |
| edge | int | `mirror` | Edge fill method: `blank` (black border), `original`, `clamp`, `mirror`. |
| blocksize | int | `8` | Block size for motion estimation. Range: 4–128. |
| contrast | int | `125` | Minimum block contrast for motion estimation. Range: 1–255. |
| search | int | `exhaustive` | Search method: `exhaustive` or `less_exhaustive`. |

## Examples

### Basic stabilization

```sh
ffmpeg -i shaky.mp4 -vf "deshake" output.mp4
```

### Limit analysis to center of frame

Stabilize based on the center 50% of the frame (useful if edges have unrelated motion).

```sh
ffmpeg -i input.mp4 -vf "deshake=x=320:y=180:w=640:h=360" output.mp4
```

### Wider search range for heavily shaken footage

```sh
ffmpeg -i very_shaky.mp4 -vf "deshake=rx=32:ry=32" output.mp4
```

### Mirror edge fill (less distracting borders)

```sh
ffmpeg -i input.mp4 -vf "deshake=edge=mirror" output.mp4
```

## Notes

- `deshake` is a simple stabilizer suitable for handheld wobble. For complex motion (panning, zoom) or very heavy shake, use `vidstabdetect` + `vidstabtransform` (requires the `vid.stab` library).
- Edge fill artifacts are inevitable when compensating for motion; `edge=mirror` produces cleaner-looking results than `edge=blank` (black borders).
- `rx` and `ry` define the maximum allowed correction per frame. If the shake exceeds these values, the frame is only partially corrected.
- The filter operates in a single pass, so it cannot look ahead to smooth out slow drifts. `vidstabtransform` handles this better with its `smoothing` parameter.

---

### drawbox

> Draw a colored rectangle (box) onto the input video, with configurable position, size, thickness, and color.

**Source:** [libavfilter/vf_drawbox.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_drawbox.c)

The `drawbox` filter draws a rectangle border (or a filled rectangle) directly onto video frames. It is frequently used for debugging bounding boxes from detection pipelines, highlighting regions of interest, adding visual framing to clips, or creating simple graphic overlays. All geometry parameters accept arithmetic expressions evaluated per frame, enabling animated boxes.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=50:w=200:h=150:color=red:t=3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | string (expr) | `0` | Horizontal position of the left edge of the box. |
| y | string (expr) | `0` | Vertical position of the top edge of the box. |
| width (w) | string (expr) | `0` (= input width) | Width of the box. |
| height (h) | string (expr) | `0` (= input height) | Height of the box. |
| color (c) | string | `black` | Box color. Supports `color@alpha` notation and the special value `invert`. |
| thickness (t) | string (expr) | `3` | Thickness of the box border in pixels. Use `fill` for a solid filled box. |
| replace | bool | `0` | When `1`, overwrite video pixels including alpha. Default composites over the video. |
| box_source | string | — | Use bounding box from frame side-data (e.g., `side_data_detection_bboxes`) instead of manual parameters. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `x` / `y` | Current box position |
| `w` / `h` | Current box dimensions |
| `t` | Box border thickness |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `hsub` / `vsub` | Chroma subsample values |

## Examples

### Draw a red border box

Outline a region with a 3-pixel red border.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=100:y=50:w=200:h=150:color=red:t=3" output.mp4
```

### Draw a semi-transparent filled box

Create a translucent highlight rectangle by using `t=fill` and `@alpha` on the color.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=10:y=10:w=300:h=100:color=yellow@0.5:t=fill" output.mp4
```

### Black border around the entire frame

Draw a box that traces the frame edge — useful for adding a clean visual border.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=0:y=0:w=iw:h=ih:color=black:t=4" output.mp4
```

### Inverted color box

Use `invert` as the color to draw a box whose color is the complement of the video content underneath.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=50:y=50:w=100:h=100:color=invert:t=2" output.mp4
```

### Animated box tracking position over time

Move the box diagonally across the frame as a function of the frame timestamp.

```sh
ffmpeg -i input.mp4 -vf "drawbox=x=t*30:y=t*20:w=100:h=60:color=lime:t=2" output.mp4
```

## Notes

- The `color` parameter accepts any FFmpeg color string, including hex codes (`#FF0000`), named colors, and alpha suffixes (`red@0.3`).
- Setting `t=fill` creates a filled rectangle; any numeric value draws only the border at that pixel thickness.
- When `box_source=side_data_detection_bboxes` is set, the `x`, `y`, `w`, and `h` parameters are ignored in favor of bounding box data embedded in the frame side-data by detection filters.
- For multiple boxes at different positions, chain multiple `drawbox` filters separated by commas.

---

### drawtext

> Render text strings or text files onto video frames using the libfreetype library, with full font, color, position, and animation control.

**Source:** [libavfilter/vf_drawtext.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_drawtext.c)

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

---

### edgedetect

> Detect and visualize edges in video using Canny edge detection or color mixing.

**Source:** [libavfilter/vf_edgedetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_edgedetect.c)

The `edgedetect` filter detects edges in video frames using the Canny algorithm, with multiple output modes for creative and analytical use. In `wires` mode, it produces a classic edge-detection output (bright lines on black). In `colormix` mode, it blends the edge signal with the original video for an artistic effect.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.1:high=0.4" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| high | double | `0.12` | High threshold for Canny hysteresis (0–1). Pixels above this are definite edges. |
| low | double | `0.08` | Low threshold for Canny hysteresis. Pixels between low and high are edges only if adjacent to a definite edge. |
| mode | int | `wires` | Output mode: `wires` (edges on black bg), `colormix` (blend edges with source), `canny` (raw Canny output). |
| planes | flags | `7` | Which planes to apply edge detection on. 1=Y, 2=Cb, 4=Cr. |

## Examples

### Classic white edges on black background

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.05:high=0.2:mode=wires" output.mp4
```

### Artistic colormix edge effect

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.1:high=0.3:mode=colormix" output.mp4
```

### Fine detail edge map for luma only

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.02:high=0.1:planes=1" output.mp4
```

### High threshold for strong edges only

```sh
ffmpeg -i input.mp4 -vf "edgedetect=low=0.2:high=0.5" output.mp4
```

## Notes

- The Canny algorithm uses hysteresis: pixels above `high` are strong edges; pixels above `low` that are connected to strong edges are also kept. This produces cleaner, continuous edge lines than a simple threshold.
- Lower `low`/`high` values detect more (and weaker) edges; higher values detect only the strongest edges.
- `mode=wires` is most useful for visualization and artistic effects; `mode=canny` outputs the raw Canny gradient for analytical use.
- Combine with `negate` after `wires` mode for dark-edge-on-light-background sketch effect.

---

### eq

> Adjust brightness, contrast, saturation, and gamma of the input video with per-channel gamma support.

**Source:** [libavfilter/vf_eq.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_eq.c)

The `eq` filter provides traditional video equalizer controls: brightness, contrast, saturation, and gamma. It supports per-channel gamma adjustments (red, green, blue) for fine-grained color grading, and all parameters accept arithmetic expressions, enabling dynamic changes per frame. The filter can be applied once at initialization or reevaluated every frame depending on the `eval` setting.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "eq=brightness=0.1:contrast=1.2:saturation=1.3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| brightness | string (expr) | `0` | Brightness offset. Range: [-1.0, 1.0]. `0` = no change. |
| contrast | string (expr) | `1` | Contrast multiplier. Range: [-1000.0, 1000.0]. `1` = no change. |
| saturation | string (expr) | `1` | Saturation multiplier. Range: [0.0, 3.0]. `1` = no change, `0` = grayscale. |
| gamma | string (expr) | `1` | Overall gamma correction. Range: [0.1, 10.0]. `1` = no change. |
| gamma_r | string (expr) | `1` | Gamma correction for the red channel. Range: [0.1, 10.0]. |
| gamma_g | string (expr) | `1` | Gamma correction for the green channel. Range: [0.1, 10.0]. |
| gamma_b | string (expr) | `1` | Gamma correction for the blue channel. Range: [0.1, 10.0]. |
| gamma_weight | string (expr) | `1` | Reduces gamma effect on bright areas. Range: [0.0, 1.0]. `0` = no gamma, `1` = full gamma. |
| eval | int | `init` | When to evaluate expressions: `init` (once) or `frame` (per frame). |

### Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Frame count, starting from 0 |
| `r` | Frame rate of the input video |
| `t` | Timestamp in seconds |

## Examples

### Increase brightness and contrast

Brighten a slightly underexposed clip and add some contrast punch.

```sh
ffmpeg -i input.mp4 -vf "eq=brightness=0.08:contrast=1.3" output.mp4
```

### Warm color grade with gamma

Apply a slight red boost via gamma_r and reduce blue for a warm look.

```sh
ffmpeg -i input.mp4 -vf "eq=gamma_r=1.1:gamma_b=0.9:saturation=1.2" output.mp4
```

### Convert to grayscale (via saturation)

Set saturation to 0 to remove all color.

```sh
ffmpeg -i input.mp4 -vf "eq=saturation=0" output.mp4
```

### Dynamic brightness change over time

Use `eval=frame` and a `t`-based expression to animate brightness as a function of time.

```sh
ffmpeg -i input.mp4 -vf "eq=brightness='0.1*sin(t)':eval=frame" output.mp4
```

### Fix underexposed dark footage with gamma

Lift the shadows using gamma correction while protecting the highlights with `gamma_weight`.

```sh
ffmpeg -i input.mp4 -vf "eq=gamma=1.5:gamma_weight=0.5" output.mp4
```

## Notes

- Contrast values below `-1` or above `1` create increasingly extreme effects; use values close to `1.0` for subtle grading.
- `gamma_weight` is used to prevent blown-out highlights when boosting overall gamma — a value of `0.5` keeps bright areas from becoming completely white.
- When `eval=frame`, expressions are re-evaluated for every frame, which allows animation but has a small CPU overhead. Use `eval=init` for static corrections.
- `eq` uses an approximate gamma calculation rather than a fully color-managed workflow; for precision color work, consider `curves` or `lut3d` with a proper ICC profile.

---

### exposure

> Adjust the exposure and black level of video in EV stops.

**Source:** [libavfilter/vf_exposure.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_exposure.c)

The `exposure` filter adjusts the overall brightness of video using an exposure compensation value expressed in EV (exposure value) stops, similar to the exposure slider in photo editing applications. Positive values brighten; negative values darken. The `black` parameter independently lifts or lowers the black point.

## Quick Start

```sh
# Increase exposure by 1 stop
ffmpeg -i input.mp4 -vf "exposure=exposure=1.0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exposure | float | `0.0` | Exposure correction in EV stops. Range: -3.0–3.0. Each stop doubles/halves the brightness. |
| black | float | `0.0` | Black level correction. Range: -1.0–1.0. Positive lifts shadows, negative crushes blacks. |

## Examples

### Recover underexposed footage (+1 stop)

```sh
ffmpeg -i dark.mp4 -vf "exposure=exposure=1.0" output.mp4
```

### Slightly darken overexposed video

```sh
ffmpeg -i bright.mp4 -vf "exposure=exposure=-0.5" output.mp4
```

### Lift blacks for a fade/matte effect

```sh
ffmpeg -i input.mp4 -vf "exposure=black=0.05" output.mp4
```

### Combine exposure correction with black point lift

```sh
ffmpeg -i input.mp4 -vf "exposure=exposure=0.5:black=0.02" output.mp4
```

## Notes

- Each EV stop doubles the brightness: +1 EV = 2× brighter, +2 EV = 4× brighter, -1 EV = half as bright.
- `exposure` operates in linear light, making it more perceptually uniform than a simple multiply (e.g. `eq=brightness`).
- For non-linear brightness adjustment (S-curves, contrast), `eq` or `curves` provide more control.
- On HDR content, `exposure` can be combined with `tonemap` for HDR-to-SDR workflows.

---

### extractplanes

> Extract individual color plane components (Y, U, V, R, G, B, A) from a video stream as separate grayscale output streams.

**Source:** [libavfilter/vf_extractplanes.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_extractplanes.c)

The `extractplanes` filter splits a multi-component video stream into separate single-plane grayscale streams — one per color component. This is useful for processing individual planes independently (e.g. applying different filters to Y and UV planes), analyzing specific channels, or as part of a processing pipeline where planes are later recombined with `mergeplanes`. It is a multiple-output filter and requires `-filter_complex`.

## Quick Start

```sh
# Extract Y, U, V planes into 3 separate files
ffmpeg -i input.mp4 -filter_complex 'extractplanes=y+u+v[y][u][v]' \
  -map '[y]' y.mp4 -map '[u]' u.mp4 -map '[v]' v.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| planes | flags | — | Planes to extract, combined with `+`: `y`, `u`, `v`, `a`, `r`, `g`, `b`. |

## Examples

### Extract all YUV planes

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'extractplanes=y+u+v[y][u][v]' \
  -map '[y]' luma.avi \
  -map '[u]' cb.avi \
  -map '[v]' cr.avi
```

### Extract luma only for analysis

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'extractplanes=y[y]' \
  -map '[y]' luma_only.mp4
```

### Extract RGB planes from an RGB source

```sh
ffmpeg -i input.png \
  -filter_complex 'extractplanes=r+g+b[r][g][b]' \
  -map '[r]' red.png \
  -map '[g]' green.png \
  -map '[b]' blue.png
```

### Extract alpha channel

```sh
ffmpeg -i input_with_alpha.mov \
  -filter_complex 'extractplanes=a[a]' \
  -map '[a]' alpha_mask.mp4
```

## Notes

- You cannot mix YUV and RGB planes in the same `extractplanes` call — they come from different pixel formats.
- The filter outputs one stream per plane, in the order they appear in the `planes` option.
- Use `mergeplanes` to recombine processed planes back into a single stream.
- `extractplanes=y` is roughly equivalent to `format=gray` but without any colorspace conversion.

---

### fade

> Apply a fade-in or fade-out effect to video, transitioning from or to a solid color.

**Source:** [libavfilter/vf_fade.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_fade.c)

The `fade` filter applies a gradual transparency transition, fading the video in from a solid color (fade-in) or out to a solid color (fade-out). You can target the effect by frame count or by timestamp, making it straightforward to add polished beginnings and endings to clips. When `alpha=1` is set, only the alpha channel is faded, which is useful for compositing workflows.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type (t) | int | `in` | Fade direction: `in` (black to video) or `out` (video to color). |
| start_frame (s) | int | `0` | Frame number at which the effect begins (frame-based mode). |
| nb_frames (n) | int | `25` | Number of frames over which the fade is applied (frame-based mode). |
| start_time (st) | duration | `0` | Timestamp (seconds) at which the effect begins (time-based mode). |
| duration (d) | duration | `0` | Duration of the fade in seconds (time-based mode). Overrides `nb_frames` when set. |
| color (c) | color | `black` | The solid color to fade to/from (e.g., `black`, `white`, `#FF0000`). |
| alpha | bool | `0` | When `1`, fade only the alpha channel if present, not the RGB values. |

## Examples

### Fade in over the first second

Fade from black to the video starting at t=0 and lasting 1 second.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1" output.mp4
```

### Fade out the last 2 seconds

For a 30-second clip, start the fade-out at 28 seconds and let it run to the end.

```sh
ffmpeg -i input.mp4 -vf "fade=t=out:st=28:d=2" output.mp4
```

### Both fade-in and fade-out in one pass

Chain two `fade` filters to apply a 1-second fade-in at the start and a 1-second fade-out at the end of a 10-second clip.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=1,fade=t=out:st=9:d=1" output.mp4
```

### Fade in from white

Use `color=white` to create a bright flash intro effect instead of the default black.

```sh
ffmpeg -i input.mp4 -vf "fade=t=in:st=0:d=0.5:color=white" output.mp4
```

### Fade alpha channel only (for compositing)

When working in a pipeline that preserves alpha, fade only transparency without changing the underlying colors.

```sh
ffmpeg -i input.mp4 -vf "fade=t=out:st=5:d=1:alpha=1" output.mp4
```

## Notes

- If both `start_time`/`duration` and `start_frame`/`nb_frames` are set for the same fade, the time-based parameters take priority when `duration` is non-zero; otherwise frames are used.
- The fade effect applies to all frames that fall within the specified range; outside this range, the video passes through unchanged.
- When applying both fade-in and fade-out in a single `-vf`, chain them with a comma — the filters are applied in sequence.
- For very precise control at non-standard frame rates, prefer the time-based (`st`/`d`) parameters over the frame-count (`s`/`n`) ones.

---

### fieldorder

> Convert interlaced video between top-field-first (TFF) and bottom-field-first (BFF) field order.

**Source:** [libavfilter/vf_fieldorder.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_fieldorder.c)

The `fieldorder` filter changes the field dominance of interlaced video from top-field-first (TFF) to bottom-field-first (BFF) or vice versa. It shifts the picture content by one line and fills the gap with content from the adjacent field, consistent with broadcast field-order conversion. If the input is not interlaced, or is already in the requested field order, the filter passes the video through unchanged.

## Quick Start

```sh
# Convert to bottom-field-first (for DV output)
ffmpeg -i input.ts -vf "fieldorder=bff" output.dv
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| order | int | `tff` | Output field order: `tff` (top field first) or `bff` (bottom field first). |

## Examples

### Convert to bottom-field-first for DV

PAL DV requires bottom-field-first.

```sh
ffmpeg -i broadcast.ts -vf "fieldorder=bff" output.dv
```

### Convert to top-field-first for broadcast

```sh
ffmpeg -i dv_capture.dv -vf "fieldorder=tff" broadcast.ts
```

### Use in a deinterlace+re-interlace pipeline

```sh
ffmpeg -i input.ts -vf "yadif=1,fieldorder=tff" output.ts
```

## Notes

- `fieldorder` only affects interlaced content — progressive video is passed through without modification.
- The conversion works by shifting image content up or down by one line and filling the vacated line with neighboring field content.
- PAL DV format is bottom-field-first; most broadcast standards (DVB, ATSC) are top-field-first.
- Use `idet` to determine the existing field order before applying `fieldorder`.
- This filter sets the `tff` / `bff` flag in the output stream metadata in addition to physically rearranging the lines.

---

### format

> Convert the input video to one of the specified pixel formats, letting libavfilter select the best match for the downstream filter.

**Source:** [libavfilter/vf_format.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_format.c)

The `format` filter requests that libavfilter convert the input video to one of the listed pixel formats. If the input is already in one of the specified formats, it passes through unchanged. When multiple formats are listed (pipe-separated), libavfilter chooses the best match for the next filter in the chain. This is useful for ensuring an encoder or filter receives a format it supports, or for explicitly controlling color space and range metadata.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "format=pix_fmts=yuv420p" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pix_fmts | string | — | Pipe-separated list of pixel format names (e.g., `yuv420p\|nv12\|rgb24`). |
| color_spaces | string | — | Pipe-separated list of color space names (e.g., `bt709\|bt470bg`). |
| color_ranges | string | — | Pipe-separated list of color range names: `tv` (limited) or `pc` (full). |
| alpha_modes | string | — | Pipe-separated list of alpha modes: `straight` or `premultiplied`. |

## Examples

### Force yuv420p for H.264 encoding

Most H.264 encoders require `yuv420p`. Inserting `format` before the encoder ensures compatibility.

```sh
ffmpeg -i input.png -vf "format=pix_fmts=yuv420p" -c:v libx264 output.mp4
```

### Allow the filter to choose among several formats

Provide a preference list so libavfilter picks the best match for the next stage without a hard requirement.

```sh
ffmpeg -i input.mp4 -vf "format=pix_fmts=yuv420p|yuv444p|nv12" output.mp4
```

### Convert to full-range (PC) color

Override the color range metadata to signal full-range (0-255) levels.

```sh
ffmpeg -i input.mp4 -vf "format=color_ranges=pc" output.mp4
```

### Ensure straight (un-premultiplied) alpha

Normalize alpha mode for compositing filters that require straight alpha.

```sh
ffmpeg -i input.mov -vf "format=alpha_modes=straight" output.mov
```

## Notes

- The `format` filter only converts between pixel formats that libswscale supports. Conversions between very different color spaces may introduce visible quality loss.
- Specifying multiple formats in `pix_fmts` lets FFmpeg choose the most efficient conversion path; a single format forces an exact conversion.
- To explicitly tag color space/range metadata without pixel conversion, use `setparams` or encoder options instead.
- For removing an alpha channel, convert to a format without alpha (e.g., `yuv420p`) — the alpha data is discarded.

---

### fps

> Force a constant output frame rate by duplicating or dropping frames as needed.

**Source:** [libavfilter/vf_fps.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_fps.c)

The `fps` filter converts variable or mismatched frame rates to a specified constant frame rate. It achieves this by duplicating frames when the source rate is too low, and dropping frames when it is too high. This is commonly needed before encoding to a container that requires a fixed frame rate, or when you need to normalize frame rates before stacking or concatenating streams. The filter supports named rate constants such as `ntsc`, `pal`, and `film`.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "fps=fps=30" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | string | `25` | Desired output frame rate. Accepts a number, fraction (`30000/1001`), or named constant (`ntsc`, `pal`, `film`, `ntsc_film`). |
| start_time | double | (auto) | Assumed PTS of the first output frame in seconds. Useful for padding or trimming the stream start. |
| round | int | `near` | Timestamp rounding method: `zero`, `inf`, `down`, `up`, `near`. |
| eof_action | int | `round` | Behavior at end of input: `round` (apply normal rounding) or `pass` (pass last frame if duration not reached). |

### Named rate constants

| Constant | Value |
|----------|-------|
| `ntsc` | 30000/1001 (~29.97 fps) |
| `pal` | 25.0 fps |
| `film` | 24.0 fps |
| `ntsc_film` | 24000/1001 (~23.976 fps) |

## Examples

### Convert to 30 fps

Normalize any input to exactly 30 frames per second.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=30" output.mp4
```

### Convert to standard NTSC rate

Use the named constant for broadcast-safe NTSC frame rate.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=ntsc" output.mp4
```

### Convert to 24 fps film rate

Target a cinematic 24 fps output.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=film" output.mp4
```

### Pad stream start to time zero

Set `start_time=0` so that if the video stream begins after time zero, it is padded with duplicate frames from the first frame.

```sh
ffmpeg -i input.mp4 -vf "fps=fps=25:start_time=0" output.mp4
```

### Combine with setpts for slow motion

Double the frame rate together with stretched PTS to produce a smoother slow-motion effect via frame duplication.

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS,fps=fps=60" output.mp4
```

## Notes

- `fps` produces a constant frame rate by duplicating or dropping frames; it does not interpolate new frames. For true slow-motion with new frames, use the `minterpolate` filter.
- When combining `fps` with `setpts`, apply `setpts` first to stretch/compress time, then `fps` to normalize the rate.
- The filter works on PTS values; if the input has no reliable PTS, results may be unpredictable. Pair with `setpts=PTS-STARTPTS` to reset timestamps beforehand.
- Container-level frame rate (`-r`) and the `fps` filter are different mechanisms; using the filter gives more control in complex filtergraphs.

---

### framerate

> Change video frame rate by interpolating new frames from adjacent source frames, designed for progressive content.

**Source:** [libavfilter/vf_framerate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_framerate.c)

The `framerate` filter converts progressive video to a different frame rate by blending adjacent frames with configurable linear interpolation weights. Unlike `minterpolate`, it does not perform motion estimation — it simply cross-fades between frames, making it faster and more predictable. It detects scene changes to avoid blending across cuts. Designed exclusively for progressive content — deinterlace first if needed.

## Quick Start

```sh
# Convert 23.976fps to 25fps
ffmpeg -i film_24fps.mp4 -vf "framerate=fps=25" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | video_rate | `50` | Target output frame rate (e.g. `25`, `30000/1001`, `60`). |
| interp_start | int | `15` | Start of the blend range (0–255). Below this: copy source frame. |
| interp_end | int | `240` | End of the blend range. Above this: copy source frame. |
| scene | double | `8.2` | Scene change sensitivity (0–100). Higher = more scene changes detected. |
| flags | flags | `scd` | Flags: `scene_change_detect` / `scd` to enable scene change detection. |

## Examples

### 23.976fps to 25fps (PAL broadcast standard)

```sh
ffmpeg -i ntsc_film.mp4 -vf "framerate=fps=25" pal.mp4
```

### 25fps to 29.97fps (PAL to NTSC)

```sh
ffmpeg -i pal.mp4 -vf "framerate=fps=30000/1001" ntsc.mp4
```

### 60fps output without scene change detection

```sh
ffmpeg -i input.mp4 -vf "framerate=fps=60:flags=0" output.mp4
```

### Custom interpolation range

```sh
ffmpeg -i input.mp4 -vf "framerate=fps=50:interp_start=40:interp_end=200" output.mp4
```

## Notes

- `framerate` uses frame blending (cross-fade), not motion compensation. It is fast and artifact-free but can produce ghosting on fast motion.
- For more visually convincing interpolation at large fps multipliers (e.g. 24→60fps), use `minterpolate` instead.
- `framerate` is not designed for interlaced content — always deinterlace with `yadif` or `bwdif` first.
- Scene change detection (`scd` flag, enabled by default) prevents blending across hard cuts; disable it only if you experience false positives.
- `interp_start` and `interp_end` define a 0–255 range of blend amounts; frames at the boundaries of the conversion window get full copies of source frames.

---

### gblur

> Apply a Gaussian blur to video with configurable sigma and plane selection.

**Source:** [libavfilter/vf_gblur.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_gblur.c)

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

---

### geq

> Apply a generic equation to each pixel using mathematical expressions for creative and corrective effects.

**Source:** [libavfilter/vf_geq.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_geq.c)

The `geq` filter evaluates a mathematical expression for every pixel in the frame, allowing completely custom per-pixel transformations. Unlike `lut` (which operates on a single channel's value), `geq` expressions can reference neighbouring pixels, the current coordinates, frame timing, and samples from any channel — enabling effects like custom blurs, edge detection, coordinate warping, and procedural patterns.

## Quick Start

```sh
# Simple luma inversion
ffmpeg -i input.mp4 -vf "geq=lum='maxval-lum(X,Y)'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| lum_expr / lum | string | Expression for luma (Y). |
| cb_expr / cb | string | Expression for Cb (U/blue-difference chroma). |
| cr_expr / cr | string | Expression for Cr (V/red-difference chroma). |
| r_expr / r | string | Expression for red (RGB input). |
| g_expr / g | string | Expression for green. |
| b_expr / b | string | Expression for blue. |
| a_expr / a | string | Expression for alpha. |
| interpolation | int | Interpolation for pixel sample functions: `nearest` or `bilinear`. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `X` | Current pixel x-coordinate. |
| `Y` | Current pixel y-coordinate. |
| `W` | Frame width in pixels. |
| `H` | Frame height in pixels. |
| `N` | Frame number (0-based). |
| `T` | Timestamp in seconds. |
| `SW` | Component horizontal scale factor (1 for luma, 0.5 for Cb/Cr on YUV 4:2:0). |
| `SH` | Component vertical scale factor. |
| `lum(x, y)` | Luma sample at coordinate (x, y). |
| `cb(x, y)` | Cb sample at coordinate (x, y). |
| `cr(x, y)` | Cr sample at coordinate (x, y). |
| `r(x, y)` | Red sample at (x, y). |
| `g(x, y)` | Green sample at (x, y). |
| `b(x, y)` | Blue sample at (x, y). |
| `alpha(x, y)` | Alpha sample at (x, y). |
| `maxval` | Maximum value for this component's bit depth (255 for 8-bit). |
| `minval` | Minimum value. |
| `negval` | `maxval - val` |

## Examples

### Horizontal flip

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(W-1-X,Y)':cb='cb((W-1-X)*SW,Y*SH)':cr='cr((W-1-X)*SW,Y*SH)'" output.mp4
```

### Brighten the left half only

```sh
ffmpeg -i input.mp4 -vf "geq=lum='if(lt(X,W/2),min(lum(X,Y)*1.5,maxval),lum(X,Y))'" output.mp4
```

### Pixelation effect

Round X and Y to a grid to create a pixelated look.

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(floor(X/16)*16,floor(Y/16)*16)':cb='cb(floor(X/16)*16*SW,floor(Y/16)*16*SH)':cr='cr(floor(X/16)*16*SW,floor(Y/16)*16*SH)'" output.mp4
```

### Vignette using distance from center

```sh
ffmpeg -i input.mp4 -vf "geq=lum='lum(X,Y)*(1-hypot((X-W/2)/(W/2),(Y-H/2)/(H/2))*0.5)'" output.mp4
```

## Notes

- `geq` is evaluated per-pixel, per-frame, making it very flexible but relatively slow compared to dedicated filters. For simple LUT-style operations, use `lut`.
- The `p(x, y)` functions (or `lum(x,y)`, `r(x,y)`, etc.) allow accessing pixels at arbitrary coordinates, enabling convolution-style effects and warping.
- Expressions are parsed by the libavutil expression evaluator, which supports standard math functions: `sin`, `cos`, `sqrt`, `abs`, `min`, `max`, `gt`, `lt`, `eq`, `if`, `floor`, `ceil`, `hypot`, etc.
- For chroma planes on YUV 4:2:0 video, coordinates are scaled by `SW`/`SH` (0.5). Always multiply x by `SW` and y by `SH` when sampling chroma planes.

---

### haldclut

> Apply a Hald CLUT image to video as a 3D color lookup table.

**Source:** [libavfilter/vf_lut3d.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_lut3d.c)

The `haldclut` filter applies a Hald CLUT (Color Look-Up Table) — a special PNG image that encodes a 3D LUT — to video. It takes two inputs: the video to be graded and the Hald CLUT image. Hald CLUTs are generated by tools like G'MIC, GIMP, or online LUT editors and can be shared as standard PNG files, making them a portable alternative to `.cube` files.

## Quick Start

```sh
# Two inputs: video + Hald CLUT PNG
ffmpeg -i input.mp4 -i hald_clut.png -filter_complex "[0:v][1:v]haldclut" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| shortest | bool | `0` | End filtering when the shortest input ends. |
| repeatlast | bool | `1` | After the CLUT stream ends, repeat its last frame. |
| eof_action | int | `repeat` | Action when the CLUT stream reaches EOF: `repeat`, `endall`, `pass`. |

## Examples

### Apply a static Hald CLUT image

The most common usage: apply a single PNG as a color grade.

```sh
ffmpeg -i input.mp4 -i clut.png -filter_complex "[0:v][1:v]haldclut" output.mp4
```

### Apply a Hald CLUT from a looping GIF (animated LUT)

Using a GIF as the CLUT allows time-varying grades.

```sh
ffmpeg -i input.mp4 -i animated_clut.gif -filter_complex "[0:v][1:v]haldclut" output.mp4
```

### Combine with scale and output

```sh
ffmpeg -i input.mp4 -i grade.png \
  -filter_complex "[0:v][1:v]haldclut[graded]" \
  -map "[graded]" -c:v libx264 output.mp4
```

### Generate a Hald CLUT with G'MIC and apply it

```sh
# Step 1: generate identity CLUT and apply edits in G'MIC to produce grade.png
# Step 2: apply
ffmpeg -i input.mp4 -i grade.png -filter_complex "[0:v][1:v]haldclut" output.mp4
```

## Notes

- The Hald CLUT must be a square PNG image where its size determines the LUT precision: a 512×512 PNG encodes a 64³ LUT (cube size 64), which is high quality.
- The CLUT image is always the second input (`[1:v]`); the video to grade is the first input (`[0:v]`).
- For file-based `.cube`/`.3dl` LUTs, use `lut3d` instead — `haldclut` is specifically for image-based CLUTs.
- Hald CLUTs can be created from any image editor by starting with an identity CLUT and applying color adjustments, then saving the result.

---

### hflip

> Horizontally flip (mirror) each frame of the input video.

**Source:** [libavfilter/vf_hflip.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_hflip.c)

The `hflip` filter mirrors every frame of the input video along the vertical axis, producing a left-right reflection. It has no parameters and operates in-place without any quality loss. Common use cases include correcting footage shot with a mirror lens rig, fixing front-camera video captured on mobile devices, or creating stylistic mirror effects.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "hflip" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Basic horizontal flip

Mirror the video horizontally and re-encode with default settings.

```sh
ffmpeg -i input.mp4 -vf "hflip" output.mp4
```

### Flip and preserve audio

When only the video needs flipping, mux with the original audio stream without re-encoding it.

```sh
ffmpeg -i input.mp4 -vf "hflip" -c:a copy output.mp4
```

### Combine with vertical flip for 180-degree rotation

Apply both horizontal and vertical flips in a single pass to achieve a 180-degree rotation equivalent.

```sh
ffmpeg -i input.mp4 -vf "hflip,vflip" output.mp4
```

### Mirror comparison side-by-side

Use `hflip` in a filtergraph to show the original and its mirror image next to each other.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[a][b]; [b]hflip[bf]; [a][bf]hstack" \
  output.mp4
```

## Notes

- `hflip` performs a purely spatial transformation with no resampling, so there is no quality degradation from the flip itself.
- The filter does not alter timestamps, audio, or any metadata.
- To rotate 90 or 270 degrees, use `transpose` instead; for an arbitrary angle, use `rotate`.
- When combined with `vflip`, the result is equivalent to a 180-degree rotation.

---

### histogram

> Compute and display a color histogram showing the distribution of pixel values for each color component.

**Source:** [libavfilter/vf_histogram.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_histogram.c)

The `histogram` filter renders a real-time color histogram for each frame, showing how pixel values are distributed across the 0–255 range for each color component. This is useful for exposure checking, detecting clipping or crushing, and verifying color balance. It supports stacked, parade, and overlay display modes, and linear or logarithmic scaling.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "histogram" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| display_mode / d | int | `stack` | Layout: `stack` (components below each other), `parade` (side by side), `overlay` (superimposed). |
| levels_mode / m | int | `linear` | Scale mode: `linear` or `logarithmic`. |
| components / c | int | `7` | Bitmask of components to display (1=Y/R, 2=U/G, 4=V/B, 7=all three). |
| level_height | int | `200` | Height of each histogram graph. Range: 50–2048. |
| scale_height | int | `12` | Height of the color scale below each graph. Range: 0–40. |
| fgopacity / f | float | `0.7` | Foreground (bars) opacity. |
| bgopacity / b | float | `0.5` | Background opacity. |
| colors_mode / l | int | `whiteonblack` | Color scheme: `whiteonblack`, `coloronblack`, `colorongray`, etc. |
| envelope / e | bool | `0` | Show peak envelope overlay. |
| ecolor / ec | color | `gold` | Color of the envelope. |

## Examples

### Basic histogram

```sh
ffmpeg -i input.mp4 -vf "histogram" output.mp4
```

### Parade mode (R/G/B side by side)

```sh
ffmpeg -i input.mp4 -vf "histogram=display_mode=parade:components=7" output.mp4
```

### Logarithmic scale for dark-heavy footage

```sh
ffmpeg -i night.mp4 -vf "histogram=levels_mode=logarithmic" output.mp4
```

### Show only luma channel

```sh
ffmpeg -i input.mp4 -vf "histogram=components=1" output.mp4
```

### Histogram beside original video

```sh
ffmpeg -i input.mp4 -vf "split[a][b];[a]histogram[h];[b][h]hstack" output.mp4
```

## Notes

- `stack` mode places component histograms vertically; `parade` places them side by side for easy comparison; `overlay` superimposes all components for compact display.
- `logarithmic` mode is useful for footage with many dark or near-black pixels (e.g. night scenes) where the linear scale makes highlights invisible.
- `components=7` shows all three components; use bitmask to select specific planes (e.g. `1` for Y-only in YUV, `7` for R+G+B).
- For broadcast monitoring, use `histogram` alongside `waveform` (for precise level checking) and `vectorscope` (for chroma/hue).

---

### hqdn3d

> Apply a High Quality 3D Denoiser combining spatial and temporal filtering.

**Source:** [libavfilter/vf_hqdn3d.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_hqdn3d.c)

The `hqdn3d` filter applies a 3D denoiser that combines spatial (within-frame) and temporal (across-frame) lowpass filtering. It is one of the fastest high-quality denoisers in FFmpeg, making it suitable for real-time or near-real-time workflows. The spatial component blurs within each frame; the temporal component averages across consecutive frames to suppress flickering noise.

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "hqdn3d=4:3:6:4.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_spatial | double | `4.0` | Spatial luma denoising strength. Higher = more smoothing. |
| chroma_spatial | double | `3.0` | Spatial chroma denoising strength. |
| luma_tmp | double | `6.0` | Temporal luma strength. Higher = stronger frame-to-frame averaging. |
| chroma_tmp | double | `4.5` | Temporal chroma strength. |

## Examples

### Moderate denoising (default values)

```sh
ffmpeg -i noisy.mp4 -vf "hqdn3d" output.mp4
```

### Aggressive denoising

```sh
ffmpeg -i very_noisy.mp4 -vf "hqdn3d=8:6:12:9" output.mp4
```

### Temporal only (no spatial blur)

Reduce temporal flickering without blurring spatial detail.

```sh
ffmpeg -i input.mp4 -vf "hqdn3d=0:0:6:4" output.mp4
```

### Chroma-only denoising

Denoise only colour channels, leave luma sharp.

```sh
ffmpeg -i input.mp4 -vf "hqdn3d=0:3:0:4" output.mp4
```

## Notes

- The four parameters are positional: `luma_spatial:chroma_spatial:luma_tmp:chroma_tmp`. If only the first is given, it sets `luma_spatial`; if the second is omitted, it defaults to `luma_spatial * 2/3`.
- Temporal strength (`luma_tmp`) often matters more than spatial — start by increasing `luma_tmp` before `luma_spatial`.
- `hqdn3d` is much faster than `nlmeans` but produces more detail loss at high strengths. It is excellent for pre-processing before encoding to improve compression efficiency.
- High values on fast-moving content can cause ghost/smear artifacts in the temporal dimension; reduce `luma_tmp` in those cases.

---

### hstack

> Stack two or more video inputs side by side horizontally into a single output frame.

**Source:** [libavfilter/vf_stack.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_stack.c)

The `hstack` filter places multiple video streams side by side in a single row, producing a wider output frame. All input streams must share the same pixel format and the same height. It is faster than achieving the same result with `overlay` and `pad`, making it the preferred choice for side-by-side video comparisons, dual-camera layouts, and horizontal strip compositions.

## Quick Start

```sh
ffmpeg -i left.mp4 -i right.mp4 -filter_complex "hstack" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams to stack horizontally. |
| shortest | bool | `0` | When `1`, stop output when the shortest input ends. |

## Examples

### Side-by-side comparison of two videos

Place two videos of the same height next to each other for a direct comparison.

```sh
ffmpeg -i original.mp4 -i processed.mp4 \
  -filter_complex "hstack" comparison.mp4
```

### Normalize heights before stacking

Scale both inputs to the same height before stacking if they differ.

```sh
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v]scale=-1:480[l]; [1:v]scale=-1:480[r]; [l][r]hstack" \
  output.mp4
```

### Stack three inputs horizontally

Specify `inputs=3` to stack three streams in a row.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]hstack=inputs=3" \
  output.mp4
```

### Stop when the shorter stream ends

Use `shortest=1` to cut off the output when the first input finishes.

```sh
ffmpeg -i long.mp4 -i short.mp4 \
  -filter_complex "hstack=shortest=1" \
  output.mp4
```

## Notes

- All input streams must have the same height and the same pixel format. Use `scale` and `format` filters to normalize before stacking.
- The output width is the sum of all input widths; the output height equals the shared input height.
- For more than two inputs arranged in a custom grid, use `xstack` instead.
- `hstack` is faster than using `pad` + `overlay` to create the same layout because it does not require compositing.

---

### hue

> Adjust the hue angle and saturation of the input video, with optional brightness control and per-frame expression support.

**Source:** [libavfilter/vf_hue.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_hue.c)

The `hue` filter modifies the hue rotation and saturation of a video in the YCbCr color space, operating on the chroma channels while leaving luma (brightness) largely intact. The hue angle can be specified in degrees (`h`) or radians (`H`), and all parameters accept per-frame expressions, enabling animated color effects like cycling hues or time-based saturation fades. A brightness adjustment (`b`) is also available for simple luma tweaks.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "hue=h=30:s=1.2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| h | string (expr) | `0` | Hue rotation angle in degrees. Accepts expressions. Mutually exclusive with `H`. |
| H | string (expr) | `0` | Hue rotation angle in radians. Mutually exclusive with `h`. |
| s | string (expr) | `1` | Saturation multiplier. Range: [-10, 10]. `0` = grayscale, `1` = original, `>1` = more saturated. |
| b | string (expr) | `0` | Brightness adjustment. Range: [-10, 10]. `0` = no change. |

### Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Frame count of the input frame, starting from 0 |
| `pts` | Presentation timestamp in timebase units |
| `r` | Input frame rate |
| `t` | Timestamp in seconds |
| `tb` | Input video timebase |

## Examples

### Rotate hue by 90 degrees (green to cyan-blue shift)

Shift the color wheel by 90 degrees for a stylistic color transformation.

```sh
ffmpeg -i input.mp4 -vf "hue=h=90" output.mp4
```

### Convert to grayscale

Set saturation to 0 to remove all color information.

```sh
ffmpeg -i input.mp4 -vf "hue=s=0" output.mp4
```

### Boost saturation for vivid colors

Increase saturation to make colors more vivid and punchy.

```sh
ffmpeg -i input.mp4 -vf "hue=s=1.5" output.mp4
```

### Animated rainbow hue cycling

Rotate the hue continuously over time for a psychedelic color-cycling effect.

```sh
ffmpeg -i input.mp4 -vf "hue=H='2*PI*t/10'" output.mp4
```

### Saturation fade-in over 3 seconds

Animate from grayscale to full color over the first 3 seconds.

```sh
ffmpeg -i input.mp4 -vf "hue=s='min(t/3,1)'" output.mp4
```

## Notes

- `h` and `H` are mutually exclusive — specifying both causes an error. Use `h` for degrees (more intuitive) or `H` for radians.
- The saturation range is [-10, 10], but values below 0 invert the colors while also desaturating; typically keep `s` between 0 and 2 for natural looks.
- `hue` operates on the YCbCr Cb and Cr channels, so it does not affect the luma (brightness) of the image when only `h` or `s` are changed.
- The filter supports runtime commands for `h`, `H`, `s`, and `b`, enabling live parameter adjustment during streaming.

---

### huesaturation

> Apply hue, saturation, and intensity adjustments to specific color ranges in a video.

**Source:** [libavfilter/vf_huesaturation.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_huesaturation.c)

The `huesaturation` filter adjusts hue, saturation, and intensity of video, with optional filtering to target specific color ranges. Unlike the simpler `hue` filter, it allows selective adjustments — for example, shifting only skin tones (reds) or making greens more vibrant without affecting blues. It is closer to the HSL Hue Saturation panel in Lightroom or Photoshop.

## Quick Start

```sh
# Shift all hues +30° and boost saturation
ffmpeg -i input.mp4 -vf "huesaturation=hue=30:saturation=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hue | float | `0.0` | Hue shift in degrees. Range: -180–180. |
| saturation | float | `0.0` | Saturation adjustment. Range: -3–3. Positive=more saturated, negative=less. |
| intensity | float | `0.0` | Intensity (luminance) shift. Range: -1–1. |
| colors | flags | `all` | Target color range: `r` (reds), `y` (yellows), `g` (greens), `c` (cyans), `b` (blues), `m` (magentas), `a` (all). Combine: `r+y`. |
| strength | float | `1.0` | Filtering strength for selective color mode. Range: 0–1. |
| rw | float | `0.333` | Red weight for luminance calculation. |
| gw | float | `0.334` | Green weight for luminance calculation. |
| bw | float | `0.333` | Blue weight for luminance calculation. |

## Examples

### Boost overall saturation

```sh
ffmpeg -i input.mp4 -vf "huesaturation=saturation=1.5" output.mp4
```

### Shift only reds (skin tones and warm colours)

```sh
ffmpeg -i portrait.mp4 -vf "huesaturation=hue=10:colors=r:strength=0.8" output.mp4
```

### Desaturate greens for forest footage

```sh
ffmpeg -i forest.mp4 -vf "huesaturation=saturation=-1:colors=g" output.mp4
```

### Convert to warm golden hour tone

Shift yellows toward orange and lift intensity slightly.

```sh
ffmpeg -i input.mp4 -vf "huesaturation=hue=-15:saturation=0.5:intensity=0.1:colors=y+r" output.mp4
```

## Notes

- `hue` shifts the entire hue wheel; `colors` limits the effect to specific segments of the wheel.
- `saturation` range is -3 to 3; values of -2 or below approach grayscale; above 2 produces heavily oversaturated output.
- `strength` controls how narrowly the color range filter targets. High strength (1.0) = only target colors affected; low strength = broader effect with more bleed.
- For a full desaturation (grayscale), set `saturation=-3` or use `monochrome` for more control over the conversion tone.

---

### idet

> Detect whether video is interlaced or progressive, and identify field order (top-first or bottom-first) and repeated fields.

**Source:** [libavfilter/vf_idet.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_idet.c)

The `idet` filter analyzes video frames and reports whether the content is interlaced (top-field-first or bottom-field-first), progressive, or contains repeated fields (a sign of telecine). It outputs frame classification metadata and cumulative statistics, making it useful for quality control and automated pipeline decisions about whether to apply deinterlacing.

## Quick Start

```sh
# Analyze interlacing and print statistics to stderr
ffmpeg -i input.mp4 -vf "idet" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| intl_thres | float | `1.04` | Threshold for classifying a frame as interlaced. |
| prog_thres | float | `1.5` | Threshold for classifying a frame as progressive. |
| rep_thres | float | `3.0` | Threshold for detecting repeated fields (telecine). |
| half_life | float | `0` | Frames after which a past frame's contribution is halved. 0 = all frames have equal weight. |
| analyze_interlaced_flag | int | `0` | Frames to analyze to verify the interlaced flag accuracy. |

## Examples

### Detect interlacing and print results

```sh
ffmpeg -i input.ts -vf "idet" -f null - 2>&1 | tail -5
```

### Use idet to clean up incorrect interlaced flags

```sh
ffmpeg -i input.mp4 -vf "idet=analyze_interlaced_flag=20" -f null -
```

### Pipe idet results for scripting

```sh
ffmpeg -i input.mp4 -vf "idet" -f null - 2>&1 | grep "Multi frame detection"
```

### Conditional deinterlace pipeline

```sh
# First check, then apply yadif if interlaced
ffmpeg -i input.ts -vf "idet,yadif=mode=0:deint=interlaced" output.mp4
```

## Notes

- `idet` logs per-frame metadata (`lavfi.idet.single.*` and `lavfi.idet.multiple.*`) and prints cumulative statistics at end-of-stream.
- Single-frame detection classifies each frame independently; multiple-frame detection incorporates history for more stable results.
- `half_life=0` means all frames are weighted equally forever; set a small value (e.g. 1 second worth of frames) for a sliding-window view.
- When `analyze_interlaced_flag > 0`, `idet` verifies whether the stream's built-in interlaced flag is accurate; if inaccurate, it is cleared.
- Chain with `yadif=deint=interlaced` to deinterlace only the frames idet identifies as interlaced.

---

### lenscorrection

> Correct barrel or pincushion lens distortion using radial correction coefficients.

**Source:** [libavfilter/vf_lenscorrection.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_lenscorrection.c)

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

---

### lut

> Apply a per-pixel lookup table transformation using mathematical expressions per channel.

**Source:** [libavfilter/vf_lut.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_lut.c)

The `lut` filter applies a mathematical expression to every pixel of each channel independently, computed once and stored in a lookup table (LUT) for fast evaluation. It supports both YCbCr (`y`, `u`, `v`) and RGB (`r`, `g`, `b`, `a`) addressing, making it suitable for channel inversions, gamma corrections, clamping, and simple color grading effects.

## Quick Start

```sh
# Boost luminance by 20%
ffmpeg -i input.mp4 -vf "lut=y='val*1.2'" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| c0 | string | Expression for component 0 (Y or R depending on pixel format). |
| c1 | string | Expression for component 1 (Cb/U or G). |
| c2 | string | Expression for component 2 (Cr/V or B). |
| c3 | string | Expression for component 3 (alpha). |
| y | string | Luminance (Y) expression — alias for c0 on YUV input. |
| u | string | Cb/U expression — alias for c1. |
| v | string | Cr/V expression — alias for c2. |
| r | string | Red expression — alias for c0 on RGB input. |
| g | string | Green expression — alias for c1. |
| b | string | Blue expression — alias for c2. |
| a | string | Alpha expression — alias for c3. |

### Expression variables

Within each expression, the following variables are available:

| Variable | Description |
|----------|-------------|
| `val` | Current input pixel value. |
| `maxval` | Maximum value for the component's bit depth (e.g. 255 for 8-bit). |
| `minval` | Minimum value (typically 0). |
| `negval` | `maxval - val` (inverted value). |
| `clipval` | `val` clamped to `[minval, maxval]`. |
| `w` / `h` | Video width / height. |
| `n` | Frame number (0-based). |
| `t` | Timestamp in seconds. |

## Examples

### Invert the luma channel (negative)

```sh
ffmpeg -i input.mp4 -vf "lut=y='negval'" output.mp4
```

### Increase luminance with clipping

```sh
ffmpeg -i input.mp4 -vf "lut=y='min(val*1.3, maxval)'" output.mp4
```

### Desaturate by zeroing chroma

```sh
ffmpeg -i input.mp4 -vf "lut=u='128':v='128'" output.mp4
```

### Increase red and reduce blue (RGB input)

Requires the input to be in RGB format (use `format=rgb24` first).

```sh
ffmpeg -i input.mp4 -vf "format=rgb24,lut=r='min(val*1.2, maxval)':b='val*0.8'" output.mp4
```

## Notes

- `lut` works on individual channels; for 3D color interactions (where R affects G output, etc.), use `lut3d` or `colorchannelmixer`.
- The expression is evaluated once per unique input value at filter initialisation, not per pixel, so it is very fast even on high-resolution video.
- For YUV inputs, chroma values range from 0–255 with neutral at 128. Setting `u` or `v` to `'128'` removes all chroma (desaturates).
- `lutyuv` is an alias for `lut` on YUV inputs; `lutrgb` is an alias for RGB inputs — both are equivalent to `lut`.

---

### lut3d

> Apply a 3D color LUT from a file to adjust colors with full three-dimensional color mapping.

**Source:** [libavfilter/vf_lut3d.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_lut3d.c)

The `lut3d` filter loads a 3D Look-Up Table from an external file and applies it to video. Unlike 1D per-channel LUTs, a 3D LUT maps every possible RGB combination to a new color, allowing complex non-linear color transformations that cannot be expressed per-channel. It supports industry-standard formats including `.cube`, `.3dl`, `.dat`, and `.m3d`.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube" output.mp4
```

## Parameters

| Name | Type | Description |
|------|------|-------------|
| file | string | Path to the 3D LUT file. Supported formats: `.cube` (Adobe), `.3dl` (Autodesk), `.dat`, `.m3d` (Pandora), `.csp` (cineSpace). |
| interp | int | Interpolation method: `nearest` (no interpolation), `trilinear` (default, good quality), `tetrahedral` (highest quality). |

## Examples

### Apply a .cube LUT for cinematic grading

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=film_look.cube" output.mp4
```

### Use tetrahedral interpolation for best quality

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube:interp=tetrahedral" output.mp4
```

### Apply LUT and re-encode with libx264

```sh
ffmpeg -i input.mp4 -vf "lut3d=file=grade.cube" -c:v libx264 -crf 18 output.mp4
```

### Chain with colorspace conversion

Convert from Rec.709 to log-C before applying a log-to-display LUT.

```sh
ffmpeg -i input.mp4 -vf "colorspace=all=bt709,lut3d=file=logc_to_display.cube" output.mp4
```

## Notes

- `.cube` files from tools like DaVinci Resolve, Adobe Premiere, or online LUT collections work directly with this filter.
- Tetrahedral interpolation provides the most accurate results and is preferred for final grading, while trilinear is a good default for previews.
- For Hald CLUT images (PNG-based LUTs) instead of file-based LUTs, use the `haldclut` filter.
- 3D LUTs operate in linear RGB space; if your footage uses a log or gamma curve, convert to linear first with `colorspace` or `lut`.

---

### median

> Apply a median filter to remove salt-and-pepper noise by replacing each pixel with the median value from its neighborhood.

**Source:** [libavfilter/vf_median.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_median.c)

The `median` filter replaces each pixel with the median value from a rectangular neighborhood, making it highly effective at removing impulse noise (salt-and-pepper noise) while preserving edges better than a Gaussian blur. The `percentile` option generalizes the filter — set it below 0.5 for an erosion-like effect (pick minimum) or above 0.5 for dilation (pick maximum).

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "median=radius=2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| radius | int | `1` | Horizontal radius. Range: 1–127. Window width = 2*radius+1. |
| radiusV | int | `0` | Vertical radius. Range: 0–127. If 0, uses horizontal radius. |
| percentile | float | `0.5` | Percentile to select (0=min, 0.5=median, 1=max). |
| planes | int | `15` | Bitmask of planes to filter (15 = all). |

## Examples

### Remove salt-and-pepper noise

```sh
ffmpeg -i noisy.mp4 -vf "median=radius=1" output.mp4
```

### Stronger denoising with radius 3

```sh
ffmpeg -i input.mp4 -vf "median=radius=3" output.mp4
```

### Asymmetric window (wide horizontal, narrow vertical)

```sh
ffmpeg -i input.mp4 -vf "median=radius=3:radiusV=1" output.mp4
```

### Dilation effect (select maximum)

```sh
ffmpeg -i input.mp4 -vf "median=radius=2:percentile=1.0" output.mp4
```

### Filter only luma plane

```sh
ffmpeg -i input.mp4 -vf "median=radius=2:planes=1" output.mp4
```

## Notes

- `median` is ideal for removing isolated pixel noise (dust, scan artifacts) because the median is resistant to outliers.
- Larger radius = stronger filtering but slower processing and more blurring.
- `percentile=0.5` is true median; `percentile=0` picks minimum (erosion); `percentile=1` picks maximum (dilation).
- For temporal noise (noise that changes frame to frame), `atadenoise` or `hqdn3d` are more effective.

---

### mergeplanes

> Merge individual color plane streams from multiple inputs into a single multi-component video stream.

**Source:** [libavfilter/vf_mergeplanes.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_mergeplanes.c)

The `mergeplanes` filter combines individual plane streams from up to 4 input streams into a single output pixel format. The `mapping` parameter is a hexadecimal bitmap specifying which input stream and plane feeds each output plane. It is the counterpart to `extractplanes`, and together they enable processing individual color components with arbitrary filter chains.

## Quick Start

```sh
# Merge 3 gray streams into yuv444p
ffmpeg -i y.mp4 -i u.mp4 -i v.mp4 \
  -filter_complex '[0][1][2]mergeplanes=0x001020:yuv444p' output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mapping | int | `0` | Hex bitmap: `0xAaBbCcDd`. Each byte: high nibble = input stream (0–3), low nibble = source plane (0–3). |
| format | pixel_fmt | `yuva444p` | Output pixel format. |
| map0s / map0p | int | `0` | Stream/plane mapping for output plane 0 (alternative to `mapping`). |
| map1s / map1p | int | `0` | Stream/plane mapping for output plane 1. |
| map2s / map2p | int | `0` | Stream/plane mapping for output plane 2. |
| map3s / map3p | int | `0` | Stream/plane mapping for output plane 3. |

## Examples

### Merge 3 gray streams into YUV444

```sh
ffmpeg -i y.mp4 -i u.mp4 -i v.mp4 \
  -filter_complex '[0][1][2]mergeplanes=0x001020:yuv444p' out.mp4
```

### Swap U and V planes in yuv420p

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'format=yuv420p,mergeplanes=0x000201:yuv420p' swapped.mp4
```

### Swap Y and Alpha in yuva444p

```sh
ffmpeg -i input.mov \
  -filter_complex 'format=yuva444p,mergeplanes=0x03010200:yuva444p' output.mov
```

### Cast RGB24 to YUV444 (plane reinterpretation, no color conversion)

```sh
ffmpeg -i input.mp4 \
  -filter_complex 'format=rgb24,mergeplanes=0x000102:yuv444p' output.mp4
```

### Merge Y from stream 0, U/V from stream 1

```sh
ffmpeg -i sharpened_luma.mp4 -i original.mp4 \
  -filter_complex '[0][1]mergeplanes=0x001011:yuv444p' out.mp4
```

## Notes

- The `mapping` hex value encodes all plane sources at once: `0xAaBbCcDd` where `A`=stream for output plane 0, `a`=plane from that stream, etc.
- The alternative `map0s`/`map0p` … `map3s`/`map3p` parameters are easier to read for complex mappings.
- Inputs must all be the same width and height; pixel formats need not match.
- `mergeplanes` is commonly used after `extractplanes` to recombine independently processed planes.

---

### minterpolate

> Convert video to a higher or lower frame rate using motion-compensated interpolation to synthesize intermediate frames.

**Source:** [libavfilter/vf_minterpolate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_minterpolate.c)

The `minterpolate` filter converts video to a target frame rate by synthesizing intermediate frames using motion estimation and compensation — the "motion smoothing" effect seen on modern TVs (sometimes called the "soap opera effect"). It supports multiple motion estimation algorithms and can degrade gracefully at scene changes by detecting them automatically.

## Quick Start

```sh
# Convert 24fps to 60fps with motion interpolation
ffmpeg -i input.mp4 -vf "minterpolate=fps=60" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fps | video_rate | `60` | Target output frame rate. Frames are dropped if fps < source fps. |
| mi_mode | int | `mci` | Motion interpolation mode: `dup` (duplicate), `blend` (blend frames), `mci` (motion-compensated). |
| mc_mode | int | `obmc` | Motion compensation mode: `obmc` (overlapped block) or `aobmc` (adaptive). Requires `mci`. |
| me_mode | int | `bilat` | Motion estimation mode: `bidir` (bidirectional) or `bilat` (bilateral). |
| me | int | `epzs` | ME algorithm: `esa`, `tss`, `tdls`, `ntss`, `fss`, `ds`, `hexbs`, `epzs`, `umh`. |
| mb_size | int | `16` | Macroblock size in pixels. |
| search_param | int | `32` | Search parameter for motion estimation. |
| vsbmc | int | `0` | Enable variable-size block motion compensation at object boundaries. |
| scd | int | `fdiff` | Scene change detection: `none` or `fdiff` (frame difference). |
| scd_threshold | double | `10.0` | Scene change detection threshold. |

## Examples

### Convert 24fps film to 60fps (smooth motion)

```sh
ffmpeg -i film_24fps.mp4 -vf "minterpolate=fps=60:mi_mode=mci" output.mp4
```

### Simple frame blending (less artifacts, less smoothness)

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:mi_mode=blend" output.mp4
```

### Slow motion: 120fps target from 30fps source

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=120:mi_mode=mci:mc_mode=aobmc" slow.mp4
```

### Disable scene change detection

```sh
ffmpeg -i input.mp4 -vf "minterpolate=fps=60:scd=none" output.mp4
```

## Notes

- `mci` (motion-compensated) mode produces the smoothest results but is computationally expensive.
- `blend` mode is fast and artifact-free but only produces a smooth crossfade between frames, not true motion interpolation.
- Scene change detection (`scd`) prevents motion vectors from crossing cuts — disable if you experience false positives with `scd=none`.
- For broadcast standards conversion (e.g. 23.976→25fps), the simpler `framerate` filter is usually preferred as it produces fewer artifacts.
- Very fast motion (action scenes, sports) will produce ghosting/warping artifacts with any interpolation method.

---

### monochrome

> Convert video to grayscale using a custom color filter for stylized black-and-white output.

**Source:** [libavfilter/vf_monochrome.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_monochrome.c)

The `monochrome` filter converts color video to stylized black-and-white by allowing you to specify the chroma channel contributions to the final luminance. This is analogous to using a colored filter in front of a black-and-white film camera: a red filter makes reds lighter and blues darker. It produces more expressive monochrome conversions than a simple desaturation.

## Quick Start

```sh
# Classic B&W with slight red-channel boost
ffmpeg -i input.mp4 -vf "monochrome=cb=-0.1:cr=0.3" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cb | float | `0.0` | Chroma blue (Cb) contribution to luminance. Range: -1–1. Negative = blue tones darker. |
| cr | float | `0.0` | Chroma red (Cr) contribution to luminance. Range: -1–1. Positive = red/warm tones lighter. |
| size | float | `1.0` | Color filter size, controlling the width of the chroma sensitivity. Range: 0–1. |
| high | float | `0.0` | Highlights sensitivity adjustment. Range: 0–1. |

## Examples

### Neutral desaturation (no chroma bias)

```sh
ffmpeg -i input.mp4 -vf "monochrome" output.mp4
```

### Red filter effect (landscapes, dramatic skies)

Makes blues darker and reds lighter — classic for sky drama and foliage.

```sh
ffmpeg -i landscape.mp4 -vf "monochrome=cr=0.5:cb=-0.3" output.mp4
```

### Green filter (portraits, skin tones)

Brightens skin tones and foliage.

```sh
ffmpeg -i portrait.mp4 -vf "monochrome=cr=-0.2:cb=-0.1" output.mp4
```

### Blue filter effect (high-contrast, dark skies)

```sh
ffmpeg -i input.mp4 -vf "monochrome=cb=0.5:cr=-0.3" output.mp4
```

## Notes

- `cr > 0` brightens warm/red tones and darkens cool/blue tones, similar to an orange or red filter on a film camera.
- `cb > 0` brightens blues; `cb < 0` darkens blues (simulating a red filter's effect on blue sky).
- For a purely flat desaturation, use `huesaturation=saturation=-3` or `colorchannelmixer` to average channels equally.
- `size` affects how broadly or narrowly the color filter sensitivity is applied. Default 1.0 is full-width.

---

### mpdecimate

> Drop near-duplicate frames to reduce frame rate, useful for very low-bitrate encoding or fixing inverse-telecine artifacts.

**Source:** [libavfilter/vf_mpdecimate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_mpdecimate.c)

The `mpdecimate` filter removes frames that are nearly identical to the previous frame, reducing the effective frame rate without re-encoding. Its primary use is for extremely low-bitrate streaming, but it also helps fix incorrectly inverse-telecined video (where duplicate fields create judder). The `hi`/`lo`/`frac` thresholds control how similar a frame must be to be considered a duplicate.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "mpdecimate" -vsync vfr output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| max | int | `0` | Max consecutive dropped frames (positive) or min interval between drops (negative). 0 = no limit. |
| keep | int | `0` | Max consecutive similar frames to keep before dropping. 0 = drop immediately. |
| hi | int | `768` (64×12) | High threshold per 8×8 block (pixel difference). |
| lo | int | `320` (64×5) | Low threshold per 8×8 block. |
| frac | float | `0.33` | Maximum fraction of blocks that may differ by more than `lo` (1.0 = whole image). |

## Examples

### Basic duplicate frame removal

```sh
ffmpeg -i input.mp4 -vf "mpdecimate" -vsync vfr output.mp4
```

### Limit to at most 2 consecutive dropped frames

```sh
ffmpeg -i input.mp4 -vf "mpdecimate=max=2" -vsync vfr output.mp4
```

### Strict deduplication (only exact duplicates)

```sh
ffmpeg -i input.mp4 -vf "mpdecimate=hi=64:lo=64:frac=0.1" -vsync vfr output.mp4
```

### Loose deduplication (drop near-duplicates aggressively)

```sh
ffmpeg -i talking_head.mp4 -vf "mpdecimate=hi=1024:lo=512:frac=0.5" -vsync vfr output.mp4
```

## Notes

- Always use `-vsync vfr` (or `-fps_mode vfr`) when outputting to a container to preserve correct timestamps after frame drops.
- A frame is dropped if no 8×8 block differs by more than `hi`, AND no more than `frac` of blocks differ by more than `lo`.
- Values for `hi` and `lo` represent pixel difference per 8×8 block: 64 = 1 unit per pixel on average within the block.
- `mpdecimate` is commonly used to detect and remove the duplicate frames left by a bad 3:2 pulldown telecine conversion.

---

### negate

> Invert the colors of a video by negating each pixel's component values.

**Source:** [libavfilter/vf_negate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_negate.c)

The `negate` filter inverts the color of each pixel by subtracting each component value from the maximum value (`maxval - val`). Applied to all channels it produces a photographic negative. Individual channels can be selectively negated using the `components` parameter, enabling effects like luma inversion while preserving hue.

## Quick Start

```sh
# Full colour inversion (photographic negative)
ffmpeg -i input.mp4 -vf "negate" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| components | flags | `7` | Bitmask of components to negate: 1=Y/R, 2=Cb/U/G, 4=Cr/V/B, 8=Alpha. Default 7 negates Y, Cb, Cr (all chroma, full inversion). |

## Examples

### Full colour inversion

```sh
ffmpeg -i input.mp4 -vf "negate" output.mp4
```

### Invert only luminance (solarize-like effect)

Negate only the Y channel to produce a light-on-dark effect with original hues.

```sh
ffmpeg -i input.mp4 -vf "negate=components=1" output.mp4
```

### Invert luma and alpha (for overlay effects)

```sh
ffmpeg -i input.mp4 -vf "negate=components=9" output.mp4
```

## Notes

- With no arguments, `negate` inverts all three colour planes (Y, Cb, Cr for YUV or R, G, B for RGB), producing a traditional photographic negative.
- The `components` bitmask uses: 1=first plane (Y/R), 2=second plane (Cb/U/G), 4=third plane (Cr/V/B), 8=alpha. Sum the values to combine, e.g. `components=5` negates Y and Cr.
- Negation is equivalent to `lut=y='negval'` but faster and more readable.
- On YUV input, negating only chroma (components=6) produces a complementary colour-shifted image with unchanged brightness.

---

### nlmeans

> Denoise video using the Non-Local Means algorithm for high-quality noise reduction.

**Source:** [libavfilter/vf_nlmeans.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_nlmeans.c)

The `nlmeans` filter applies Non-Local Means denoising, a high-quality algorithm that compares small patches across the entire frame to identify similar regions and averages them to suppress noise. It produces excellent results, preserving fine detail and textures that simpler blur-based denoisers destroy. The trade-off is computational cost: it is significantly slower than `hqdn3d` or `atadenoise`.

## Quick Start

```sh
ffmpeg -i noisy.mp4 -vf "nlmeans=s=4:p=7:r=15" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | double | `1.0` | Denoising strength. Higher = stronger denoising, less detail. Typical range: 1–10. |
| p | int | `7` | Patch size (side length in pixels). Must be odd. Range: 1–99. |
| pc | int | `0` | Patch size for chroma planes. 0 = use `p`. |
| r | int | `15` | Research window size (side length). Must be odd. Larger = better quality, much slower. |
| rc | int | `0` | Research window for chroma. 0 = use `r`. |

## Examples

### Moderate denoising

Good for slightly noisy footage — preserves detail while smoothing grain.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=3:p=7:r=15" output.mp4
```

### Aggressive denoising for very grainy footage

```sh
ffmpeg -i grainy.mp4 -vf "nlmeans=s=8:p=7:r=21" output.mp4
```

### Denoise luma more than chroma

Chroma noise is often less visible; using smaller patch/search for chroma is faster.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=4:p=7:r=15:pc=3:rc=9" output.mp4
```

### Fast preview mode (small search window)

Reduce `r` to speed up processing at the cost of quality.

```sh
ffmpeg -i input.mp4 -vf "nlmeans=s=4:p=5:r=9" output.mp4
```

## Notes

- `s` is the primary quality knob: start at 3–4 for moderate noise and increase by 2 until noise is acceptable. Values above 8 tend to over-smooth fine textures.
- Computational cost scales with `r²`: doubling the research window quadruples processing time. The default `r=15` is a good balance.
- `nlmeans` is better than `hqdn3d` at preserving high-frequency texture and edges, making it preferred for film grain preservation vs. noise reduction.
- For GPU-accelerated denoising in production workflows, consider `bm3d` which has a two-pass mode for even higher quality.

---

### noise

> Add noise or grain to video with configurable strength, type, and per-component settings.

**Source:** [libavfilter/vf_noise.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_noise.c)

The `noise` filter adds noise or grain to video frames. It can generate uniform, Gaussian, or temporally-correlated noise on any combination of color planes. Common uses include adding film grain for aesthetic purposes, simulating film stock, or reducing banding by dithering smooth gradients.

## Quick Start

```sh
# Add moderate grain to luma only
ffmpeg -i input.mp4 -vf "noise=alls=15:allf=t+u" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_seed / alls | int | `123457` | Random seed for all components. |
| all_strength / alls | int | `0` | Noise strength for all components. Range: 0–100. |
| all_flags / allf | flags | `0` | Noise type flags for all components. See below. |
| c0_seed | int | — | Seed for component 0 (Y/R). |
| c0_strength / c0s | int | `0` | Noise strength for component 0. |
| c0_flags / c0f | flags | `0` | Noise type for component 0. |
| c1_*/c2_*/c3_* | — | — | Per-component variants for planes 1, 2, and 3. |

### Flag values

| Flag | Description |
|------|-------------|
| `a` | Averaged noise (averages multiple noise samples, smoother). |
| `p` | Planar processing. |
| `s` | Saturation (apply noise only to saturated areas). |
| `u` | Uniform distribution noise. |
| `t` | Temporal noise (same noise pattern across frames, reduces flickering). |

## Examples

### Add film-grain-style noise (luma only)

```sh
ffmpeg -i input.mp4 -vf "noise=c0s=20:c0f=t+u" output.mp4
```

### Add grain to all planes

```sh
ffmpeg -i input.mp4 -vf "noise=alls=15:allf=t+u" output.mp4
```

### Anti-banding dithering noise

Very light noise to break up gradient banding.

```sh
ffmpeg -i gradient.mp4 -vf "noise=alls=4:allf=u" output.mp4
```

### Heavy noise for stylized effect

```sh
ffmpeg -i input.mp4 -vf "noise=alls=50:allf=u" output.mp4
```

## Notes

- Combine `t` (temporal) and `u` (uniform) flags: `allf=t+u` adds consistent, film-grain-like noise that doesn't flicker frame to frame.
- `all_strength` (or `alls`) is the main control: 5–10 for subtle grain, 20–40 for heavy grain, 50+ for extreme effect.
- Adding noise before encoding can actually *improve* compression efficiency on content with banding, because the noise gives the encoder more variation to quantize.
- Per-component flags (`c0f`, `c1f`, etc.) allow separate behavior: e.g., noisy luma but smooth chroma.

---

### null

> Pass the input video through unchanged — a no-op filter useful for testing and filtergraph construction.

**Source:** [libavfilter/vf_null.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_null.c)

The `null` filter passes every video frame from input to output without any modification. It is a no-op and has no effect on the video content, timestamps, or metadata. Its primary uses are in testing filtergraph pipelines, as a placeholder when a filter is conditionally needed, and as a required endpoint when using `-filter_complex` without a terminal filter.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "null" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Pass-through for testing pipeline overhead

Measure the encoding overhead of a filtergraph without any actual filtering.

```sh
ffmpeg -i input.mp4 -vf "null" output.mp4
```

### Use as a placeholder in a conditional pipeline

Insert `null` as a no-op stage while developing or debugging a filtergraph that will later use a real filter.

```sh
ffmpeg -i input.mp4 -vf "null,scale=1280:720" output.mp4
```

### Terminate a filter_complex branch

In a complex filtergraph, route an unused output to `nullsink` (the sink version) to avoid errors.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[main][discard]; [discard]nullsink" \
  -map "[main]" output.mp4
```

## Notes

- `null` has zero processing cost and is completely transparent to the frame pipeline.
- The audio equivalent is `anull`.
- When using `-filter_complex`, if a labeled output is not mapped to an output file, use `nullsink` (not `null`) to consume and discard the unused stream.
- The filter is also useful for benchmarking decoders: `ffmpeg -i input.mp4 -vf "null" -f null -` discards all output and measures decode throughput.

---

### overlay

> Overlay a second video on top of the first at a specified position, supporting transparency and dynamic coordinates.

**Source:** [libavfilter/vf_overlay.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_overlay.c)

The `overlay` filter composites two video streams together, placing the second input (the overlay) on top of the first input (the main video) at coordinates given by `x` and `y` expressions. Both inputs must be connected as separate streams using the filtergraph syntax. The filter supports alpha transparency, various output pixel formats, and dynamic position updates per frame, making it useful for watermarking, picture-in-picture, and logo placement.

## Quick Start

```sh
ffmpeg -i main.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | string (expr) | `0` | Horizontal position of the overlay's top-left corner on the main video. |
| y | string (expr) | `0` | Vertical position of the overlay's top-left corner on the main video. |
| eof_action | int | repeat | Action when the overlay input ends: `repeat` (last frame), `endall` (end output), `pass` (pass main through). |
| eval | int | frame | When to evaluate `x`/`y`: `init` (once) or `frame` (per frame). |
| shortest | bool | 0 | Terminate output when the shortest input ends. |
| format | int | yuv420 | Output pixel format: `yuv420`, `yuv444`, `rgb`, `gbrp`, `auto`, etc. |
| repeatlast | bool | 1 | Continue repeating the last overlay frame after its stream ends. |
| alpha | int | auto | Alpha compositing mode for the overlay: `straight`, `premultiplied`, or `auto`. |

## Expression Variables

The `x` and `y` options accept expressions with the following variables:

| Variable | Description |
|----------|-------------|
| `main_w` / `W` | Main (background) input width |
| `main_h` / `H` | Main (background) input height |
| `overlay_w` / `w` | Overlay input width |
| `overlay_h` / `h` | Overlay input height |
| `x` | Current computed x value |
| `y` | Current computed y value |
| `n` | Input frame number |
| `t` | Timestamp in seconds |
| `hsub` / `vsub` | Chroma subsample values of the output format |

## Examples

### Place a watermark in the bottom-right corner

Position a logo image 10 pixels from the right and bottom edges of the main video.

```sh
ffmpeg -i input.mp4 -i logo.png \
  -filter_complex "overlay=main_w-overlay_w-10:main_h-overlay_h-10" \
  output.mp4
```

### Picture-in-picture (PiP)

Scale a second video to 320x180 and place it in the top-right corner.

```sh
ffmpeg -i main.mp4 -i pip.mp4 \
  -filter_complex "[1:v]scale=320:180[pip]; [0:v][pip]overlay=main_w-320-10:10" \
  output.mp4
```

### Animated overlay that slides in from the left

Move the overlay from off-screen left to its final position over 2 seconds.

```sh
ffmpeg -i main.mp4 -i banner.png \
  -filter_complex "overlay=x='if(lt(t,2),t*200-overlay_w,200)':y=50" \
  output.mp4
```

### Overlay a semi-transparent PNG logo

Use a PNG with an alpha channel; the filter handles compositing automatically.

```sh
ffmpeg -i input.mp4 -i logo_alpha.png \
  -filter_complex "overlay=10:10:format=auto" \
  output.mp4
```

### Align two streams to the same start time

When inputs have different start timestamps, reset both to zero before overlaying to avoid sync issues.

```sh
ffmpeg -i main.mp4 -i overlay.mp4 \
  -filter_complex \
    "[0:v]setpts=PTS-STARTPTS[bg]; \
     [1:v]setpts=PTS-STARTPTS[fg]; \
     [bg][fg]overlay=0:0" \
  output.mp4
```

## Notes

- Both inputs must be provided via the filtergraph; a single `-vf overlay` won't work — you need `-filter_complex` or `-lavfi`.
- When `eval=init`, the `t` and `n` variables evaluate to NaN; use `eval=frame` for time-dependent positioning.
- Output is in `yuv420` by default; use `format=auto` or `format=rgb` when the overlay contains full color information or alpha that yuv420 can't represent accurately.
- For static images used as overlays (e.g., logos), loop the image with `-loop 1` and use `shortest=1` or `eof_action=repeat` to keep it visible for the full duration of the main video.

---

### pad

> Add padding around the input video to reach a specified output size, placing the original frame at given coordinates.

**Source:** [libavfilter/vf_pad.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_pad.c)

The `pad` filter adds colored borders around the input video to produce a larger output canvas. You specify the desired output dimensions and the `(x, y)` offset at which the original frame is placed. All parameters accept arithmetic expressions, making it easy to center the input, create letterbox/pillarbox effects, or add exact pixel margins. The padding area is filled with a configurable color (default black).

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| width (w) | string (expr) | `0` (= input width) | Width of the output padded frame. |
| height (h) | string (expr) | `0` (= input height) | Height of the output padded frame. |
| x | string (expr) | `0` | Horizontal offset of the input frame within the padded canvas. Negative values center the input. |
| y | string (expr) | `0` | Vertical offset of the input frame within the padded canvas. Negative values center the input. |
| color | color | `black` | Fill color for the padded area. |
| eval | int | `init` | When to evaluate expressions: `init` (once) or `frame` (per frame). |
| aspect | rational | — | Pad to fit a given display aspect ratio instead of a fixed resolution. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output (padded) width |
| `oh` / `out_h` | Output (padded) height |
| `x` / `y` | Offset values (can reference each other) |
| `a` | Input aspect ratio (`iw/ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `hsub` / `vsub` | Chroma subsample values |

## Examples

### Letterbox to 16:9 (add black bars)

Take a 4:3 video and pad it to 16:9 by adding bars on the left and right sides.

```sh
ffmpeg -i input_4_3.mp4 -vf "pad=ih*16/9:ih:(ow-iw)/2:0" output.mp4
```

### Center video in a 1920x1080 canvas

Place the input at the center of a Full HD frame, regardless of its original size.

```sh
ffmpeg -i input.mp4 -vf "pad=1920:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```

### Add a uniform 20-pixel border

Extend each side by 20 pixels, placing the input at (20, 20).

```sh
ffmpeg -i input.mp4 -vf "pad=iw+40:ih+40:20:20" output.mp4
```

### Pad to 16:9 aspect ratio with white background

Use the `aspect` option with a custom fill color.

```sh
ffmpeg -i input.mp4 -vf "pad=aspect=16/9:color=white:x=(ow-iw)/2:y=(oh-ih)/2" output.mp4
```

### Pad for 9:16 portrait format

Add pillarbox bars to a landscape video for a vertical platform.

```sh
ffmpeg -i landscape.mp4 -vf "scale=-2:1920,pad=1080:1920:(ow-iw)/2:0" portrait.mp4
```

## Notes

- The `x` and `y` expressions can reference `ow`/`oh`, allowing centering math like `(ow-iw)/2` before the final dimensions are known.
- If `x` or `y` evaluates to a negative number, the filter automatically centers the input within the padded area.
- To add padding and then scale, chain `pad` before `scale`; to add padding to a scaled result, chain `scale` before `pad`.
- The `color` parameter accepts any FFmpeg color string including hex (`#RRGGBB`), named colors, and colors with alpha (`black@0.5`).

---

### palettegen

> Generate an optimized 256-color palette image from a video stream, for use in high-quality GIF encoding.

**Source:** [libavfilter/vf_palettegen.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_palettegen.c)

The `palettegen` filter analyzes a video stream and generates an optimized 256-color palette image that best represents the colors in the input. This palette is then used by the `paletteuse` filter in a two-pass GIF encoding workflow to produce significantly better-looking GIFs than single-pass approaches. The output is a 256x1 PNG image containing the color palette. `palettegen` and `paletteuse` are designed to be used together.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "palettegen" palette.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| max_colors | int | `256` | Maximum number of colors to include in the palette. The palette always contains 256 entries; unused entries are black. |
| reserve_transparent | bool | `1` | Reserve one palette entry for transparency, leaving up to 255 opaque colors. Recommended for GIF use. |
| transparency_color | color | — | Background color to use for transparent areas. |
| stats_mode | int | `full` | How to build the color histogram: `full` (whole frame), `diff` (changed areas only), or `single` (per-frame, one palette per frame). |

### `stats_mode` values

| Value | Description |
|-------|-------------|
| `full` | Compute histogram from the entire frame. Best for static or slow-moving content. |
| `diff` | Only include pixels that changed from the previous frame. Good for animations with a static background. |
| `single` | Compute a new palette for each frame. Used with `paletteuse new=1` for per-frame palettes. |

## Examples

### Generate a palette for GIF encoding

First pass of the two-pass GIF workflow: analyze the video and save the palette.

```sh
ffmpeg -i input.mp4 -vf "palettegen" palette.png
```

### Palette optimized for moving content

Use `stats_mode=diff` to bias the palette toward the colors in motion, improving quality for animated content with a static background.

```sh
ffmpeg -i input.mp4 -vf "palettegen=stats_mode=diff" palette.png
```

### Limit palette to 128 colors

Reduce the color count for smaller GIF files at the cost of some quality.

```sh
ffmpeg -i input.mp4 -vf "palettegen=max_colors=128" palette.png
```

### Full two-pass GIF creation

Complete workflow: generate palette then use it to encode a high-quality GIF.

```sh
ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i input.mp4 -i palette.png -lavfi "fps=15,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" output.gif
```

## Notes

- `palettegen` and `paletteuse` must always be used together — the palette image generated by `palettegen` is the second input to `paletteuse`.
- `reserve_transparent=1` (the default) reserves one palette slot for GIF transparency. Disable it (`reserve_transparent=0`) when generating a palette for a standalone image with no transparency.
- The filter exports the frame metadata `lavfi.color_quant_ratio` which indicates the quality of color quantization; a ratio close to 1 means excellent palette coverage.
- For the best GIF quality, pre-process the input with `fps` and `scale` to normalize the frame rate and dimensions before running `palettegen`.

---

### paletteuse

> Apply a pre-generated color palette to a video stream using dithering, producing high-quality GIF output.

**Source:** [libavfilter/vf_paletteuse.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_paletteuse.c)

The `paletteuse` filter takes two inputs — a video stream and a 256-color palette image (generated by `palettegen`) — and maps the video colors to the palette using configurable dithering algorithms. This is the second and final step of the two-pass GIF encoding workflow. The choice of dithering mode significantly affects the visual quality and file size of the output GIF. `paletteuse` and `palettegen` are designed to be used together.

## Quick Start

```sh
ffmpeg -i input.mp4 -i palette.png \
  -lavfi "paletteuse" output.gif
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dither | int | `sierra2_4a` | Dithering algorithm to use (see table below). |
| bayer_scale | int | `2` | Scale of the bayer dither pattern (0–5). Lower = more visible pattern but less banding. |
| diff_mode | int | `none` | Process only changed regions (`rectangle`) or everything (`none`). |
| new | bool | `0` | Take a new palette for each output frame (used with `stats_mode=single` in `palettegen`). |
| alpha_threshold | int | `128` | Alpha values above this are treated as fully opaque; below as fully transparent. Range: [0, 255]. |

### Dithering algorithms

| Value | Description |
|-------|-------------|
| `bayer` | Ordered 8x8 bayer dithering (deterministic, cross-hatch pattern). |
| `heckbert` | Simple error diffusion as defined by Paul Heckbert (reference implementation). |
| `floyd_steinberg` | Floyd-Steinberg error diffusion (widely used, smooth results). |
| `sierra2` | Frankie Sierra v2 error diffusion. |
| `sierra2_4a` | Frankie Sierra v2 "Lite" (default — good balance of quality and file size). |
| `sierra3` | Frankie Sierra v3 error diffusion. |
| `burkes` | Burkes error diffusion. |
| `atkinson` | Atkinson dithering (Apple Computer, preserves highlights). |
| `none` | No dithering — direct color mapping. |

## Examples

### Basic GIF encoding with default dithering

Second pass of the two-pass GIF workflow using the default `sierra2_4a` dither.

```sh
ffmpeg -i input.mp4 -i palette.png \
  -lavfi "[0:v][1:v]paletteuse" output.gif
```

### Use Floyd-Steinberg dithering

Floyd-Steinberg produces smoother gradients for photographic content.

```sh
ffmpeg -i input.mp4 -i palette.png \
  -lavfi "[0:v][1:v]paletteuse=dither=floyd_steinberg" output.gif
```

### Bayer dithering for retro look

Use bayer dithering with a high scale for a deliberate pixel-art aesthetic.

```sh
ffmpeg -i input.mp4 -i palette.png \
  -lavfi "[0:v][1:v]paletteuse=dither=bayer:bayer_scale=4" output.gif
```

### Full two-pass GIF pipeline in a single command

Run both palettegen and paletteuse in one FFmpeg invocation using filter_complex.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]fps=15,scale=480:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  output.gif
```

### Reduce GIF noise with diff_mode

Only re-process the changed rectangular region per frame, which reduces error diffusion noise in static areas.

```sh
ffmpeg -i input.mp4 -i palette.png \
  -lavfi "[0:v][1:v]paletteuse=diff_mode=rectangle" output.gif
```

## Notes

- `paletteuse` requires two inputs: `[0:v]` is the video to encode and `[1:v]` is the 256-color palette PNG from `palettegen`. Use `-lavfi` or `-filter_complex` to connect them.
- The dithering algorithm has a large effect on both visual quality and GIF file size: error diffusion methods (`floyd_steinberg`, `sierra2_4a`) generally produce better visuals, while `bayer` produces smaller, more compressible output.
- `diff_mode=rectangle` can significantly reduce file size and visual noise for animations with large static areas by limiting dithering to the bounding box of changed pixels.
- When the input video has transparent areas (e.g., RGBA), adjust `alpha_threshold` to control what alpha level counts as transparent in the GIF.

---

### perspective

> Correct or apply perspective distortion by mapping four corner points to new positions.

**Source:** [libavfilter/vf_perspective.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_perspective.c)

The `perspective` filter applies a perspective transformation by mapping four corner points of the input frame to new positions. It can be used to correct keystoning (when a projector or camera is not perpendicular to the subject), or to warp video to match a surface's perspective. The corners are numbered 0 (top-left), 1 (top-right), 2 (bottom-left), 3 (bottom-right).

## Quick Start

```sh
# Correct slight trapezoidal distortion
ffmpeg -i input.mp4 -vf "perspective=x0=30:y0=0:x1=1890:y1=0:x2=0:y2=1080:x3=1920:y3=1080" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x0 | string | `0` | X-coordinate of top-left corner. Expression, can use `iw`/`ih`. |
| y0 | string | `0` | Y-coordinate of top-left corner. |
| x1 | string | `iw` | X-coordinate of top-right corner. |
| y1 | string | `0` | Y-coordinate of top-right corner. |
| x2 | string | `0` | X-coordinate of bottom-left corner. |
| y2 | string | `ih` | Y-coordinate of bottom-left corner. |
| x3 | string | `iw` | X-coordinate of bottom-right corner. |
| y3 | string | `ih` | Y-coordinate of bottom-right corner. |
| interpolation | int | `linear` | Interpolation: `linear` or `cubic`. |
| sense | int | `source` | Interpretation: `source` (corners in input) or `destination` (corners in output). |

## Examples

### Correct trapezoid (top is narrower than bottom)

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=80:y0=0:x1=1840:y1=0:x2=0:y2=1080:x3=1920:y3=1080:sense=source" output.mp4
```

### Map video onto a tilted surface

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=100:y0=50:x1=1820:y1=30:x2=50:y2=1050:x3=1870:y3=1070" output.mp4
```

### Cubic interpolation for better quality

```sh
ffmpeg -i input.mp4 -vf "perspective=x0=50:y0=0:x1=1870:y1=0:x2=0:y2=1080:x3=1920:y3=1080:interpolation=cubic" output.mp4
```

## Notes

- Corner coordinates are (x0,y0)=top-left, (x1,y1)=top-right, (x2,y2)=bottom-left, (x3,y3)=bottom-right.
- With `sense=source`, the coordinates specify where the input corners *are* (the filter maps them to a rectangle). With `sense=destination`, the coordinates specify where the corners should *go*.
- `cubic` interpolation gives better quality at the cost of speed; use it for final output.
- For barrel/pincushion lens correction (radial distortion), use `lenscorrection` instead.

---

### psnr

> Calculate the Peak Signal-to-Noise Ratio (PSNR) quality metric between two video streams.

**Source:** [libavfilter/vf_psnr.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_psnr.c)

The `psnr` filter computes the Peak Signal-to-Noise Ratio between two video streams — typically an original and a compressed or processed version. Higher PSNR (in dB) indicates less distortion. The filter outputs per-frame PSNR values to a file or stderr while passing the first stream through unchanged, making it useful for codec quality evaluation and comparison.

## Quick Start

```sh
# Compare original and encoded video; print PSNR to stderr
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file / f | string | — | Path to a file where per-frame PSNR statistics are written. If omitted, summary is printed to stderr. |
| stats_version | int | `1` | Format version for the stats file (1 or 2). Version 2 adds more columns. |
| output_max | bool | `0` | If enabled, also log the maximum PSNR value. |

## Examples

### Print PSNR summary to stderr

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr" -f null -
```

### Save per-frame PSNR to a log file

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]psnr=stats_file=psnr.log" -f null -
```

### Compare H.264 encodings at different CRF values

```sh
# Encode at CRF 23
ffmpeg -i original.mp4 -c:v libx264 -crf 23 encoded_23.mp4

# Compare
ffmpeg -i original.mp4 -i encoded_23.mp4 \
  -filter_complex "[0:v][1:v]psnr=f=psnr_23.log" -f null -
```

### PSNR alongside SSIM

Compute both metrics in a single pass.

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v]split[a][b];[1:v]split[c][d];[a][c]psnr;[b][d]ssim" -f null -
```

## Notes

- PSNR is reported in dB. Values above 40 dB are generally considered visually lossless; 30–40 dB is acceptable quality; below 30 dB is noticeably degraded.
- The first input (`[0:v]`) is the reference; the second (`[1:v]`) is the test. The first stream is passed through to the output unchanged.
- Use `-f null -` as the output to discard the video output and only collect statistics.
- PSNR correlates imperfectly with perceptual quality — `ssim` is a better perceptual metric for most use cases.

---

### rotate

> Rotate video frames by an arbitrary angle expressed in radians, with configurable output dimensions and fill color.

**Source:** [libavfilter/vf_rotate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_rotate.c)

The `rotate` filter rotates video frames clockwise by an arbitrary angle specified in radians. Unlike `transpose`, which only supports 90-degree increments, `rotate` handles any angle and can animate the rotation per frame using expressions. The output dimensions can be independently controlled, and any uncovered area is filled with a configurable color (or made transparent with `none`). Bilinear interpolation is enabled by default for smooth results.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "rotate=PI/4" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| angle (a) | string (expr) | `0` | Clockwise rotation angle in radians. Negative values rotate counter-clockwise. Evaluated per frame. |
| out_w (ow) | string (expr) | `iw` | Output frame width. Evaluated once at configuration time. |
| out_h (oh) | string (expr) | `ih` | Output frame height. Evaluated once at configuration time. |
| fillcolor (c) | string | `black` | Color used to fill areas not covered by the rotated frame. Use `none` for transparent. |
| bilinear | bool | `1` | Enable bilinear interpolation for smoother rotated output. |

## Expression Variables

The `angle`, `out_w`, and `out_h` options accept these constants:

| Variable | Description |
|----------|-------------|
| `n` | Sequential input frame number, starting from 0 |
| `t` | Time in seconds of the current frame |
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output width |
| `oh` / `out_h` | Output height |
| `hsub` / `vsub` | Chroma subsample values |
| `rotw(a)` | Minimum output width to fully contain the input rotated by `a` radians |
| `roth(a)` | Minimum output height to fully contain the input rotated by `a` radians |

## Examples

### Rotate 45 degrees clockwise

Convert the angle from degrees to radians by multiplying by `PI/180`.

```sh
ffmpeg -i input.mp4 -vf "rotate=45*PI/180" output.mp4
```

### Rotate 90 degrees counter-clockwise

Use a negative angle to go counter-clockwise.

```sh
ffmpeg -i input.mp4 -vf "rotate=-PI/2" output.mp4
```

### Expand canvas to show the full rotated frame

Use the `rotw`/`roth` helper functions to set the output size large enough to contain the entire rotated frame.

```sh
ffmpeg -i input.mp4 -vf "rotate=PI/6:ow=rotw(PI/6):oh=roth(PI/6)" output.mp4
```

### Animated continuous rotation

Rotate the video continuously, completing one full revolution every 5 seconds.

```sh
ffmpeg -i input.mp4 -vf "rotate=2*PI*t/5" output.mp4
```

### Oscillating wobble effect

Apply a sinusoidal rotation for a subtle wobble animation at 1 Hz with 5-degree amplitude.

```sh
ffmpeg -i input.mp4 -vf "rotate=5*PI/180*sin(2*PI*t)" output.mp4
```

## Notes

- Angles are in radians; multiply degrees by `PI/180` to convert.
- By default, the output canvas retains the input dimensions (`iw` x `ih`), which means corners of the rotated image will be clipped. Use `rotw`/`roth` to expand the canvas.
- Setting `fillcolor=none` produces transparent areas if the output format supports alpha (e.g., PNG); for opaque formats, `none` renders as black.
- `bilinear=0` disables interpolation for a faster but pixelated rotation — useful mainly for pixel art or debugging.

---

### scale

> Scale the input video size and/or convert the image format.

**Source:** [libavfilter/vf_scale.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_scale.c)

The `scale` filter resizes video frames to the specified width and height, delegating the actual scaling to the libswscale library. It preserves the display aspect ratio by adjusting the sample aspect ratio, and can also convert between pixel formats as needed by the downstream filter chain. Use it whenever you need to change resolution, fit a video into a target size, or normalize dimensions before encoding.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| w (width) | string (expr) | input width | Output width expression. Use `-1` to preserve aspect ratio based on height. |
| h (height) | string (expr) | input height | Output height expression. Use `-1` to preserve aspect ratio based on width. |
| flags | string | (libswscale default) | Scaling algorithm flags passed to libswscale (e.g., `bilinear`, `bicubic`, `lanczos`). |
| interl | bool | 0 | Interlacing mode: `1` forces interlaced-aware scaling, `-1` auto-detects from frame flags. |
| force_original_aspect_ratio | int | 0 | `1` = decrease dimensions to fit, `2` = increase dimensions to fit, preserving the original AR. |
| force_divisible_by | int | 1 | When using `force_original_aspect_ratio`, ensure the output dimensions are divisible by this value. |
| in_color_matrix | int | auto | Input YCbCr color matrix (e.g., `bt709`, `bt601`). |
| out_color_matrix | int | auto | Output YCbCr color matrix. |
| eval | int | init | When to evaluate expressions: `init` (once) or `frame` (per frame). |

## Expression Variables

The `w` and `h` options accept arithmetic expressions with the following variables:

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input video width |
| `ih` / `in_h` | Input video height |
| `ow` / `out_w` | Output width (can reference `oh`) |
| `oh` / `out_h` | Output height (can reference `ow`) |
| `a` | Input aspect ratio (`iw / ih`) |
| `sar` | Input sample aspect ratio |
| `dar` | Input display aspect ratio |
| `n` | Input frame number |
| `t` | Input frame timestamp in seconds |

## Examples

### Scale to 720p keeping aspect ratio

Scale the width to 1280 and let FFmpeg calculate the height automatically to preserve the input aspect ratio. The `-1` value means "compute from the other dimension."

```sh
ffmpeg -i input.mp4 -vf "scale=1280:-1" output.mp4
```

### Scale to height, ensure width is divisible by 2

Use `-2` instead of `-1` to also guarantee the computed dimension is even — required by many codecs.

```sh
ffmpeg -i input.mp4 -vf "scale=-2:720" output.mp4
```

### Halve the resolution

Use expressions relative to the input dimensions to produce output at half the original size.

```sh
ffmpeg -i input.mp4 -vf "scale=iw/2:ih/2" output.mp4
```

### Scale to fit within 1280x720 without upscaling

Use `force_original_aspect_ratio=decrease` to scale down a video so it fits within the target box while preserving AR.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720:force_original_aspect_ratio=decrease" output.mp4
```

### High-quality downscale with Lanczos

Use the `lanczos` flag for sharper results when downscaling, at a higher CPU cost.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720:flags=lanczos" output.mp4
```

## Notes

- When one dimension is set to `-1`, the filter computes the other to maintain the input AR. Use `-2` to also ensure the result is even (required by most YUV codecs).
- If both `w` and `h` are `0`, the input dimensions are passed through unchanged.
- The `flags` parameter controls the scaling algorithm quality; common values are `bilinear` (fast, lower quality), `bicubic` (balanced), and `lanczos` (high quality, slow).
- When chaining `scale` after `crop` or `pad`, order matters: scaling after cropping reduces work; scaling before can improve quality if the source is much larger than the crop target.

---

### scdet

> Detect scene changes in video and output scene change scores as frame metadata.

**Source:** [libavfilter/vf_scdet.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_scdet.c)

The `scdet` filter detects scene changes in video by computing the difference between consecutive frames. It writes a `lavfi.scene_score` metadata value (0–100) to each frame. Frames with a score above the threshold are considered scene changes and can be extracted or processed separately by chaining with the `select` filter.

## Quick Start

```sh
# Detect scene changes and print timestamps to stderr
ffmpeg -i input.mp4 -vf "scdet" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| threshold / t | double | `10.0` | Scene change score threshold (0–100). Frames above this score are flagged as scene changes. |
| sc_pass / s | bool | `0` | If true, only pass frames that are flagged as scene changes to the output. |

## Examples

### Detect and log all scene changes

```sh
ffmpeg -i input.mp4 -vf "scdet=threshold=10" -f null - 2>&1 | grep "scene_score"
```

### Extract only scene change frames as JPEG thumbnails

Use `scdet` to detect, then `select` to filter.

```sh
ffmpeg -i input.mp4 \
  -vf "scdet=threshold=8,select='gte(scene_score,8)'" \
  -vsync vfr scene_%04d.jpg
```

### Adjust threshold for detecting only large scene changes

```sh
ffmpeg -i documentary.mp4 -vf "scdet=threshold=25" -f null -
```

### Output only scene change frames (sc_pass mode)

```sh
ffmpeg -i input.mp4 -vf "scdet=t=10:s=1" -vsync vfr scenes_%04d.png
```

## Notes

- `lavfi.scene_score` is set on every frame; values approaching 100 indicate very different consecutive frames (hard cuts). Values of 10–20 are typical for gradual transitions.
- Lower threshold → more scene changes detected (including gradual transitions and camera moves); higher threshold → only hard cuts.
- The `select` filter can read the `scene_score` metadata: `select='gt(scene_score\\,0.3)'` (note the backslash escape in shell).
- `sc_pass=1` drops all non-scene-change frames — use with `-vsync vfr` to preserve timestamps when outputting image sequences.

---

### select

> Select or filter video frames based on an expression, passing only frames that match specified criteria.

**Source:** [libavfilter/f_select.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_select.c)

The `select` filter evaluates an expression for each input frame and passes or discards the frame based on the result. Frames for which the expression evaluates to zero are dropped; non-zero values route the frame to an output (the integer ceiling of the result minus 1 determines which output index for multi-output use). This enables precise frame selection based on timestamp, frame type (I/P/B), scene change score, key frame status, or any arithmetic combination of these variables.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframes_%04d.jpg
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr (e) | string | — | Expression evaluated for each frame. Non-zero = pass; zero = discard. |
| outputs (n) | int | `1` | Number of output streams. Frames are routed to output `ceil(result)-1`. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Sequential frame number, starting from 0 |
| `selected_n` | Sequential number of selected frames |
| `prev_selected_n` | Frame number of the previously selected frame |
| `t` | Frame timestamp in seconds |
| `pts` | Frame PTS in timebase units |
| `prev_pts` | PTS of the previously filtered frame |
| `prev_selected_pts` | PTS of the previously selected frame |
| `prev_selected_t` | Timestamp of the previously selected frame in seconds |
| `start_pts` | PTS of the first non-NaN frame |
| `start_t` | Timestamp of the first frame in seconds |
| `pict_type` | Frame type: `I`, `P`, `B`, `S`, `SI`, `SP`, `BI` |
| `key` | `1` if the frame is a keyframe, `0` otherwise |
| `scene` | Scene change score (0.0 to 1.0); higher = more likely a new scene |
| `interlace_type` | `PROGRESSIVE`, `TOPFIRST`, or `BOTTOMFIRST` |
| `TB` | Input timebase |
| `concatdec_select` | Used with the concat demuxer to filter in/out points |

## Examples

### Extract only keyframes

Select only I-frames (keyframes) and save them as images.

```sh
ffmpeg -i input.mp4 -vf "select='eq(pict_type,I)'" -vsync vfr keyframes_%04d.jpg
```

### Extract one frame per second

Use the timestamp to select one frame at each whole second.

```sh
ffmpeg -i input.mp4 -vf "select='isnan(prev_selected_t)+gte(t-prev_selected_t,1)'" -vsync vfr fps1_%04d.jpg
```

### Detect scene changes

Select frames where the scene change score exceeds a threshold, useful for finding cut points.

```sh
ffmpeg -i input.mp4 -vf "select='gt(scene,0.4)',showinfo" -f null -
```

### Split frames into two outputs by type

Route I-frames to one output and all other frames to a second output for different processing.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]select='if(eq(pict_type,I),1,2)':outputs=2[iframes][others]" \
  -map "[iframes]" iframes.mp4 \
  -map "[others]" others.mp4
```

### Select every Nth frame

Keep every 10th frame to create a time-lapse effect.

```sh
ffmpeg -i input.mp4 -vf "select='not(mod(n,10))'" -vsync vfr timelapse.mp4
```

## Notes

- When using `select` to extract frames as images, always add `-vsync vfr` (or `-fps_mode vfr`) to prevent FFmpeg from duplicating frames to maintain a constant output rate.
- The `scene` variable requires prior scene detection; use `select=scene` alongside `showinfo` or `metadata` filters to inspect scores before choosing a threshold.
- For simple time-based trimming, `trim` is more efficient than `select` because `trim` avoids evaluating the expression for every frame.
- When routing to multiple outputs with `outputs=N`, a result of `0` drops the frame entirely; results `1` through `N` route to outputs 0 through N-1.

---

### selectivecolor

> Adjust CMYK values selectively for specific color ranges such as reds, greens, blues, and neutrals.

**Source:** [libavfilter/vf_selectivecolor.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_selectivecolor.c)

The `selectivecolor` filter applies CMYK (Cyan, Magenta, Yellow, Black) color adjustments to specific color families in the image, similar to the Selective Color tool in Photoshop. You can independently adjust cyan/magenta/yellow/black components in nine color ranges: reds, yellows, greens, cyans, blues, magentas, whites, neutrals, and blacks.

## Quick Start

```sh
# Add cyan to blues for a cool, film-like look
ffmpeg -i input.mp4 -vf "selectivecolor=blues=0.1:-0.05:0:0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| correction_method | int | `absolute` | `absolute` (fixed adjustment) or `relative` (proportional to existing value). |
| reds | string | — | Adjustment for red tones: `cyan:magenta:yellow:black` (each -1 to 1). |
| yellows | string | — | Adjustment for yellow tones. |
| greens | string | — | Adjustment for green tones. |
| cyans | string | — | Adjustment for cyan tones. |
| blues | string | — | Adjustment for blue tones. |
| magentas | string | — | Adjustment for magenta tones. |
| whites | string | — | Adjustment for highlight tones. |
| neutrals | string | — | Adjustment for midtone neutral tones. |
| blacks | string | — | Adjustment for shadow/dark tones. |

## Examples

### Warm up reds (reduce cyan in reds)

```sh
ffmpeg -i portrait.mp4 -vf "selectivecolor=reds=-0.1:0:0.1:0" output.mp4
```

### Make greens more vibrant

```sh
ffmpeg -i landscape.mp4 -vf "selectivecolor=greens=-0.1:-0.05:0.15:0" output.mp4
```

### Add density to blacks (shadow lift)

```sh
ffmpeg -i input.mp4 -vf "selectivecolor=blacks=0:0:0:0.1" output.mp4
```

### Cool highlight look

```sh
ffmpeg -i input.mp4 -vf "selectivecolor=whites=0.05:-0.05:-0.1:0" output.mp4
```

## Notes

- Each color range takes four values in order: `cyan:magenta:yellow:black`. Positive cyan = more cyan (cooler/more blue-green); negative cyan = less cyan (warmer/more red).
- In `absolute` mode, the value is added directly; in `relative` mode, it is scaled by the existing component amount.
- Values outside the range of -1 to 1 will be clamped. Subtle adjustments of 0.05–0.15 are usually sufficient.
- Selective color gives finer control than `colorbalance` because it targets specific color families rather than tonal regions (shadows/midtones/highlights).

---

### setpts

> Rewrite the presentation timestamps (PTS) of video frames using an arbitrary arithmetic expression.

**Source:** [libavfilter/setpts.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/setpts.c)

The `setpts` filter replaces the PTS (presentation timestamp) of each video frame with the result of a user-defined expression. This gives precise control over playback speed (fast motion / slow motion), timestamp normalization, fixed-rate output, and custom timing patterns. The audio equivalent is `asetpts`. Because `setpts` only modifies timestamps — not frame content — it is a zero-copy, lossless operation.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS-STARTPTS" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string (expr) | — | Expression evaluated for each frame to produce the new PTS value. |
| strip_fps | bool | `false` | If true, remove the framerate metadata. Recommended when sending to a VFR muxer. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | The current input frame's PTS in timebase units |
| `STARTPTS` | PTS of the very first frame |
| `TB` | The input timebase (e.g., `1/90000`) |
| `T` | Current frame time in seconds |
| `STARTT` | Time of the first frame in seconds |
| `N` | Sequential frame count starting from 0 |
| `FRAME_RATE` / `FR` | Input frame rate (only defined for CFR video) |
| `PREV_INPTS` | PTS of the previous input frame |
| `PREV_INT` | Time of the previous input frame in seconds |
| `PREV_OUTPTS` | PTS of the previous output frame |
| `PREV_OUTT` | Time of the previous output frame in seconds |
| `INTERLACED` | 1 if the current frame is interlaced |
| `T_CHANGE` | Time of the first frame after a runtime command was applied |

## Examples

### Reset timestamps to start at zero

Remove any initial timestamp offset so the output starts at PTS 0. This is almost always needed after `trim`.

```sh
ffmpeg -i input.mp4 -vf "trim=10:20,setpts=PTS-STARTPTS" output.mp4
```

### Slow motion (2x slower)

Double all PTS values to stretch the video to twice its original duration.

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" output.mp4
```

### Fast motion (4x faster)

Quarter the PTS values to compress the video to one-quarter its original duration.

```sh
ffmpeg -i input.mp4 -vf "setpts=0.25*PTS" output.mp4
```

### Force a fixed 25 fps rate from frame count

Generate synthetic PTS based on frame number, ignoring the original timestamps.

```sh
ffmpeg -i input.mp4 -vf "setpts=N/(25*TB)" output.mp4
```

### Add a 10-second delay to the video

Shift all timestamps forward by 10 seconds (in timebase units) without changing playback speed.

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS+10/TB" output.mp4
```

## Notes

- `setpts` modifies only PTS values; it does not insert or remove frames. To change the number of frames, use `fps` (to duplicate/drop) or `minterpolate` (to interpolate).
- For slow-motion that also needs extra frames inserted, combine `setpts` with `fps`: `setpts=2*PTS,fps=fps=50` stretches time and then fills in extra frames via duplication.
- The expression is evaluated in the timebase of the input; divide time-in-seconds values by `TB` to get the correct PTS units.
- For audio timestamps, use the `asetpts` filter instead. When doing speed changes, process both streams together to maintain sync.

---

### setsar

> Set the sample (pixel) aspect ratio of the video frames without rescaling the pixel data.

**Source:** [libavfilter/vf_aspect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_aspect.c)

The `setsar` filter changes the Sample Aspect Ratio (SAR) metadata of video frames without modifying the actual pixel data. SAR describes the shape of individual pixels (e.g., square pixels have SAR 1:1, while anamorphic SD video often has non-square pixels). Use `setsar` to correct incorrectly tagged SAR metadata, to signal square pixels after a resize operation, or to prepare anamorphic content for display. The companion filter `setdar` sets the Display Aspect Ratio instead.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "setsar=1:1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sar (ratio, r) | string | — | The desired sample aspect ratio as a fraction (e.g., `1:1`, `16:15`, `64:45`). |
| max | int | `100` | Maximum value for numerator or denominator in the simplified ratio. |

## Examples

### Reset SAR to square pixels (1:1)

Mark the output as having square pixels, which is the standard for most modern video.

```sh
ffmpeg -i input.mp4 -vf "setsar=1:1" output.mp4
```

### Set SAR for PAL 16:9 anamorphic

Tag widescreen SD video with the appropriate non-square pixel ratio.

```sh
ffmpeg -i input.mpg -vf "setsar=64:45" output.mp4
```

### Fix incorrectly tagged SAR after scaling

After scaling a video, reset SAR to 1:1 to ensure correct display.

```sh
ffmpeg -i input.mp4 -vf "scale=1280:720,setsar=1:1" output.mp4
```

### Use rational expression

Specify the ratio as a division expression.

```sh
ffmpeg -i input.mp4 -vf "setsar=ratio=16/15" output.mp4
```

## Notes

- `setsar` only modifies metadata; it does not resample or rescale any pixel data. If you need actual pixel changes to match a new aspect ratio, use `scale` instead.
- The `scale` filter automatically adjusts SAR to maintain the display aspect ratio when resizing; you usually only need `setsar` to override or correct that metadata afterward.
- Display Aspect Ratio (DAR) = SAR * (width / height). Use `setdar` to set the DAR directly if that is more convenient.
- Many encoders and muxers reset SAR to 1:1 unless explicitly told otherwise; check the output with `ffprobe` to confirm the metadata was written correctly.

---

### signalstats

> Compute broadcast-standard signal quality metrics (Y/U/V min/max/avg, saturation, hue) for each frame and output them as metadata.

**Source:** [libavfilter/vf_signalstats.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_signalstats.c)

The `signalstats` filter computes per-frame statistics about the video signal — luma (Y), chroma (U/V), saturation, and hue levels — and attaches them as `lavfi.signalstats.*` frame metadata. It is designed for digitization QC of analog video and can also visually highlight out-of-range pixels. The statistics are output to the FFmpeg log and can be captured with tools like `ffprobe`.

## Quick Start

```sh
# Print signal stats for every frame
ffmpeg -i input.mp4 -vf "signalstats" -f null - 2>&1 | grep signalstats
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stat | flags | (none) | Additional statistics to compute: `tout` (temporal outliers), `vrep` (vertical line repetition), `brng` (out-of-range values). |
| out | int | (none) | Highlight filter: `tout`, `vrep`, or `brng`. Marks detected pixels in the output frame. |
| color / c | color | `yellow` | Color used to highlight detected pixels when `out` is set. |

## Metadata Fields

| Field | Range | Description |
|-------|-------|-------------|
| YMIN, YMAX | 0–255 | Min/max luma value |
| YLOW, YHIGH | 0–255 | Luma at 10th/90th percentile |
| YAVG | 0–255 | Average luma |
| UMIN–UMAX, VMIN–VMAX | 0–255 | Min/max chroma |
| SATMIN–SATMAX | 0–181 | Min/max saturation |
| HUEMED, HUEAVG | 0–360 | Median/average hue |
| YDIF, UDIF, VDIF | 0–255 | Frame-to-frame difference per plane |

## Examples

### Dump all frame stats to CSV

```sh
ffprobe -f lavfi -i "movie=input.mp4,signalstats" \
  -show_frames -select_streams v \
  -print_format csv -show_entries frame_tags=lavfi.signalstats.YAVG \
  > luma_avg.csv
```

### Highlight out-of-range pixels visually

```sh
ffmpeg -i input.mp4 -vf "signalstats=out=brng:color=red" output.mp4
```

### Check temporal outliers (noise spikes)

```sh
ffmpeg -i input.mp4 -vf "signalstats=stat=tout:out=tout" output.mp4
```

### QC check: find frames with illegal luma levels

```sh
ffprobe -f lavfi -i "movie=input.mp4,signalstats" \
  -show_frames -select_streams v \
  -show_entries frame_tags=lavfi.signalstats.YMIN,lavfi.signalstats.YMAX 2>/dev/null
```

## Notes

- Legal broadcast luma range is 16–235 (8-bit); `brng` detects pixels outside the 0–255 nominal range (i.e. super-black or super-white).
- `vrep` (vertical line repetition) detects tape dropout artifacts common in VHS/Betamax digitization.
- `tout` (temporal outliers) detects pixels that differ dramatically from the previous frame — a sign of noise or tape damage.
- All statistics are attached to frames as `lavfi.signalstats.*` metadata; use `ffprobe -show_frames` to extract them to CSV or JSON.

---

### smartblur

> Blur video without affecting edges and outlines, with separate control over luma, chroma, and alpha planes.

**Source:** [libavfilter/vf_smartblur.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_smartblur.c)

The `smartblur` filter blurs video while intelligently preserving edges and outlines. Unlike a simple Gaussian blur, it uses a threshold to selectively blur flat areas while leaving edges sharp — or, with negative strength values, sharpen detail. Separate parameters control the luma and chroma planes independently.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "smartblur=luma_radius=1.5:luma_strength=0.8" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_radius / lr | float | `1.0` | Gaussian blur radius for luma (Y). Range: 0.1–5.0. Larger = slower. |
| luma_strength / ls | float | `1.0` | Luma blur strength. 0–1 blurs, -1–0 sharpens. |
| luma_threshold / lt | int | `0` | Luma threshold (-30–30). 0 = filter all; positive = flat areas only; negative = edges only. |
| chroma_radius / cr | float | (luma_radius) | Gaussian blur radius for chroma. Defaults to luma_radius. |
| chroma_strength / cs | float | (luma_strength) | Chroma blur strength. Defaults to luma_strength. |
| chroma_threshold / ct | int | (luma_threshold) | Chroma threshold. Defaults to luma_threshold. |
| alpha_radius / ar | float | (luma_radius) | Gaussian blur radius for alpha plane. |
| alpha_strength / as | float | (luma_strength) | Alpha blur strength. |
| alpha_threshold / at | int | (luma_threshold) | Alpha threshold. |

## Examples

### Gentle content-aware blur (skin smoothing)

Blur flat areas while keeping edges crisp.

```sh
ffmpeg -i portrait.mp4 -vf "smartblur=lr=1.5:ls=0.8:lt=10" output.mp4
```

### Sharpen detail while blurring noise

Negative luma strength sharpens edges; threshold focuses on edges.

```sh
ffmpeg -i soft.mp4 -vf "smartblur=lr=1.0:ls=-0.5:lt=-3" output.mp4
```

### Blur only chroma (reduce color noise)

Keep luma sharp, blur only color channels.

```sh
ffmpeg -i noisy.mp4 -vf "smartblur=lr=0:ls=0:cr=2.0:cs=0.8" output.mp4
```

### Strong denoise for flat areas only

Threshold of 20 means only very flat areas get blurred.

```sh
ffmpeg -i input.mp4 -vf "smartblur=lr=3.0:ls=1.0:lt=20" output.mp4
```

## Notes

- `luma_strength` in [0.0, 1.0] blurs; in [-1.0, 0.0] sharpens. Values outside these ranges are clamped.
- `luma_threshold` = 0 applies blur everywhere; positive values target flat areas (good for noise reduction); negative values target edges (good for sharpening).
- If chroma/alpha options are not set, they inherit the corresponding luma value.
- For pure sharpening use `unsharp` which gives more control; `smartblur` excels at content-aware noise reduction.

---

### split

> Duplicate the input video stream into N identical output streams for use in branching filtergraphs.

**Source:** [libavfilter/split.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/split.c)

The `split` filter takes a single input video stream and produces N identical copies of it. This is essential in filtergraph pipelines where the same source needs to feed multiple downstream filters simultaneously — for example, creating a preview thumbnail alongside the main encode, or constructing a side-by-side comparison. The audio equivalent is `asplit`. The default number of outputs is 2.

## Quick Start

```sh
ffmpeg -i input.mp4 -filter_complex "[0:v]split[a][b]; [a]scale=640:360[small]; [b]scale=1920:1080[large]" \
  -map "[small]" small.mp4 -map "[large]" large.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outputs | int | `2` | Number of output streams to produce. |

## Examples

### Split into two outputs for multi-resolution encoding

Decode once and encode to two different resolutions simultaneously.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[a][b]; [a]scale=1280:720[hd]; [b]scale=640:360[sd]" \
  -map "[hd]" hd.mp4 \
  -map "[sd]" sd.mp4
```

### Split and apply different filters to each branch

Apply different filters (e.g., grayscale and original) to two copies of the same stream.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][gray]; [gray]hue=s=0[bw]" \
  -map "[orig]" color.mp4 \
  -map "[bw]" bw.mp4
```

### Split into three outputs

Specify the count explicitly when you need more than two branches.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split=3[a][b][c]; [a]scale=1920:1080[fhd]; [b]scale=1280:720[hd]; [c]scale=640:360[sd]" \
  -map "[fhd]" fhd.mp4 -map "[hd]" hd.mp4 -map "[sd]" sd.mp4
```

### Crop one branch and stack side by side

Use split to create a side-by-side comparison between original and cropped versions.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][tocrop]; [tocrop]crop=iw/2:ih:0:0[cropped]; [orig][cropped]hstack" \
  output.mp4
```

## Notes

- Each output branch receives reference-counted frames from the same decoded source, so `split` does not significantly increase memory usage for read-only operations.
- When downstream branches apply different filters, each branch may buffer frames independently, which can increase memory for high-resolution or long-GOP content.
- The audio equivalent, `asplit`, works identically for audio streams.
- `split` is required in filtergraph syntax; simply connecting one pad to two different filters is not valid — you must use `split` explicitly.

---

### ssim

> Calculate the Structural Similarity Index (SSIM) between two video streams as a perceptual quality metric.

**Source:** [libavfilter/vf_ssim.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_ssim.c)

The `ssim` filter computes the Structural Similarity Index Measure (SSIM) between two video streams — typically an original and a processed/compressed copy. SSIM is a perceptual quality metric that models human visual perception better than PSNR by comparing luminance, contrast, and structure. It produces values between 0 and 1, where 1 is identical and values above 0.95 are generally considered high quality.

## Quick Start

```sh
# Compare original and encoded; print SSIM to stderr
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file / f | string | — | File path to write per-frame SSIM statistics. Prints summary to stderr if omitted. |

## Examples

### Print SSIM to stderr

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim" -f null -
```

### Save per-frame SSIM values to a file

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v][1:v]ssim=stats_file=ssim.log" -f null -
```

### Compare two codec settings side by side

```sh
# Encode at two quality levels
ffmpeg -i original.mp4 -c:v libx264 -crf 23 crf23.mp4
ffmpeg -i original.mp4 -c:v libx264 -crf 35 crf35.mp4

# Compare both against original
ffmpeg -i original.mp4 -i crf23.mp4 -filter_complex "[0:v][1:v]ssim=f=ssim_23.log" -f null -
ffmpeg -i original.mp4 -i crf35.mp4 -filter_complex "[0:v][1:v]ssim=f=ssim_35.log" -f null -
```

### Compute SSIM and PSNR in a single pass

```sh
ffmpeg -i original.mp4 -i encoded.mp4 \
  -filter_complex "[0:v]split[a][b];[1:v]split[c][d];[a][c]psnr;[b][d]ssim" \
  -f null -
```

## Notes

- SSIM values: 1.0 = identical, >0.95 = high quality, 0.90–0.95 = acceptable, <0.90 = noticeable degradation.
- SSIM is generally more aligned with human perception than PSNR, especially for compression artifacts and blur.
- The first input (`[0:v]`) is the reference; the second (`[1:v]`) is the test stream. The first stream passes through unchanged to the output.
- Use `-f null -` as the output to discard the video and only collect statistics.

---

### tblend

> Blend consecutive video frames together using compositing modes for motion blur and temporal effects.

**Source:** [libavfilter/vf_blend.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_blend.c)

The `tblend` filter is the temporal variant of `blend`: it blends each frame with the previous frame from the same stream. This creates motion blur, ghosting, or temporal smoothing effects without requiring a second input. It accepts the same modes as `blend`.

## Quick Start

```sh
# Temporal frame blending (motion blur effect)
ffmpeg -i input.mp4 -vf "tblend=all_mode=average:all_opacity=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_mode | int | `normal` | Blend mode applied to all components. See `blend` for the full mode list. |
| all_opacity | float | `1.0` | Opacity of the blend. 0=show only current frame, 1=fully blended with previous. |
| all_expr | string | — | Custom expression. Variables include `A` (current frame) and `B` (previous frame). |
| c0_mode | int | — | Mode for component 0. |
| c1_mode | int | — | Mode for component 1. |
| c2_mode | int | — | Mode for component 2. |

### Available blend modes

Same as `blend`: `normal`, `addition`, `average`, `burn`, `darken`, `difference`, `divide`, `dodge`, `exclusion`, `hardlight`, `hardmix`, `lighten`, `linearlight`, `multiply`, `negation`, `or`, `overlay`, `pinlight`, `reflect`, `screen`, `softlight`, `subtract`, `vividlight`, `xor`, and others.

## Examples

### Smooth motion blur (average of current and previous frame)

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=average" output.mp4
```

### Ghost/smear effect with overlay mode

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=overlay:all_opacity=0.4" output.mp4
```

### Temporal difference (highlight changed pixels)

Produces a motion-detection-style output where still areas are black.

```sh
ffmpeg -i input.mp4 -vf "tblend=all_mode=difference" output.mp4
```

### Reduce flicker with soft temporal averaging

```sh
ffmpeg -i flickery.mp4 -vf "tblend=all_mode=average:all_opacity=0.3" output.mp4
```

## Notes

- `tblend` operates on a single stream; `blend` composites two separate streams. They share the same mode options.
- `all_mode=average` is the most useful for motion blur: each output pixel is the mean of the current and previous frame pixel at the same location.
- `all_opacity` controls how much of the previous frame contributes. At 0.5 with `normal` mode, you get a 50/50 mix; at 1.0, the previous frame completely replaces the current.
- For high-quality frame interpolation (not simple blending), see `minterpolate`.

---

### thumbnail

> Select the most visually representative frame from each batch of N consecutive frames.

**Source:** [libavfilter/vf_thumbnail.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_thumbnail.c)

The `thumbnail` filter analyzes batches of consecutive frames and selects the single most representative frame from each batch, discarding the rest. Representativeness is determined by histogram analysis — the frame whose histogram most closely resembles the mean of the batch is chosen. This makes it ideal for generating accurate thumbnails or preview images from video files. Combine it with `scale` and `-frames:v 1` to extract a single thumbnail image.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "thumbnail,scale=320:180" -frames:v 1 thumb.jpg
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| n | int | `100` | Number of frames per batch. One frame is selected per batch. |
| log | int | `info` | Logging level for displaying selected frame statistics. |

## Examples

### Extract a single representative thumbnail

Analyze the entire video (or at least the first batch of 100 frames) and save the best frame as a JPEG.

```sh
ffmpeg -i input.mp4 -vf "thumbnail,scale=320:180" -frames:v 1 thumb.jpg
```

### Finer-grained thumbnail grid (every 50 frames)

Set `n=50` to get a representative frame from each 50-frame window, producing more thumbnails for longer videos.

```sh
ffmpeg -i input.mp4 -vf "thumbnail=50,scale=160:90" -vsync vfr thumbs_%04d.jpg
```

### High-quality PNG thumbnail

Extract the representative frame at full resolution as a lossless PNG.

```sh
ffmpeg -i input.mp4 -vf "thumbnail=200" -frames:v 1 thumb.png
```

### Thumbnail with time offset

Start from 30 seconds into the video before running thumbnail selection to avoid opening-credit frames.

```sh
ffmpeg -ss 30 -i input.mp4 -vf "thumbnail=100,scale=640:360" -frames:v 1 thumb.jpg
```

## Notes

- Larger `n` values analyze more frames per batch, improving representativeness, but require proportionally more memory since all frames in the batch are buffered.
- When combined with `-frames:v 1`, only the first selected frame (from the first batch) is saved. Remove this flag to collect one thumbnail per batch across the whole video.
- The filter selects an existing frame, not an average; the output is always an actual decoded video frame.
- For fast, rough thumbnails, seeking to a fixed timestamp (`-ss`) is faster; `thumbnail` is better when you need a content-aware selection.

---

### tile

> Arrange consecutive video frames into a tiled grid layout in a single output frame.

**Source:** [libavfilter/vf_tile.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_tile.c)

The `tile` filter arranges consecutive input frames into a grid, producing a single output frame that contains a mosaic of multiple frames. It is useful for creating contact sheets, thumbnail previews, or visualizing temporal information across multiple frames at once.

## Quick Start

```sh
# Create a 4x3 grid of frames
ffmpeg -i input.mp4 -vf "tile=4x3" -frames:v 1 thumbnail.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| layout | image_size | `6x5` | Grid dimensions as `columns x rows`. |
| nb_frames | int | `0` | Total number of frames to tile. 0 = columns × rows. |
| margin | int | `0` | Outer border in pixels around the entire grid. |
| padding | int | `0` | Spacing between individual tiles in pixels. |
| color | color | `black` | Fill colour for unused grid cells and padding/margin. |
| overlap | int | `0` | Number of tiles to overlap (reuse) from the previous frame. |
| init_padding | int | `0` | Number of empty tiles to add at the start. |

## Examples

### One-frame contact sheet (4×3 grid)

Sample one frame every N frames to get 12 evenly-spaced thumbnails.

```sh
ffmpeg -i input.mp4 -vf "fps=1/10,tile=4x3" -frames:v 1 sheet.png
```

### Animated tile showing every 4 frames

Update the grid every 4 frames.

```sh
ffmpeg -i input.mp4 -vf "tile=2x2" output.mp4
```

### Add padding and margin

```sh
ffmpeg -i input.mp4 -vf "fps=1,tile=3x3:margin=5:padding=3:color=white" -frames:v 1 sheet.jpg
```

### Thumbnail strip for video scrubbing

One row of 10 thumbnails.

```sh
ffmpeg -i input.mp4 -vf "fps=1/5,scale=160:-1,tile=10x1" -frames:v 1 strip.png
```

## Notes

- `tile` collects input frames and outputs one grid frame after every `nb_frames` input frames. With `nb_frames=12` (4×3), it emits one grid output for every 12 input frames.
- Combine with `fps=1/N` or `select` to extract evenly-spaced frames before tiling, rather than tiling every frame.
- The output frame size is `(input_width × columns) + (padding × (columns-1)) + (margin × 2)` — watch for very large output sizes with high-resolution inputs.
- Use `-frames:v 1` to extract just one grid image from the start of the stream.

---

### tonemap

> Apply tone mapping to convert between different dynamic ranges, including HDR to SDR conversion.

**Source:** [libavfilter/vf_tonemap.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_tonemap.c)

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

---

### tpad

> Add padding frames at the start or end of a video stream — either solid-color frames or clones of the first/last frame.

**Source:** [libavfilter/vf_tpad.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_tpad.c)

The `tpad` filter adds temporal padding to a video stream — inserting extra frames at the beginning (to delay the start) or at the end (to extend it). It can add solid-color frames or clone the first/last frame, and supports both frame counts and duration-based specifications. This is useful for synchronizing streams, creating freeze frames, or adding holds before/after the content.

## Quick Start

```sh
# Add 30 black frames before the video
ffmpeg -i input.mp4 -vf "tpad=start=30" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | int | `0` | Number of frames to prepend. |
| stop | int | `0` | Number of frames to append (-1 = pad indefinitely). |
| start_mode | int | `add` | Mode for prepended frames: `add` (solid color) or `clone` (repeat first frame). |
| stop_mode | int | `add` | Mode for appended frames: `add` (solid color) or `clone` (repeat last frame). |
| start_duration | duration | `0` | Duration to prepend (overrides `start`). E.g. `1.5` or `00:00:01.500`. |
| stop_duration | duration | `0` | Duration to append (overrides `stop`). |
| color | color | `black` | Color for `add`-mode frames. |

## Examples

### Add 1 second of black before video

```sh
ffmpeg -i input.mp4 -vf "tpad=start_duration=1:color=black" output.mp4
```

### Freeze-frame hold: clone first frame for 2 seconds

```sh
ffmpeg -i input.mp4 -vf "tpad=start=48:start_mode=clone" output.mp4
```

### Hold last frame for 3 seconds at end

```sh
ffmpeg -i input.mp4 -vf "tpad=stop_duration=3:stop_mode=clone" output.mp4
```

### Pad both ends with white

```sh
ffmpeg -i input.mp4 -vf "tpad=start_duration=0.5:stop_duration=0.5:color=white" output.mp4
```

### Pad audio stream to match video length

```sh
ffmpeg -i input.mp4 -vf "tpad=stop=-1:stop_mode=clone" -af "apad" output.mp4
```

## Notes

- `stop=-1` pads indefinitely — useful when you need to synchronize video length with a longer audio track; always pair with a time limit (e.g. `-t` or `-to`).
- `clone` mode repeats the actual first/last frame content, creating a freeze-frame effect. `add` mode inserts a solid-color frame.
- `start_duration` and `stop_duration` override `start`/`stop` when non-zero, and accept FFmpeg's standard time duration syntax.
- For audio padding use the `apad` audio filter in the same pipeline.

---

### transpose

> Transpose rows and columns in the input video to rotate 90 degrees and optionally flip.

**Source:** [libavfilter/vf_transpose.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_transpose.c)

The `transpose` filter swaps the rows and columns of each video frame to achieve 90-degree rotations combined with optional flipping. It is the preferred method for rotating video by exactly 90 or 270 degrees because it operates as a simple pixel rearrangement with no interpolation, unlike the general `rotate` filter. The `passthrough` option lets you skip the operation when the input is already in the desired orientation.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dir | int | `0` (cclock_flip) | Transposition direction (see values below). |
| passthrough | int | `none` | Skip transposition if input geometry matches: `none`, `portrait`, or `landscape`. |

### `dir` values

| Value | Name | Effect |
|-------|------|--------|
| `0` / `cclock_flip` | Counter-clockwise + vertical flip | 90° CCW then flip vertically |
| `1` / `clock` | Clockwise | 90° clockwise |
| `2` / `cclock` | Counter-clockwise | 90° counter-clockwise |
| `3` / `clock_flip` | Clockwise + vertical flip | 90° CW then flip vertically |

## Examples

### Rotate 90 degrees clockwise

Correct portrait video shot on a phone that was held sideways.

```sh
ffmpeg -i input.mp4 -vf "transpose=clock" output.mp4
```

### Rotate 90 degrees counter-clockwise

Undo a clockwise rotation or correct the opposite orientation.

```sh
ffmpeg -i input.mp4 -vf "transpose=cclock" output.mp4
```

### Rotate 180 degrees

Apply `transpose` twice — each clockwise — to achieve a 180-degree rotation.

```sh
ffmpeg -i input.mp4 -vf "transpose=clock,transpose=clock" output.mp4
```

### Rotate only landscape videos, pass portrait through

Use `passthrough=landscape` to skip rotation when the video is already in portrait orientation.

```sh
ffmpeg -i input.mp4 -vf "transpose=dir=clock:passthrough=landscape" output.mp4
```

## Notes

- `transpose` is a pixel-copy operation with no interpolation, so it introduces no quality loss beyond the output encoding.
- The output dimensions are swapped: a 1920x1080 input becomes 1080x1920 after any 90-degree transpose.
- For arbitrary angles, use the `rotate` filter instead.
- On some hardware-accelerated pipelines (e.g., VAAPI, VideoToolbox), there are dedicated rotation options on the encoder that may be faster than software `transpose`.

---

### trim

> Extract a continuous sub-section of the input video by specifying start and end points by time or frame number.

**Source:** [libavfilter/trim.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/trim.c)

The `trim` filter retains one continuous segment of the input video, discarding everything before the start point and everything after the end point. Unlike stream-level seeking (`-ss` / `-t`), `trim` operates at the filter level, which enables accurate frame-level trimming in complex filtergraphs. Note that `trim` does not reset timestamps — chain it with `setpts=PTS-STARTPTS` afterward if you need the output to start at time zero.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "trim=start=10:end=20,setpts=PTS-STARTPTS" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | duration | — | Timestamp of the first frame to keep. |
| end | duration | — | Timestamp of the first frame to drop (exclusive). |
| duration | duration | — | Maximum duration of the output section. |
| start_frame | int64 | — | Frame number (0-based) of the first frame to keep. |
| end_frame | int64 | — | Frame number of the first frame to drop. |
| start_pts | int64 | — | Start timestamp in timebase units. |
| end_pts | int64 | — | End timestamp in timebase units. |

## Examples

### Trim from 10 to 30 seconds

Keep only the segment between 10 and 30 seconds and reset timestamps to start at zero.

```sh
ffmpeg -i input.mp4 -vf "trim=start=10:end=30,setpts=PTS-STARTPTS" output.mp4
```

### Keep only the first 5 seconds

Use `duration` to specify an exact clip length starting from the beginning.

```sh
ffmpeg -i input.mp4 -vf "trim=duration=5,setpts=PTS-STARTPTS" output.mp4
```

### Trim to a specific minute

Equivalent to selecting the second minute of the input (60 to 120 seconds).

```sh
ffmpeg -i input.mp4 -vf "trim=60:120,setpts=PTS-STARTPTS" output.mp4
```

### Frame-accurate trim by frame number

Keep frames 100 through 299 (200 frames total) regardless of timestamps.

```sh
ffmpeg -i input.mp4 -vf "trim=start_frame=100:end_frame=300,setpts=PTS-STARTPTS" output.mp4
```

### Trim in a filtergraph alongside audio

When trimming both video and audio, use `atrim` for the audio stream and synchronize the start points.

```sh
ffmpeg -i input.mp4 \
  -filter_complex \
    "[0:v]trim=start=5:end=15,setpts=PTS-STARTPTS[v]; \
     [0:a]atrim=start=5:end=15,asetpts=PTS-STARTPTS[a]" \
  -map "[v]" -map "[a]" output.mp4
```

## Notes

- `trim` does not alter the PTS values of kept frames. Always chain `setpts=PTS-STARTPTS` after `trim` to produce output that starts at time zero, as many muxers and players expect this.
- When both time-based and frame-based start/end options are set simultaneously, the filter keeps frames that satisfy at least one of the constraints.
- The `end` point is exclusive: the frame with exactly `end` timestamp will not appear in the output.
- For simple segment extraction without filtergraph overhead, stream-level `-ss` and `-t` or `-to` options are faster since they can seek and avoid decoding discarded frames.

---

### unsharp

> Sharpen or blur video using an unsharp mask applied to luma and chroma channels.

**Source:** [libavfilter/vf_unsharp.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_unsharp.c)

The `unsharp` filter applies an unsharp mask to sharpen or blur the input video. Despite the name, positive `luma_amount` values sharpen the image by amplifying the difference between the original and a blurred copy, while negative values produce a net blur. It can operate on luma, chroma, or both channels independently.

## Quick Start

```sh
# Moderate sharpening
ffmpeg -i input.mp4 -vf "unsharp=5:5:1.0" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| luma_msize_x / lx | int | `5` | Luma matrix horizontal size (must be odd). Range: 3–23. |
| luma_msize_y / ly | int | `5` | Luma matrix vertical size (must be odd). Range: 3–23. |
| luma_amount / la | float | `1.0` | Luma sharpening strength. Positive=sharpen, negative=blur. Range: -1.5–1.5. |
| chroma_msize_x / cx | int | `5` | Chroma matrix horizontal size. |
| chroma_msize_y / cy | int | `5` | Chroma matrix vertical size. |
| chroma_amount / ca | float | `0.0` | Chroma sharpening strength. Default 0 leaves chroma unchanged. |
| alpha_msize_x / ax | int | `5` | Alpha matrix horizontal size. |
| alpha_msize_y / ay | int | `5` | Alpha matrix vertical size. |
| alpha_amount / aa | float | `0.0` | Alpha sharpening strength. |

## Examples

### Gentle sharpening

Useful for restoring detail after scaling or compression.

```sh
ffmpeg -i input.mp4 -vf "unsharp=5:5:0.5" output.mp4
```

### Strong sharpening

Aggressive sharpening for very soft or out-of-focus footage.

```sh
ffmpeg -i input.mp4 -vf "unsharp=7:7:1.5" output.mp4
```

### Blur both luma and chroma

Negative amounts produce a blur effect.

```sh
ffmpeg -i input.mp4 -vf "unsharp=5:5:-0.8:5:5:-0.5" output.mp4
```

### Sharpen luma only, leave chroma unchanged

Standard sharpening that avoids colour-noise amplification.

```sh
ffmpeg -i input.mp4 -vf "unsharp=lx=5:ly=5:la=1.0:ca=0.0" output.mp4
```

## Notes

- Matrix sizes must be odd numbers (3, 5, 7, …, 23). Larger matrices produce a wider blur before the difference is computed, affecting low-frequency detail.
- The default `luma_amount=1.0` is noticeable but not extreme; start with 0.5 and increase to taste.
- `chroma_amount=0` (the default) is usually correct: sharpening chroma can amplify colour noise, especially in skin tones.
- For edge-preserving sharpening that avoids amplifying noise, see `smartblur` with a negative `luma_strength`.

---

### vectorscope

> Display a 2D color vectorscope showing the distribution of chroma values, used for broadcast color QC and calibration.

**Source:** [libavfilter/vf_vectorscope.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_vectorscope.c)

The `vectorscope` filter generates a 2D plot of two color components against each other — typically Cb vs. Cr (U vs. V) — creating the classic vectorscope display used in broadcast video production. It reveals color saturation, hue accuracy, and whether colors fall within legal broadcast gamut. Multiple visualization modes provide different ways to inspect the color distribution.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "vectorscope" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode / m | int | `gray` | Display mode: `gray`, `tint`, `color`, `color2`, `color3`, `color4`, `color5`. |
| x | int | `1` | Color component for X axis (0=Y, 1=U/Cb, 2=V/Cr, 3=A). |
| y | int | `2` | Color component for Y axis. |
| intensity / i | float | `0.004` | Brightness of plotted points (used in gray/color/color3/color5 modes). |
| envelope / e | int | `none` | Envelope: `none`, `instant`, `peak`, `peak+instant`. |
| graticule / g | int | `none` | Graticule overlay: `none`, `green`, `color`, `invert`. |
| opacity / o | float | `0.75` | Graticule opacity. |
| bgopacity / b | float | `0.3` | Background opacity. |
| colorspace / c | int | `auto` | Colorspace for graticule targets: `auto`, `601`, `709`. |
| lthreshold / l | float | `0.0` | Low threshold for the 3rd component (ignored below this). |
| hthreshold / h | float | `1.0` | High threshold for the 3rd component (ignored above this). |

## Examples

### Standard Cb/Cr vectorscope

```sh
ffmpeg -i input.mp4 -vf "vectorscope" output.mp4
```

### With color graticule targets (BT.709)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=graticule=color:colorspace=709:opacity=0.9" output.mp4
```

### Show actual pixel colors (color2 mode)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=mode=color2" output.mp4
```

### Peak envelope (hold max saturation)

```sh
ffmpeg -i input.mp4 -vf "vectorscope=envelope=peak" output.mp4
```

### Display alongside original video

```sh
ffmpeg -i input.mp4 -vf "[in]split[a][b];[a]vectorscope[vs];[b][vs]hstack" output.mp4
```

## Notes

- Default X=1 (U/Cb) and Y=2 (V/Cr) gives the standard vectorscope view — dots at center = neutral, saturated colors appear farther from center.
- `graticule=color` overlays the standard broadcast target boxes for primary and secondary colors; dots outside these boxes indicate out-of-gamut chroma.
- `colorspace=709` draws Rec.709 targets (HDTV); `colorspace=601` draws Rec.601 targets (SDTV).
- Use alongside `waveform` for complete broadcast QC: waveform checks luma levels, vectorscope checks chroma.
- `lthreshold`/`hthreshold` filter which pixels contribute based on the 3rd component (luma by default), useful for isolating highlights or shadows.

---

### vflip

> Vertically flip (mirror) each frame of the input video.

**Source:** [libavfilter/vf_vflip.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_vflip.c)

The `vflip` filter mirrors every frame of the input video along the horizontal axis, producing an upside-down reflection. It has no parameters and is lossless. Common use cases include correcting footage shot with an upside-down camera mount, creating reflection effects, or compositing where a flipped stream is required.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

## Parameters

This filter has no configurable parameters.

## Examples

### Basic vertical flip

Flip the video upside down and re-encode.

```sh
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

### Flip with audio copy

Flip the video while passing the audio through without re-encoding.

```sh
ffmpeg -i input.mp4 -vf "vflip" -c:a copy output.mp4
```

### Create a ground reflection effect

Stack the original video on top of a vertically-flipped copy to simulate a reflection.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[top][bot]; [bot]vflip[flipped]; [top][flipped]vstack" \
  output.mp4
```

### Combine with hflip for 180-degree rotation

Applying both `vflip` and `hflip` is equivalent to a 180-degree rotation.

```sh
ffmpeg -i input.mp4 -vf "vflip,hflip" output.mp4
```

## Notes

- `vflip` is a spatial-only transformation with no resampling, so there is no quality loss from the operation itself.
- Timestamps, audio, and metadata are not modified by this filter.
- For 90-degree rotations use `transpose`; for arbitrary angles use `rotate`.
- When chained with `hflip`, the order does not matter — both combinations produce an identical 180-degree result.

---

### vibrance

> Boost or reduce the saturation of muted colors while protecting already-saturated colors.

**Source:** [libavfilter/vf_vibrance.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_vibrance.c)

The `vibrance` filter boosts or reduces saturation of muted (less saturated) colors more than already-saturated colors, similar to the Vibrance slider in Adobe Lightroom. This preserves naturally saturated elements like skin tones while making dull colours pop. Negative values reduce vibrance, pushing the image toward more muted or monochromatic tones.

## Quick Start

```sh
# Boost vibrance without over-saturating skin tones
ffmpeg -i input.mp4 -vf "vibrance=intensity=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| intensity | float | `0.0` | Vibrance intensity. Range: -2–2. Positive=more vibrant, negative=less. |
| rbal | float | `1.0` | Red balance adjustment. |
| gbal | float | `1.0` | Green balance adjustment. |
| bbal | float | `1.0` | Blue balance adjustment. |
| rlum | float | `0.072` | Red luminance coefficient. |
| glum | float | `0.715` | Green luminance coefficient. |
| blum | float | `0.213` | Blue luminance coefficient. |
| alternate | bool | `0` | Use an alternate vibrance calculation method. |

## Examples

### Subtle vibrance boost for landscape

```sh
ffmpeg -i landscape.mp4 -vf "vibrance=intensity=0.5" output.mp4
```

### Strong vibrance for colourful content

```sh
ffmpeg -i product.mp4 -vf "vibrance=intensity=1.2" output.mp4
```

### Reduce vibrance for muted, filmic look

```sh
ffmpeg -i input.mp4 -vf "vibrance=intensity=-0.5" output.mp4
```

### Combine with hue rotation

```sh
ffmpeg -i input.mp4 -vf "huesaturation=hue=10,vibrance=intensity=0.6" output.mp4
```

## Notes

- `vibrance` differs from `saturation` in that it targets muted colors preferentially. Full saturation (`huesaturation=saturation=1`) boosts all colors equally and can cause skin tones to go orange.
- `intensity=0` is a no-op passthrough; the practical range for normal adjustments is -0.8 to 1.5.
- The `rbal`/`gbal`/`bbal` parameters fine-tune per-channel vibrance balance; leave at defaults unless correcting specific colour channel biases.
- For a complete colour workflow, use `vibrance` after any global exposure/white-balance corrections and before any creative grading.

---

### vignette

> Apply a natural lens vignette effect, darkening the corners and edges of the frame, or reverse an existing vignette.

**Source:** [libavfilter/vf_vignette.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_vignette.c)

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

---

### vstack

> Stack two or more video inputs vertically into a single output frame.

**Source:** [libavfilter/vf_stack.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_stack.c)

The `vstack` filter places multiple video streams one above the other in a single column, producing a taller output frame. All input streams must share the same pixel format and the same width. It is faster than achieving the same result with `overlay` and `pad`, making it the preferred choice for vertical video strip compositions, top-and-bottom comparisons, and stacked camera layouts.

## Quick Start

```sh
ffmpeg -i top.mp4 -i bottom.mp4 -filter_complex "vstack" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams to stack vertically. |
| shortest | bool | `0` | When `1`, stop output when the shortest input ends. |

## Examples

### Stack two videos vertically

Place two videos of the same width one above the other.

```sh
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "vstack" output.mp4
```

### Normalize widths before stacking

Scale both inputs to the same width before stacking if they differ.

```sh
ffmpeg -i top.mp4 -i bottom.mp4 \
  -filter_complex "[0:v]scale=1280:-1[t]; [1:v]scale=1280:-1[b]; [t][b]vstack" \
  output.mp4
```

### Create a reflection effect

Stack the original video on top of a vertically flipped copy to simulate a surface reflection.

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:v]split[orig][copy]; [copy]vflip[flipped]; [orig][flipped]vstack" \
  output.mp4
```

### Stack three inputs vertically

Specify `inputs=3` to stack three streams in a column.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v][2:v]vstack=inputs=3" \
  output.mp4
```

## Notes

- All input streams must have the same width and the same pixel format. Use `scale` and `format` filters to normalize before stacking.
- The output height is the sum of all input heights; the output width equals the shared input width.
- For more than two inputs arranged in a custom grid, use `xstack` instead.
- `vstack` is faster than using `pad` + `overlay` to create the same layout because it does not require compositing.

---

### waveform

> Generate a video waveform monitor overlay for analyzing luma and chroma levels.

**Source:** [libavfilter/vf_waveform.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_waveform.c)

The `waveform` filter generates a video waveform monitor — a tool used in professional video production to analyze the luminance and chrominance levels of a video signal. The waveform shows the distribution of pixel values across each scanline, making it easy to spot clipping, crushing, or color casts. It outputs the waveform overlaid on or beside the video.

## Quick Start

```sh
ffmpeg -i input.mp4 -vf "waveform" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode / m | int | `row` | Waveform orientation: `row` (horizontal) or `column` (vertical). |
| intensity / i | float | `0.04` | Intensity of each plotted point (0.0–1.0). |
| mirror / r | bool | `1` | Mirror the waveform display. |
| display / d | int | `stack` | Output layout: `stack` (waveform below video), `parade` (side by side), `overlay` (waveform over video). |
| components / c | int | `1` | Which components to show. Bitmask: 1=Y, 2=Cb, 4=Cr, 7=all. |
| envelope / e | int | `none` | Envelope mode: `none`, `instant`, `peak`, `peak+instant`. |
| filter / f | int | `lowpass` | Filter type: `lowpass`, `flat`, `aflat`, `chroma`, `color`, `acolor`. |
| graticule / g | int | `none` | Graticule overlay: `none`, `green`, `orange`, `invert`. |
| opacity / o | float | `0.75` | Opacity of the graticule. |
| bgopacity / b | float | `0.75` | Background opacity. |
| flags / fl | flags | `0` | Flags: `torchlight` (show all planes at once). |

## Examples

### Standard luma waveform

```sh
ffmpeg -i input.mp4 -vf "waveform" output.mp4
```

### Parade mode (all three components side by side)

```sh
ffmpeg -i input.mp4 -vf "waveform=display=parade:components=7" output.mp4
```

### Overlay waveform on video

```sh
ffmpeg -i input.mp4 -vf "waveform=display=overlay:intensity=0.1" output.mp4
```

### Graticule with green markers

```sh
ffmpeg -i input.mp4 -vf "waveform=graticule=green:opacity=0.9" output.mp4
```

## Notes

- In `row` mode, each vertical column of the waveform corresponds to the same horizontal position in the video, making it easy to identify left-right color casts.
- `parade` mode displays Y, Cb, and Cr side by side — very useful for identifying white balance and color casts simultaneously.
- Legal broadcast levels are typically 16–235 (luma) and 16–240 (chroma) for 8-bit video. The waveform makes clipping immediately visible.
- For chroma analysis, `vectorscope` is more useful than waveform; use both together for complete broadcast QC.

---

### xfade

> Apply a cross-fade transition effect between two video streams.

**Source:** [libavfilter/vf_xfade.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_xfade.c)

The `xfade` filter creates smooth transition effects between two video streams. It takes two inputs and blends them using one of many built-in transition types (wipes, fades, slides, etc.) or a custom expression. The `offset` parameter controls when the transition starts relative to the first input, and `duration` controls how long it lasts.

## Quick Start

```sh
# Simple crossfade between two clips
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4" \
  output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transition | int | `fade` | Transition type. See the list below. |
| duration | duration | `1s` | Duration of the transition in seconds. |
| offset | duration | `0s` | Time offset (from the start of the first input) when the transition begins. |
| expr | string | — | Custom transition expression. Used when `transition=custom`. Variables: `X`, `Y`, `W`, `H`, `A`, `B`, `P` (progress 0–1). |

### Available transition types

`fade`, `fadeblack`, `fadewhite`, `fadegrays`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `wipetl`, `wipetr`, `wipebl`, `wipebr`, `slideleft`, `slideright`, `slideup`, `slidedown`, `smoothleft`, `smoothright`, `smoothup`, `smoothdown`, `circlecrop`, `rectcrop`, `circleopen`, `circleclose`, `vertopen`, `vertclose`, `horzopen`, `horzclose`, `dissolve`, `pixelize`, `diagtl`, `diagtr`, `diagbl`, `diagbr`, `hlslice`, `hrslice`, `vuslice`, `vdslice`, `hblur`, `radial`, `squeezeh`, `squeezev`, `zoomin`, `distance`, `fadefast`, `fadeslow`

## Examples

### Crossfade at 4-second mark of a 5-second clip

The transition starts 4 s into clip1, lasts 1 s.

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=1:offset=4" \
  output.mp4
```

### Wipe left transition

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=wipeleft:duration=0.5:offset=3" \
  output.mp4
```

### Chain multiple transitions between three clips

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 \
  -filter_complex "[0:v][1:v]xfade=fade:1:4[ab];[ab][2:v]xfade=wipeleft:1:8[out]" \
  -map "[out]" output.mp4
```

### Custom transition expression (horizontal wipe with easing)

```sh
ffmpeg -i clip1.mp4 -i clip2.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=custom:duration=1:offset=3:expr='if(gt(X/W,P),A,B)'" \
  output.mp4
```

## Notes

- `offset` is the timestamp in the first stream when the transition begins. Set it to `(duration_of_clip1 - transition_duration)` for the transition to finish exactly when clip1 ends.
- Both input streams must have the same frame size and pixel format. Use `scale` and `format` if needed.
- When chaining multiple clips with transitions, each `xfade` node in the `filter_complex` needs its own `offset` — account for the reduced duration due to previous transitions.
- The `expr` custom transition uses `P` (progress 0→1), `A` (first input pixel), `B` (second input pixel), `X`/`Y` (pixel coordinates), `W`/`H` (dimensions).

---

### xstack

> Stack multiple video inputs into a custom 2D grid or layout within a single output frame.

**Source:** [libavfilter/vf_stack.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_stack.c)

The `xstack` filter arranges multiple video streams into a freely configurable 2D layout within a single output frame. Unlike `hstack` and `vstack`, which only support single rows or columns, `xstack` can create grids, irregular arrangements, and any combination of positions using a coordinate-based layout syntax. For two inputs the default is a 2x1 side-by-side layout; for all other counts a `layout` or `grid` must be explicitly specified.

## Quick Start

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:grid=2x2" \
  output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | `2` | Number of input streams. Overridden by `grid` when `grid` is set. |
| layout | string | — | Custom position specification for each input, pipe-separated. Format: `col_expr_row_expr` (e.g., `0_0\|w0_0\|0_h0\|w0_h0`). |
| grid | image_size | — | Fixed grid size in `COLUMNSxROWS` format (e.g., `2x2`). Mutually exclusive with `layout`. |
| shortest | bool | `0` | Terminate when the shortest input ends. |
| fill | string | `none` | Color used for unused pixels in the output frame. Default `none` leaves them undefined. |

### Layout syntax

In the `layout` option, each input's position is `col_expr_row_expr` where expressions can use:
- `wN` — width of input N
- `hN` — height of input N
- `+` to sum multiple values (e.g., `w0+w1`)

## Examples

### 2x2 grid from four inputs

Arrange four streams in a 2-column, 2-row grid.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:grid=2x2" \
  output.mp4
```

### Custom layout (manual positions)

Place four inputs in a 2x2 arrangement using explicit layout coordinates.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" \
  output.mp4
```

### 3x3 grid for nine camera feeds

Create a 3-column, 3-row surveillance-style monitor layout.

```sh
ffmpeg -i 1.mp4 -i 2.mp4 -i 3.mp4 -i 4.mp4 -i 5.mp4 -i 6.mp4 -i 7.mp4 -i 8.mp4 -i 9.mp4 \
  -filter_complex \
    "[0:v][1:v][2:v][3:v][4:v][5:v][6:v][7:v][8:v]xstack=inputs=9:grid=3x3" \
  output.mp4
```

### Vertical strip (1x4)

Stack four streams in a single column using a custom layout.

```sh
ffmpeg -i a.mp4 -i b.mp4 -i c.mp4 -i d.mp4 \
  -filter_complex \
    "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|0_h0|0_h0+h1|0_h0+h1+h2" \
  output.mp4
```

## Notes

- All inputs must share the same pixel format; normalize with `format` if needed. For `grid`, inputs within each row must also share the same height, and all rows must share the same width.
- Use `fill=black` (or any color) to fill gaps that appear when inputs have different sizes.
- `layout` and `grid` are mutually exclusive — specifying both results in an error.
- For simple two-input side-by-side or top-bottom layouts, `hstack` and `vstack` are simpler alternatives and have the same performance.

---

### yadif

> Deinterlace video using the 'Yet Another Deinterlacing Filter' with spatial and temporal analysis.

**Source:** [libavfilter/vf_yadif.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_yadif.c)

The `yadif` filter ("Yet Another Deinterlacing Filter") removes interlacing artifacts from video by blending or reconstructing missing lines using spatial and temporal information from adjacent frames. It is the most commonly used deinterlacing filter in FFmpeg, offering a good balance of quality and speed. For higher quality, see `bwdif`.

## Quick Start

```sh
ffmpeg -i interlaced.mp4 -vf "yadif" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `0` | Output mode: `0`=send_frame (one output per input frame), `1`=send_field (one output per field, doubles frame rate), `2`=send_frame_nospatial (skip spatial check), `3`=send_field_nospatial. |
| parity | int | `-1` | Field parity: `0`=top field first (tff), `1`=bottom field first (bff), `-1`=auto-detect (recommended). |
| deint | int | `0` | Which frames to deinterlace: `0`=all frames, `1`=only frames marked as interlaced. |

## Examples

### Basic deinterlacing (one output frame per input frame)

```sh
ffmpeg -i interlaced.mp4 -vf "yadif=0" output.mp4
```

### Double-rate deinterlacing (one frame per field)

Outputs twice as many frames; useful for producing smooth 50/60fps from 25/30i.

```sh
ffmpeg -i interlaced.mp4 -vf "yadif=1" output.mp4
```

### Deinterlace only flagged interlaced frames

Pass progressive frames through unchanged.

```sh
ffmpeg -i mixed.mp4 -vf "yadif=deint=1" output.mp4
```

### Deinterlace with explicit top-field-first parity

```sh
ffmpeg -i interlaced.ts -vf "yadif=mode=0:parity=0" output.mp4
```

## Notes

- `mode=0` (send_frame) is the standard choice: it outputs the same number of frames as the input, with each interlaced frame reconstructed into one progressive frame.
- `mode=1` (send_field) outputs one frame per field, doubling the frame rate. Use with `-r` or `fps` to set the output frame rate.
- When `parity=-1` (auto), yadif reads the field order from the container metadata. If the interlacing is undetected, set it explicitly with `parity=0` (tff) or `parity=1` (bff).
- For broadcast material or high-quality deinterlacing, `bwdif` produces better motion rendering, especially on fast motion.

---

### zoompan

> Apply a Ken Burns-style zoom and pan effect, animating position and zoom level across still or video frames.

**Source:** [libavfilter/vf_zoompan.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_zoompan.c)

The `zoompan` filter applies a zoom and/or pan animation to each input frame, producing multiple output frames from a single source frame. This creates the classic "Ken Burns effect" — slow zooms into photos or video frames with a simultaneous panning motion. All parameters (`z`, `x`, `y`, `d`) accept per-frame expressions, giving full control over the trajectory. It is commonly used in photo slideshows, documentary-style edits, and motion graphics.

## Quick Start

```sh
ffmpeg -i input.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125:s=hd720" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| zoom (z) | string (expr) | `1` | Zoom level expression. Range is 1.0 (no zoom) to 10.0. |
| x | string (expr) | `0` | Horizontal position of the top-left corner of the view within the input frame. |
| y | string (expr) | `0` | Vertical position of the top-left corner of the view within the input frame. |
| d | string (expr) | `90` | Duration in output frames for each input frame. |
| s | image_size | `hd720` | Output frame size (e.g., `hd720`, `1280x720`). |
| fps | video_rate | `25` | Output frame rate. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `iw` / `in_w` | Input frame width |
| `ih` / `in_h` | Input frame height |
| `ow` / `out_w` | Output frame width |
| `oh` / `out_h` | Output frame height |
| `zoom` | Last calculated zoom value for the current input frame |
| `pzoom` | Zoom of the last output frame of the previous input frame |
| `x` / `y` | Last calculated x/y position for the current input frame |
| `px` / `py` | x/y of the last output frame of the previous input frame |
| `in` | Input frame count |
| `on` | Output frame count |
| `duration` | Number of output frames for the current input frame |
| `pduration` | Number of output frames created for the previous input frame |
| `a` | Input width / input height ratio |
| `sar` | Sample aspect ratio |
| `dar` | Display aspect ratio |
| `in_time` / `it` | Input timestamp in seconds |
| `out_time` / `ot` | Output timestamp in seconds |

## Examples

### Slow zoom in, centered

Zoom from 1x to 1.5x over 125 frames while keeping the center of the image in view.

```sh
ffmpeg -i input.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=hd720" output.mp4
```

### Zoom in with pan toward a corner

Simultaneously zoom in and pan toward the top-left region of the image.

```sh
ffmpeg -i input.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=200:x='if(gte(zoom,1.5),x,x+1/a)':y='if(gte(zoom,1.5),y,y+1)':s=1280x720" output.mp4
```

### Ken Burns across a photo slideshow

Apply a different zoom direction to each image in a multi-image slideshow.

```sh
ffmpeg -framerate 1/5 -i photo%03d.jpg \
  -vf "zoompan=z='if(eq(on,1),1,zoom+0.002)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=hd720:fps=25" \
  slideshow.mp4
```

### Zoom in only during the first second of video

Use conditional expression to apply zoom only for the first second (25 frames at 25 fps), then hold.

```sh
ffmpeg -i input.mp4 -vf "zoompan=z='if(between(in_time,0,1),2,1)':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'" output.mp4
```

## Notes

- Each input frame generates `d` output frames; for video input with `d=1`, the filter acts as a per-frame zoom/crop without time expansion.
- The `zoom` and `pzoom` variables let you build smooth transitions between frames by referencing the previous zoom state.
- Large output `d` values applied to video (not stills) will result in very long output — use `d=1` for video and larger values only for still-image inputs.
- The output size `s` should match or be smaller than the input to avoid upscaling artifacts; for best quality, input images should be larger than the output size.

---

## Audio Filters

### acompressor

> Apply dynamic range compression to reduce the difference between loud and quiet parts of an audio stream.

**Source:** [libavfilter/af_sidechaincompress.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_sidechaincompress.c)

The `acompressor` filter reduces the dynamic range of an audio signal by attenuating samples that exceed a configurable threshold. Configurable attack and release times control how quickly the gain reduction is applied and withdrawn, while a makeup gain parameter compensates for the resulting drop in overall loudness. It is widely used in broadcast normalization, podcast processing, and music mastering to achieve a consistent, controlled sound.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "acompressor=threshold=0.089:ratio=9:attack=200:release=1000:makeup=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | 1.0 | Input gain applied before compression. Range: 0.015625–64. |
| mode | int | downward | Compression mode: `downward` (reduce loud peaks) or `upward` (boost quiet signals). |
| threshold | double | 0.125 | Level above which gain reduction begins. Expressed as a linear amplitude (0.00097563–1). For example, 0.125 corresponds to approximately -18 dBFS. |
| ratio | double | 2.0 | Compression ratio. A ratio of 4:1 means that for every 4 dB above the threshold, only 1 dB passes through. Range: 1–20. |
| attack | double | 20.0 | Time in milliseconds the signal must remain above the threshold before gain reduction starts. Range: 0.01–2000. |
| release | double | 250.0 | Time in milliseconds the signal must remain below the threshold before gain reduction is eased off. Range: 0.01–9000. |
| makeup | double | 1.0 | Post-compression gain multiplier to restore loudness. Range: 1–64. |
| knee | double | 2.828 | Width in dB around the threshold where the compression curve is softened. A higher value gives a gentler transition. Range: 1–8. |
| link | int | average | Whether gain reduction is driven by the `average` level across all channels or the `maximum` (loudest) channel. |
| detection | int | rms | How the signal level is measured: `peak` (instantaneous sample) or `rms` (root-mean-square of recent samples). |
| level_sc | double | 1.0 | Gain applied to the sidechain signal (the signal used for level detection when used as a sidechain compressor). |
| mix | double | 1.0 | Blend between the uncompressed (0.0) and fully compressed (1.0) output — enables parallel compression. |

## Examples

### Gentle broadcast compression

A conservative 3:1 ratio with moderate attack and release is suitable for dialogue normalization:

```sh
ffmpeg -i podcast.mp3 -af "acompressor=threshold=0.125:ratio=3:attack=50:release=500:makeup=1.5" output.mp3
```

### Hard limiting (very high ratio)

A 20:1 ratio effectively acts as a limiter, clamping any peak above the threshold:

```sh
ffmpeg -i input.mp3 -af "acompressor=threshold=0.5:ratio=20:attack=5:release=100:makeup=1" output.mp3
```

### Upward compression to boost quiet passages

`mode=upward` raises quiet sections toward the threshold rather than reducing loud ones:

```sh
ffmpeg -i input.mp3 -af "acompressor=mode=upward:threshold=0.25:ratio=4:attack=20:release=200" output.mp3
```

### Parallel compression (New York compression)

Blend a heavily compressed signal with the dry signal at 50% mix:

```sh
ffmpeg -i drums.wav -af "acompressor=threshold=0.1:ratio=10:attack=1:release=50:makeup=4:mix=0.5" output.wav
```

### Sidechain compression (duck music under voice)

Use `filter_complex` to have the compressor react to the voice stream and apply gain reduction to the music stream:

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300[aout]" \
  -map "[aout]" output.mp3
```

## Notes

- The `threshold` parameter uses a linear amplitude scale, not dBFS. To convert: `linear = 10^(dBFS/20)`. For example, -18 dBFS is approximately 0.125.
- Short `attack` values (below ~5 ms) can cause audible distortion on transients; start with 20–50 ms and adjust by ear.
- Setting `makeup` too aggressively after heavy compression can cause downstream clipping — follow with a `volume` or limiter stage if needed.
- When `detection=rms`, the compressor reacts to perceived loudness more smoothly than with `peak`, making it better suited for musical material.
- The `link=average` default is appropriate for stereo material; use `link=maximum` to preserve stereo image on hard-panned sources.

---

### acontrast

> Apply audio contrast enhancement (dynamic range compression/expansion) to make quiet parts louder and loud parts more distinct.

**Source:** [libavfilter/af_acontrast.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_acontrast.c)

The `acontrast` filter applies simple audio contrast enhancement — an automatic gain adjustment that increases the dynamic contrast between loud and quiet passages. It is similar in concept to a waveform shaper: at high `contrast` values it effectively clips and re-shapes the waveform to make audio subjectively louder and more aggressive. It is a quick, single-parameter alternative to a full compander chain.

## Quick Start

```sh
ffmpeg -i input.wav -af "acontrast=contrast=50" enhanced.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| contrast | float | `33.0` | Contrast amount (0–100). Higher values increase aggressiveness. |

## Examples

### Default contrast (moderate enhancement)

```sh
ffmpeg -i quiet.wav -af acontrast louder.wav
```

### Aggressive enhancement (adds "loudness war" style compression)

```sh
ffmpeg -i music.wav -af "acontrast=contrast=80" aggressive.wav
```

### Subtle enhancement for voice clarity

```sh
ffmpeg -i podcast.wav -af "acontrast=contrast=20" podcast_enhanced.wav
```

### Zero contrast (no-op)

```sh
ffmpeg -i input.wav -af "acontrast=contrast=0" output.wav
```

## Notes

- `contrast=0` is a pass-through (no effect); `contrast=100` is maximum enhancement and can introduce distortion.
- At high values, `acontrast` is equivalent to soft clipping/limiting — the waveform is re-shaped, not just amplified.
- For broadcast-standard loudness normalization, use `loudnorm` or `ebur128` instead of `acontrast`.
- Compare with `compand` or `acompressor` for more nuanced dynamics control.

---

### acrusher

> Reduce audio bit depth to create lo-fi, digital distortion effects, with optional LFO modulation and logarithmic mode.

**Source:** [libavfilter/af_acrusher.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_acrusher.c)

The `acrusher` filter simulates the effect of reducing audio bit depth, creating the harsh, quantization-distorted sound characteristic of early digital audio, lo-fi electronics, and video game music. Unlike simply changing the bit depth, it produces the *perceptual* effect while keeping the actual sample depth unchanged. It supports linear and logarithmic quantization, anti-aliasing, DC offset, and optional LFO modulation for dynamic bit-crushing effects.

## Quick Start

```sh
# 8-bit lo-fi effect
ffmpeg -i input.mp3 -af "acrusher=bits=8:mode=lin" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1` | Input gain. |
| level_out | double | `1` | Output gain. |
| bits | double | `8` | Target bit depth. Lower = harsher distortion. |
| mix | double | `0.5` | Blend between crushed and clean signal. |
| mode | int | `lin` | Quantization mode: `lin` (linear) or `log` (logarithmic). |
| dc | double | `1` | DC offset — asymmetric crushing of positive/negative halves. |
| aa | double | `0.5` | Anti-aliasing factor. Higher = smoother, less harsh. |
| samples | double | `1` | Sample rate reduction factor (>1 reduces effective sample rate). |
| lfo | bool | `0` | Enable LFO modulation of bit depth. |
| lforange | double | `20` | LFO modulation depth (in bits). |
| lforate | double | `0.3` | LFO rate in Hz. |

## Examples

### Classic 8-bit game audio

```sh
ffmpeg -i music.wav -af "acrusher=bits=8:mode=lin:aa=0.3" retro.wav
```

### Very lo-fi 4-bit effect

```sh
ffmpeg -i input.wav -af "acrusher=bits=4:mix=0.8" lofi.wav
```

### Logarithmic mode (more natural sounding)

```sh
ffmpeg -i input.wav -af "acrusher=bits=8:mode=log" output.wav
```

### Wobble effect with LFO

```sh
ffmpeg -i input.mp3 -af "acrusher=bits=12:lfo=1:lforange=8:lforate=2" wobble.mp3
```

### Sample rate reduction (adds aliasing)

```sh
ffmpeg -i input.wav -af "acrusher=bits=16:samples=4:aa=0" telephone.wav
```

## Notes

- `mode=log` produces a more "natural" lo-fi sound because human hearing is logarithmic; `lin` gives a harsher, more digital sound.
- `aa` (anti-aliasing) softens the harsh aliasing noise at the cost of some fidelity. `aa=0` gives maximum harshness.
- `samples` reduces the effective sample rate by only updating the output every N samples, adding gritty aliasing artifacts.
- `lfo=1` with moderate `lforange` and `lforate` creates a rhythmic wobbling bit-crush, useful for electronic music effects.
- `mix` blends the effect — `0` = clean original, `1` = fully crushed. Use intermediate values for parallel compression-style blending.

---

### adelay

> Delay one or more audio channels by a specified amount of time or number of samples.

**Source:** [libavfilter/af_adelay.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_adelay.c)

The `adelay` filter shifts individual audio channels in time by a specified delay, padding the beginning with silence. Each channel can have an independent delay value, making it useful for fixing inter-channel timing mismatches, implementing Haas-effect stereo widening, or compensating for microphone placement differences.

## Quick Start

```sh
ffmpeg -i input.wav -af "adelay=500|0" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delays | string | — | Pipe-separated list of delay values for each channel. Append `S` for samples, `s` for seconds, or no suffix for milliseconds. Channels without a specified delay value are left undelayed (unless `all=1`). |
| all | bool | false | When enabled, the last delay value in `delays` is applied to all remaining channels not explicitly listed. |

## Examples

### Delay the left channel by 500 ms (right channel unchanged)

```sh
ffmpeg -i stereo.wav -af "adelay=500|0" output.wav
```

### Delay three channels at different times

Delay the first channel by 1.5 seconds, skip the second (no delay), delay the third by 0.5 seconds:

```sh
ffmpeg -i multichannel.wav -af "adelay=1500|0|500" output.wav
```

### Delay by exact sample counts

Delay the second channel by 500 samples and the third by 700 samples:

```sh
ffmpeg -i input.wav -af "adelay=0|500S|700S" output.wav
```

### Apply the same delay to all channels

Using `all=1` repeats the last specified delay for every remaining channel:

```sh
ffmpeg -i input.wav -af "adelay=delays=64S:all=1" output.wav
```

### Haas effect stereo widening

A short delay of 20–40 ms on one channel creates a perceived stereo widening effect (Haas/precedence effect):

```sh
ffmpeg -i mono.mp3 -af "pan=stereo|c0=c0|c1=c0,adelay=0|30" wide_stereo.mp3
```

## Notes

- Channels with a delay of `0` (or channels for which no delay is provided when `all=0`) pass through with no modification.
- Very long delays allocate a correspondingly large silence buffer in memory; keep delays reasonable for batch or streaming workflows.
- Unlike `aecho`, `adelay` does not add any feedback or repeated reflections — it is a pure one-time time shift.
- When using the `s` (seconds) suffix, the value is a floating-point number of seconds; the `S` (samples) suffix requires an integer.

---

### aecho

> Add echo or reverb-style reflections to an audio stream with configurable delays and decay levels.

**Source:** [libavfilter/af_aecho.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_aecho.c)

The `aecho` filter simulates echoes and reflections by feeding delayed, attenuated copies of the input signal back into the output. Multiple echoes can be stacked by providing pipe-separated delay and decay lists. Use it to add depth to a voice recording, simulate outdoor environments, or create the classic "double-tracking" effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000:0.3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | float | 0.6 | Gain applied to the input signal before processing. Range: (0, 1]. |
| out_gain | float | 0.3 | Gain applied to the output signal after mixing in reflections. Range: (0, 1]. |
| delays | string | 1000 | Pipe-separated list of delay times in milliseconds for each reflection. Each value must be in the range (0, 90000]. |
| decays | string | 0.5 | Pipe-separated list of loudness factors for each reflection. Each value must be in the range (0, 1]. The number of decays must match the number of delays. |

## Examples

### Double-tracking effect (very short delay)

A 60 ms delay creates the impression of two instruments playing in unison:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.88:60:0.4" output.mp3
```

### Metallic robot effect (extremely short delay)

A 6 ms delay creates a metallic or robotic character:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.88:6:0.4" output.mp3
```

### Open-air mountain echo (single long delay)

A 1-second delay at moderate decay simulates an outdoor echo:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000:0.3" output.mp3
```

### Multiple mountain walls (two separate echoes)

Two echoes at different delays and decays simulate reflections from two surfaces:

```sh
ffmpeg -i input.mp3 -af "aecho=0.8:0.9:1000|1800:0.3|0.25" output.mp3
```

### Subtle room reverb (multiple short echoes)

Three rapidly decaying echoes approximate a small room:

```sh
ffmpeg -i input.mp3 -af "aecho=0.6:0.4:20|40|80:0.5|0.3|0.15" output.mp3
```

## Notes

- The sum of `in_gain` and each `decay` multiplied by `out_gain` should not exceed 1.0 to avoid clipping and feedback buildup.
- `delays` and `decays` must have the same number of pipe-separated values; mismatched counts produce an error.
- Very long delays (e.g., 10000 ms or more) allocate a correspondingly large internal buffer; keep memory constraints in mind for embedded or batch pipelines.
- This filter is purely additive — it cannot model complex reverb tails as accurately as convolution-based approaches, but it is very fast and sufficient for stylistic effects.

---

### afade

> Apply a fade-in or fade-out effect to an audio stream with a choice of curve shapes.

**Source:** [libavfilter/af_afade.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_afade.c)

The `afade` filter smoothly ramps audio volume from silence to full (fade-in) or from full to silence (fade-out) over a configurable time range. It supports a wide variety of curve shapes — linear, sinusoidal, logarithmic, exponential, and others — giving precise control over the character of the transition. Use it to open and close clips cleanly or to create professional-sounding intro and outro segments.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type | int | in | Fade direction: `in` (silence to full volume) or `out` (full volume to silence). (alias: `t`) |
| start_sample | int64 | 0 | Sample index at which the fade begins. (alias: `ss`) |
| nb_samples | int64 | 44100 | Number of samples over which the fade is applied. (alias: `ns`) |
| start_time | duration | 0 | Time at which the fade begins. Overrides `start_sample` if set. (alias: `st`) |
| duration | duration | — | Duration of the fade. Overrides `nb_samples` if set. (alias: `d`) |
| curve | int | tri | Shape of the fade curve. Options: `tri` (linear), `qsin` (quarter sine), `hsin` (half sine), `esin` (exponential sine), `log` (logarithmic), `ipar` (inverted parabola), `qua` (quadratic), `cub` (cubic), `squ` (square root), `cbr` (cubic root), `par` (parabola), `exp` (exponential), `iqsin`, `ihsin`, `dese`, `desi`, `losi`, `sinc`, `isinc`, `quat`, `quatr`, `qsin2`, `hsin2`, `nofade`. (alias: `c`) |
| silence | double | 0.0 | Initial gain for fade-in (or final gain for fade-out). Default 0.0 = complete silence. |
| unity | double | 1.0 | Target gain for fade-in (or initial gain for fade-out). Default 1.0 = original volume. |

## Examples

### Fade in over the first 3 seconds

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=3" output.mp3
```

### Fade out over the last 5 seconds of a 60-second clip

```sh
ffmpeg -i input.mp3 -af "afade=t=out:st=55:d=5" output.mp3
```

### Fade in with a logarithmic curve (sounds more natural to the ear)

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=5:curve=log" output.mp3
```

### Apply both a fade-in and fade-out in one command

Chain two `afade` filters — the first fades in over 2 seconds, the second fades out over the last 3 seconds of a 30-second clip:

```sh
ffmpeg -i input.mp3 -af "afade=t=in:st=0:d=2,afade=t=out:st=27:d=3" output.mp3
```

### Fade in the first 15 seconds and fade out the last 25 of a 900-second file

```sh
ffmpeg -i input.mp3 -af "afade=t=in:ss=0:d=15,afade=t=out:st=875:d=25" output.mp3
```

## Notes

- When using `start_time` and `duration` together, both must be set in compatible units (seconds or time duration strings).
- The `curve=tri` (linear) default is perceptually uneven — a linear ramp in amplitude does not sound like a smooth fade to most listeners. `qsin` (quarter sine) or `log` are generally more natural-sounding.
- For sample-accurate editing, use `start_sample` and `nb_samples` rather than `start_time` and `duration`, which depend on accurate timestamps.
- All parameters are available as real-time commands via `sendcmd`, allowing fade automation without re-encoding.

---

### afftdn

> Denoise audio using FFT-based spectral subtraction, supporting white, vinyl, shellac, and custom noise profiles.

**Source:** [libavfilter/af_afftdn.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_afftdn.c)

The `afftdn` filter removes noise from audio using FFT-based spectral subtraction. It models the noise floor spectrum and subtracts it from each frame. It supports several built-in noise type profiles (white, vinyl, shellac) and a custom 15-band profile. The noise floor can be tracked automatically over time for varying noise conditions, making it effective for tape hiss, vinyl crackle, and microphone self-noise reduction.

## Quick Start

```sh
ffmpeg -i noisy.wav -af "afftdn=nr=10:nf=-40" clean.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise_reduction / nr | float | `12` | Noise reduction amount in dB. Range: 0.01–97. |
| noise_floor / nf | float | `-50` | Noise floor in dB. Range: -80 to -20. |
| noise_type / nt | int | `white` | Noise model: `white` (w), `vinyl` (v), `shellac` (s), `custom` (c). |
| band_noise / bn | string | — | Custom 15-band noise profile (space or `\|` separated dB values). |
| residual_floor / rf | float | `-38` | Residual floor in dB after reduction. Range: -80 to -20. |
| track_noise / tn | bool | `0` | Auto-track and adapt the noise floor over time. |
| track_residual / tr | bool | `0` | Auto-track the residual floor. |
| output_mode / om | int | `output` | Output: `input` (passthrough), `output` (denoised), `noise` (only removed noise). |
| adaptivity / ad | float | `0.5` | Gain adaptation speed (0=instant, 1=very slow). |
| gain_smooth / gs | int | `0` | Smooth gain across frequency bins to reduce musical noise. Range: 0–50. |

## Examples

### Remove white noise (microphone self-noise)

```sh
ffmpeg -i mic.wav -af "afftdn=nr=10:nf=-40" clean.wav
```

### Vinyl noise reduction

```sh
ffmpeg -i vinyl.wav -af "afftdn=nt=vinyl:nr=15:nf=-50" clean.wav
```

### Enable noise floor tracking for variable noise

```sh
ffmpeg -i recording.wav -af "afftdn=nr=12:nf=-50:tn=1" output.wav
```

### Monitor what is being removed

```sh
ffmpeg -i noisy.wav -af "afftdn=nr=10:nf=-40:om=noise" noise_only.wav
```

### Reduce musical noise artifacts with gain smoothing

```sh
ffmpeg -i input.wav -af "afftdn=nr=12:nf=-40:gs=10" output.wav
```

## Notes

- Start with conservative settings (`nr=10:nf=-40`) and increase only if noise remains. Excessive reduction causes artifacts ("musical noise").
- `track_noise=1` continuously adapts the noise floor model — useful for recordings with changing background noise.
- `output_mode=noise` lets you hear exactly what is being removed, which helps tune `nr` and `nf` parameters.
- `gain_smooth` reduces the "musical noise" artifact (random tonal remnants) at the cost of some resolution.
- For speech-specific denoising, `arnndn` uses a trained neural network and often produces better results on voice material.

---

### aformat

> Constrain the output audio format to one of a set of allowed sample formats, sample rates, or channel layouts.

**Source:** [libavfilter/af_aformat.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_aformat.c)

The `aformat` filter forces the audio stream to conform to one of the formats you specify. FFmpeg's filter negotiation framework will insert the minimum number of automatic conversions needed to satisfy the constraint. It is useful for ensuring downstream filters or encoders receive a compatible format without manually inserting `aresample` or format conversion filters.

## Quick Start

```sh
ffmpeg -i input.wav -af "aformat=sample_fmts=s16:sample_rates=44100:channel_layouts=stereo" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sample_fmts | sample_fmt | (all allowed) | A `\|`-separated list of acceptable sample formats, e.g., `s16\|s32\|fltp`. (alias: `f`) |
| sample_rates | int | (all allowed) | A `\|`-separated list of acceptable sample rates in Hz, e.g., `44100\|48000`. (alias: `r`) |
| channel_layouts | channel_layout | (all allowed) | A `\|`-separated list of acceptable channel layouts, e.g., `stereo\|mono`. (alias: `cl`) |

## Examples

### Force unsigned 8-bit or signed 16-bit stereo output

```sh
ffmpeg -i input.flac -af "aformat=sample_fmts=u8|s16:channel_layouts=stereo" output.wav
```

### Ensure 48 kHz sample rate for broadcast delivery

```sh
ffmpeg -i input.mp3 -af "aformat=sample_rates=48000" output.wav
```

### Restrict to float formats for a downstream DSP filter

Some filters only work with float samples. This ensures conversion happens before the chain:

```sh
ffmpeg -i input.wav -af "aformat=sample_fmts=fltp|flt,dynaudnorm" output.wav
```

### Accept either stereo or mono, forcing a conversion if needed

```sh
ffmpeg -i input.wav -af "aformat=channel_layouts=stereo|mono" output.wav
```

### Constrain all three dimensions at once

```sh
ffmpeg -i input.flac -af "aformat=sample_fmts=s16:sample_rates=44100|48000:channel_layouts=stereo" output.wav
```

## Notes

- If a parameter is omitted, any value is accepted for that dimension — you only need to specify the dimensions you want to constrain.
- FFmpeg automatically inserts the cheapest conversion (e.g., `aresample` for rate conversion, `aconvert` for format conversion) to satisfy the constraint; no explicit conversion filter is needed.
- The `|` separator in option values must be used without spaces: `s16|s32`, not `s16 | s32`.
- `aformat` is often used as a final step in a filter chain to guarantee encoder-compatible output before the muxer stage.

---

### agate

> Apply a noise gate to audio, attenuating signals that fall below a configurable threshold.

**Source:** [libavfilter/af_agate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_agate.c)

The `agate` filter applies a noise gate that attenuates (closes) when the signal level drops below the `threshold`, and opens when the level rises above it. It is commonly used to suppress background noise, room tone, or microphone hiss between speech passages. For gating triggered by an external sidechain signal, see `sidechaingate`.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "agate=threshold=0.02:attack=10:release=200" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before gating. Range: 0.015625–64. |
| mode | int | `downward` | Gate mode: `downward` (attenuate below threshold) or `upward` (attenuate above threshold). |
| range | double | `0.06125` | Attenuation when gate is closed (linear). 0 = silence, 1 = passthrough. |
| threshold | double | `0.125` | Level at which the gate opens (linear amplitude). |
| ratio | double | `2.0` | Rate of attenuation below the threshold. Higher = harder gate. |
| attack | double | `20.0` | Time in ms for the gate to open after signal exceeds threshold. |
| release | double | `250.0` | Time in ms for the gate to close after signal drops below threshold. |
| makeup | double | `1.0` | Output gain applied after gating. |
| knee | double | `2.828` | Width in dB of soft-knee transition around the threshold. |
| detection | int | `rms` | Level detection: `rms` or `peak`. |
| link | int | `average` | Multi-channel link: `average` or `maximum`. |
| level_sc | double | `1.0` | Sidechain input gain (used when operating as sidechain). |

## Examples

### Remove microphone noise between speech

```sh
ffmpeg -i interview.mp3 -af "agate=threshold=0.015:attack=20:release=500:range=0.01" output.mp3
```

### Drum gate — cut bleed between hits

Tight gate with fast release to isolate drum hits.

```sh
ffmpeg -i drums.wav -af "agate=threshold=0.05:attack=5:release=80:range=0" output.wav
```

### Gentle noise floor reduction

Reduce (but not silence) background noise.

```sh
ffmpeg -i recording.mp3 -af "agate=threshold=0.02:range=0.1:attack=50:release=1000" output.mp3
```

## Notes

- `threshold` uses linear amplitude. For dBFS conversion: `linear = 10^(dBFS/20)`. For example, -30 dBFS ≈ 0.0316.
- `range=0` completely silences the gated signal; `range=0.06125` (the default) gives about -24 dB of attenuation.
- `attack` and `release` are in milliseconds. Long release values prevent chattering (rapid open/close) on reverb tails.
- For gating triggered by a second audio stream (e.g. gate the music when the voice is active), use `sidechaingate`.

---

### alimiter

> Apply a lookahead peak limiter to audio to prevent samples from exceeding a configurable ceiling.

**Source:** [libavfilter/af_alimiter.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_alimiter.c)

The `alimiter` filter applies a lookahead peak limiter to audio, ensuring that no sample exceeds the configured `limit` ceiling. Unlike a compressor, a limiter has an effectively infinite ratio: any peak above the threshold is hard-limited. It includes optional auto-level control (ASC) to prevent pumping artifacts on sustained loud signals.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "alimiter=limit=0.9:attack=5:release=50" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain applied before limiting. Range: 0.015625–64. |
| level_out | double | `1.0` | Output gain applied after limiting. Range: 0.015625–64. |
| limit | double | `1.0` | Maximum output level (linear amplitude). Default 1.0 = 0 dBFS. |
| attack | double | `5.0` | Attack time in milliseconds. Range: 0.1–80. |
| release | double | `50.0` | Release time in milliseconds. Range: 1–8000. |
| asc | bool | `0` | Enable auto-level control to prevent pumping on sustained loud signals. |
| asc_level | double | `0.5` | ASC sensitivity (0–1). Lower values make ASC trigger less aggressively. |
| level | bool | `1` | Auto-level: auto-adjust gain to avoid clipping. |

## Examples

### True peak limiting at -1 dBFS

Standard mastering limiter ceiling to prevent inter-sample peaks above -1 dBFS.

```sh
ffmpeg -i input.mp3 -af "alimiter=limit=0.891:attack=5:release=50" output.mp3
```

### Combine with loudnorm for broadcast normalisation

Apply EBU R128 normalization then limit peaks.

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-16:TP=-1.5,alimiter=limit=0.891" output.mp3
```

### Brick-wall limiter with fast attack

Catch transient peaks very aggressively.

```sh
ffmpeg -i drums.wav -af "alimiter=limit=0.95:attack=0.5:release=20" output.wav
```

### Add input gain before limiting

Boost the signal then limit it to prevent clipping.

```sh
ffmpeg -i input.mp3 -af "alimiter=level_in=2:limit=1.0:attack=5:release=100" output.mp3
```

## Notes

- `limit=1.0` corresponds to 0 dBFS. For mastering, set `limit=0.891` (-1 dBFS) or `limit=0.794` (-2 dBFS) to leave headroom.
- Very short attack values (< 1 ms) can cause audible distortion on transients; 3–10 ms is a typical mastering range.
- ASC (`asc=1`) helps prevent pumping when the signal stays continuously loud for extended periods.
- The lookahead window is determined by the `attack` time: longer attack = more lookahead, smoother limiting.

---

### amerge

> Merge two or more audio streams into a single multi-channel stream by concatenating their channels.

**Source:** [libavfilter/af_amerge.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_amerge.c)

The `amerge` filter combines multiple audio streams into one multi-channel stream by placing all channels from each input stream side-by-side. Unlike `amix`, which sums the samples of multiple streams together, `amerge` preserves each channel independently. It is the correct tool for assembling a multi-channel file from separate mono or stereo sources.

## Quick Start

```sh
ffmpeg -i left.wav -i right.wav -filter_complex "[0:a][1:a]amerge=inputs=2" -ac 2 stereo.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | 2 | Number of input audio streams to merge. |
| layout_mode | int | legacy | How to determine the output channel layout: `legacy` (reorder channels when layouts are compatible and disjoint), `reset` (ignore input layouts, output channels in stream order), `normal` (preserve channel names without reordering). |

## Examples

### Merge two mono files into a stereo stream

Using the `amovie` source to reference files and then merging:

```sh
ffmpeg -i left.wav -i right.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2,pan=stereo|c0=c0|c1=c1" \
  stereo.wav
```

### Merge six separate audio tracks from an MKV into a single 5.1 stream

```sh
ffmpeg -i input.mkv \
  -filter_complex "[0:1][0:2][0:3][0:4][0:5][0:6]amerge=inputs=6" \
  -c:a pcm_s16le output.mkv
```

### Merge a mono vocal with a stereo music track into a 3-channel stream

```sh
ffmpeg -i vocal_mono.wav -i music_stereo.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2[out]" \
  -map "[out]" -c:a flac three_channel.flac
```

### Use reset mode to avoid unexpected channel reordering

```sh
ffmpeg -i stream1.wav -i stream2.wav \
  -filter_complex "[0:a][1:a]amerge=inputs=2:layout_mode=reset" \
  merged.wav
```

## Notes

- All inputs to `amerge` must have the same sample rate and sample format; mismatched inputs will cause an error. Insert `aresample` or `aformat` before `amerge` if needed.
- If inputs have different durations, the output stops at the end of the shortest input.
- In `legacy` mode, when input channel layouts are disjoint and known (e.g., 2.1 + FC+BL+BR = 5.1), channels are reordered to conform to the standard layout. This can produce unexpected ordering if the layouts are not perfectly complementary — use `reset` or `normal` mode to disable reordering.
- The `amerge` filter has an empty `description` field in the source data; the description above is derived from the `texi_section` documentation.

---

### amix

> Mix multiple audio input streams into a single output stream.

**Source:** [libavfilter/af_amix.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_amix.c)

The `amix` filter combines two or more audio streams into one by summing their samples. It supports per-input weighting, automatic volume normalization to prevent clipping, and configurable end-of-stream behavior. Use it to overlay background music with dialogue, combine multiple microphone inputs, or blend any set of audio sources.

## Quick Start

```sh
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex "amix=inputs=2:duration=first" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | int | 2 | Number of input audio streams to mix. |
| duration | int | longest | How to determine the end of the output stream: `longest` (continue until the longest input ends), `shortest` (stop when the shortest input ends), `first` (stop when the first input ends). |
| dropout_transition | float | 2.0 | Transition time in seconds for volume re-normalization when an input stream ends. |
| weights | string | "1 1 ..." | Space-separated weight for each input stream. The last specified weight is repeated for any remaining inputs. |
| normalize | bool | true | When enabled, inputs are scaled so the total gain stays at unity. Disable with caution — unweighted summation can clip. |

## Examples

### Mix three audio streams, ending when the first ends

```sh
ffmpeg -i INPUT1 -i INPUT2 -i INPUT3 \
  -filter_complex "amix=inputs=3:duration=first:dropout_transition=3" \
  output.mp3
```

### Mix vocals and background music with music at 25% volume

`normalize=0` preserves the explicit weight ratios without automatic re-scaling:

```sh
ffmpeg -i vocals.mp3 -i music.mp3 \
  -filter_complex "amix=inputs=2:duration=longest:dropout_transition=0:weights='1 0.25':normalize=0" \
  output.mp3
```

### Mix two stereo streams in a video pipeline

```sh
ffmpeg -i video.mp4 -i commentary.mp3 \
  -filter_complex "[0:a][1:a]amix=inputs=2:duration=first[aout]" \
  -map 0:v -map "[aout]" -c:v copy output.mp4
```

### Mix four radio channels and keep the longest

```sh
ffmpeg -i ch1.mp3 -i ch2.mp3 -i ch3.mp3 -i ch4.mp3 \
  -filter_complex "amix=inputs=4:duration=longest" \
  mixed.mp3
```

### Equal mix with a 5-second dropout transition

When one input ends, the remaining inputs are smoothly re-normalized over 5 seconds:

```sh
ffmpeg -i intro.mp3 -i loop.mp3 \
  -filter_complex "amix=inputs=2:duration=longest:dropout_transition=5" \
  output.mp3
```

## Notes

- `amix` only supports float samples internally. Integer-format inputs are automatically converted via `aresample`; if you need integer output, consider `amerge` instead.
- When `normalize=1` (the default), the volume of each input is scaled by `1/n_active_inputs`, which avoids clipping but also reduces loudness when all streams are active. Use `weights` to compensate.
- The `weights` and `normalize` options can be changed at runtime using the `sendcmd` filter.
- For lossless channel merging (e.g., combining separate mono tracks into a stereo file), `amerge` is more appropriate than `amix`.

---

### anull

> Pass audio through unchanged — a no-op filter useful for testing and filter graph construction.

**Source:** [libavfilter/af_anull.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_anull.c)

The `anull` filter passes every audio sample to its output without modification. It has no parameters and introduces no latency or processing overhead. Its primary uses are as a placeholder in filter graphs during development, as a no-op endpoint when a filter is syntactically required but no transformation is desired, and in testing pipelines to verify that audio passes through a graph correctly.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "anull" output.mp3
```

## Parameters

This filter has no parameters.

## Examples

### Verify that audio passes through a filter graph

```sh
ffmpeg -i input.mp3 -af "anull" -f null -
```

### Use as a placeholder while building a graph

Replace `anull` with the intended filter once it is determined:

```sh
ffmpeg -i input.mp3 -af "anull" output.mp3
```

### Combine with other filters in a complex graph

`anull` can serve as a labelled passthrough node in a `filter_complex` graph:

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]anull[out]" -map "[out]" output.mp3
```

## Notes

- `anull` is the audio equivalent of the `null` video filter.
- It incurs no measurable performance overhead — the filter framework may optimize it away entirely.
- Using `anull` in a production pipeline is harmless but unnecessary; it can be removed without any change to the output.

---

### apad

> Pad the end of an audio stream with silence to reach a minimum length or to match a video stream duration.

**Source:** [libavfilter/af_apad.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_apad.c)

The `apad` filter appends silence to the end of an audio stream. It can add a fixed number of samples, extend the stream to a minimum total length, or pad indefinitely. Its most common use is in combination with the `-shortest` FFmpeg option to prevent audio from ending before a longer video track.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "apad=pad_dur=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| packet_size | int | 4096 | Size of each silence packet in samples. |
| pad_len | int64 | — | Number of silence samples to append. Mutually exclusive with `whole_len`. |
| whole_len | int64 | — | Minimum total number of samples in the output. Silence is appended until this count is reached. Mutually exclusive with `pad_len`. |
| pad_dur | duration | — | Duration of silence to append (e.g., `2.5` seconds). Mutually exclusive with `whole_dur`. |
| whole_dur | duration | — | Minimum total duration of the output. Silence is appended until this duration is reached. Mutually exclusive with `pad_dur`. |

## Examples

### Add 1024 samples of silence to the end

```sh
ffmpeg -i input.wav -af "apad=pad_len=1024" output.wav
```

### Ensure the output is at least 10000 samples long

```sh
ffmpeg -i input.wav -af "apad=whole_len=10000" output.wav
```

### Add 2 seconds of silence at the end

```sh
ffmpeg -i input.mp3 -af "apad=pad_dur=2" output.mp3
```

### Pad audio to match a video's duration when using -shortest

This is the canonical use case: pad audio silence so it outlasts the video, then let `-shortest` trim both to the video length:

```sh
ffmpeg -i video.mp4 -i audio.mp3 \
  -filter_complex "[1:a]apad[aout]" \
  -map 0:v -map "[aout]" -shortest output.mp4
```

### Ensure a minimum total duration of 30 seconds

```sh
ffmpeg -i input.mp3 -af "apad=whole_dur=30" output.mp3
```

## Notes

- If none of `pad_len`, `whole_len`, `pad_dur`, or `whole_dur` is set, `apad` will append silence indefinitely — this is intentional when used with `-shortest` to guarantee the audio outlasts the video.
- `pad_dur` and `whole_dur` are mutually exclusive; setting both causes an error.
- `pad_len` and `whole_len` are also mutually exclusive.
- Note: in FFmpeg 4.4 and earlier, setting `pad_dur=0` or `whole_dur=0` also triggered infinite padding. In later versions, a zero value is treated as "disabled".

---

### aphaser

> Apply a phasing effect to audio using an all-pass filter chain modulated by an LFO.

**Source:** [libavfilter/af_aphaser.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_aphaser.c)

The `aphaser` filter applies a phaser effect by passing audio through a chain of all-pass filters whose cutoff frequencies are modulated by a low-frequency oscillator (LFO). This creates the characteristic sweeping notches in the frequency spectrum associated with phaser pedals. Unlike a flanger, a phaser does not use a delay line — it produces a smoother, more subtle effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "aphaser=in_gain=0.4:speed=0.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | double | `0.4` | Input gain. Range: 0–1. |
| out_gain | double | `0.74` | Output gain. Range: 0–1. |
| delay | double | `3.0` | Delay in milliseconds (initial phase shift). Range: 0–5. |
| decay | double | `0.4` | Feedback decay — controls intensity. Range: 0–0.99. |
| speed | double | `0.5` | LFO modulation speed in Hz. Range: 0.1–2. |
| type | int | `triangular` | LFO waveform: `triangular` or `sinusoidal`. |

## Examples

### Classic slow phaser

```sh
ffmpeg -i guitar.wav -af "aphaser=in_gain=0.4:decay=0.4:speed=0.3" output.wav
```

### Fast, intense phaser

```sh
ffmpeg -i synth.mp3 -af "aphaser=decay=0.8:speed=1.5:type=sinusoidal" output.mp3
```

### Subtle vocal phaser

```sh
ffmpeg -i vocal.wav -af "aphaser=in_gain=0.6:decay=0.3:speed=0.4" output.wav
```

### Deep sweeping phaser

```sh
ffmpeg -i bass.wav -af "aphaser=delay=5:decay=0.7:speed=0.2" output.wav
```

## Notes

- `decay` is the most significant quality knob: higher values (>0.7) produce intense resonant sweeps; lower values (0.2–0.4) are subtle.
- `speed` controls how fast the LFO sweeps. For tempo-locked effects, calculate `speed = BPM/60 / beat_division`.
- Phaser is more subtle than flanger because it uses all-pass filters rather than a physical delay line — it changes phase without adding a distinct echo.
- `out_gain` may need to be reduced if `decay` is high, as strong resonance can boost the signal level.

---

### apulsator

> Modulate stereo audio volume with an LFO (low-frequency oscillator) to create tremolo, auto-panning, or rhythmic stereo effects.

**Source:** [libavfilter/af_apulsator.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_apulsator.c)

The `apulsator` filter is a stereo LFO (low-frequency oscillator) effect that modulates the volume of the left and right audio channels independently. With `offset_r=0`, it acts as a tremolo (both channels pulse together). With `offset_r=0.5` (default), it acts as an auto-panner (channels alternate 180° out of phase). Intermediate offsets create sweeping, rotating stereo effects. Multiple waveform shapes are available.

## Quick Start

```sh
# Auto-panner at 2 Hz
ffmpeg -i input.wav -af "apulsator" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain (0.015625–64). |
| level_out | double | `1.0` | Output gain (0.015625–64). |
| mode | int | `sine` | LFO waveform: `sine`, `triangle`, `square`, `sawup`, `sawdown`. |
| amount | double | `1.0` | Modulation depth (0–1). |
| offset_l | double | `0.0` | Left channel LFO phase offset (0–1). |
| offset_r | double | `0.5` | Right channel LFO phase offset (0–1). Default 0.5 = auto-pan. |
| width | double | `1.0` | Pulse width (0–2). |
| timing | int | `hz` | Timing mode: `hz`, `bpm`, or `ms`. |
| hz | double | `2.0` | LFO frequency in Hz (0.01–100, when `timing=hz`). |
| bpm | double | `120.0` | LFO rate in BPM (30–300, when `timing=bpm`). |
| ms | int | `500` | LFO period in milliseconds (10–2000, when `timing=ms`). |

## Examples

### Auto-panner (default)

```sh
ffplay -i music.wav -af apulsator
```

### Tremolo effect (both channels in phase)

```sh
ffmpeg -i input.wav -af "apulsator=offset_r=0:hz=5" tremolo.wav
```

### Slow auto-pan at 120 BPM with triangle wave

```sh
ffmpeg -i input.wav -af "apulsator=mode=triangle:timing=bpm:bpm=120" output.wav
```

### Fast pulsing effect with square wave

```sh
ffplay -i music.wav -af "apulsator=mode=square:hz=8:amount=0.8"
```

## Notes

- `offset_r=0` → tremolo; `offset_r=0.5` → auto-pan; values in between → continuous panning sweep.
- `amount` sets how much the LFO modulates the signal — `1.0` = full modulation (channel can go silent at the trough); `0.5` = half modulation.
- Use `timing=bpm` when working to music tempo; `timing=ms` for precise period control.
- Combine `mode=sine:offset_r=0.5` for the smoothest auto-pan effect.

---

### aresample

> Resample audio to a different sample rate or convert between audio formats using libswresample.

**Source:** [libavfilter/af_aresample.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_aresample.c)

The `aresample` filter converts audio to a different sample rate and can also stretch or compress audio timestamps to maintain synchronization. It is powered by the `libswresample` library and exposes all of its resampler options. When no parameters are given, it acts as an automatic format adapter, inserting itself wherever a format conversion is needed in a filter graph.

## Quick Start

```sh
ffmpeg -i input.flac -af "aresample=44100" output.flac
```

## Parameters

`aresample` has no parameters defined in its JSON option list. It accepts the following syntax:

```
aresample=[sample_rate:]resampler_options
```

| Argument | Description |
|----------|-------------|
| sample_rate | Target sample rate in Hz. Optional; if omitted, the rate is negotiated automatically. |
| resampler_options | Colon-separated `key=value` pairs passed directly to `libswresample`. See the `ffmpeg-resampler` manual for the complete list. |

Common `libswresample` options:

| Option | Description |
|--------|-------------|
| `async` | Maximum number of samples per second the resampler may add or remove to compensate for timestamp drift. |
| `first_pts` | Assume the first PTS is this value instead of zero. |
| `min_hard_comp` | Minimum difference (in seconds) between timestamps before hard compensation (inserting/dropping samples) is triggered. |
| `filter_size` | Length of the resampling filter (more taps = higher quality, more CPU). |

## Examples

### Resample to 44100 Hz

```sh
ffmpeg -i input_48k.wav -af "aresample=44100" output_44k.wav
```

### Resample to 48000 Hz (common broadcast standard)

```sh
ffmpeg -i input.mp3 -af "aresample=48000" output.wav
```

### Timestamp compensation with up to 1000 samples/s adjustment

This allows the resampler to insert or drop up to 1000 samples per second to correct A/V drift:

```sh
ffmpeg -i input.mp4 -af "aresample=async=1000" output.mp4
```

### High-quality resampling with a larger filter

A longer filter kernel gives better frequency response at the cost of more CPU:

```sh
ffmpeg -i input.flac -af "aresample=96000:filter_size=256" output_96k.flac
```

### Automatic format negotiation (no arguments)

Let FFmpeg decide when a conversion is needed — useful in complex filter graphs:

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]aresample,dynaudnorm[out]" -map "[out]" output.mp3
```

## Notes

- `aresample` with no arguments is equivalent to `aformat` with no constraints — it acts as a passthrough unless FFmpeg's filter negotiation decides a conversion is needed.
- The `async` option is particularly useful when synchronizing audio to video in files with imprecise timestamps; it gradually corrects drift without audible artifacts.
- Very high sample rate conversion (e.g., 8000 Hz to 192000 Hz) is computationally expensive; consider whether it is actually required before including it in a pipeline.
- The `aresample` filter has an empty `options` list in the source JSON because its options are passed through to `libswresample` rather than being declared as AVOptions.

---

### arnndn

> Reduce noise from speech recordings using a Recurrent Neural Network model trained specifically for voice denoising.

**Source:** [libavfilter/af_arnndn.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_arnndn.c)

The `arnndn` filter removes noise from speech audio using a Recurrent Neural Network (RNN) trained on a large corpus of speech and noise samples. Unlike `afftdn` which uses generic spectral subtraction, `arnndn` is optimized specifically for voice recordings and can cleanly separate speech from complex background noise (crowds, traffic, wind). Requires an external `.rnnn` model file.

## Quick Start

```sh
ffmpeg -i noisy_voice.wav -af "arnndn=m=/path/to/model.rnnn" clean.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| model / m | string | — | Path to the `.rnnn` model file. **Required.** |
| mix | float | `1` | Mix ratio of denoised vs. original. Range: -1 to 1. 1=full denoised, 0=original, -1=noise only. |

## Examples

### Full denoising with a model file

```sh
ffmpeg -i speech_with_noise.wav \
  -af "arnndn=m=./models/bd.rnnn" \
  clean_speech.wav
```

### Partial denoising (70% clean, 30% original)

```sh
ffmpeg -i interview.wav \
  -af "arnndn=m=./models/bd.rnnn:mix=0.7" \
  output.wav
```

### Extract removed noise only (`mix=-1`)

```sh
ffmpeg -i input.wav \
  -af "arnndn=m=./models/bd.rnnn:mix=-1" \
  noise_only.wav
```

### Chain with compand for broadcast speech

```sh
ffmpeg -i podcast.wav \
  -af "arnndn=m=./models/lq.rnnn,compand=attacks=0.1:decays=0.3:points=-70/-70|-20/-10|0/-3" \
  output.wav
```

## Notes

- Pre-trained model files are available in the `ffmpeg-rnnnoise-models` and `RNNoise` projects. Common models: `bd.rnnn` (broadband), `lq.rnnn` (low quality microphone), `mp.rnnn` (music+speech).
- `arnndn` is designed for speech — it may suppress or distort non-speech audio (music, sound effects).
- `mix=-1` outputs the removed noise, useful to verify what the model is discarding.
- The model expects 48 kHz audio; FFmpeg will automatically resample if needed, but for best results ensure input is at 48 kHz.
- For non-speech audio, `afftdn` with noise floor tracking is usually a better choice.

---

### asplit

> Split an audio stream into two or more identical copies for parallel processing in a filter graph.

**Source:** [libavfilter/split.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/split.c)

The `asplit` filter duplicates an audio stream into multiple identical output streams. Each output is an independent copy of the input that can be routed to a different branch of a filter graph. Use it whenever you need to apply different processing chains to the same audio source, or when you want to mix a processed version back with the original (parallel processing).

## Quick Start

```sh
ffmpeg -i input.mp3 -filter_complex "[0:a]asplit=2[a1][a2]" -map "[a1]" out1.mp3 -map "[a2]" out2.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| outputs | int | 2 | Number of output streams to produce. All outputs are identical copies of the input. |

## Examples

### Split into two outputs and apply different EQ to each

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]asplit=2[a1][a2]; \
    [a1]highpass=f=200[high]; \
    [a2]lowpass=f=500[low]" \
  -map "[high]" high.mp3 \
  -map "[low]" low.mp3
```

### Parallel compression: blend dry and compressed signals

```sh
ffmpeg -i drums.wav \
  -filter_complex "[0:a]asplit=2[dry][wet]; \
    [wet]acompressor=threshold=0.1:ratio=8:makeup=4[comp]; \
    [dry][comp]amix=inputs=2:weights='0.5 0.5'[out]" \
  -map "[out]" parallel_comp.wav
```

### Split into three branches for simultaneous encoding

```sh
ffmpeg -i input.flac \
  -filter_complex "[0:a]asplit=3[a1][a2][a3]" \
  -map "[a1]" -c:a aac out_aac.m4a \
  -map "[a2]" -c:a mp3 out_mp3.mp3 \
  -map "[a3]" -c:a flac out_flac.flac
```

### Preview and save simultaneously

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]asplit=2[play][save]" \
  -map "[play]" -f alsa default \
  -map "[save]" saved.mp3
```

## Notes

- Each output of `asplit` is a full copy of the input data. Memory usage scales linearly with the number of outputs; use only as many as you need.
- The source JSON lists `asplit` with `type = "video"` and description "Pass on the input to N video outputs" — this is a known data artifact from the shared `split.c` implementation. `asplit` is the audio-specific variant; the video counterpart is `split`.
- For two outputs, `asplit` and `asplit=2` are equivalent.
- `asplit` is a pure routing primitive with no signal processing and no latency.

---

### atempo

> Adjust audio playback speed without changing pitch, using a time-stretching algorithm.

**Source:** [libavfilter/af_atempo.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_atempo.c)

The `atempo` filter changes the playback speed of audio — making it faster or slower — without altering the pitch. It accepts a tempo scale factor where 1.0 is the original speed, values below 1.0 slow it down, and values above 1.0 speed it up. The supported range per instance is 0.5–100.0. For ratios outside the range 0.5–2.0, FFmpeg skips some samples instead of blending them; to avoid artifacts for large changes, chain multiple `atempo` instances whose product equals the desired ratio.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "atempo=1.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tempo | double | 1.0 | Playback speed multiplier. Range: 0.5–100.0. Values below 1.0 slow down, values above 1.0 speed up. |

## Examples

### Slow down audio to 80% speed

```sh
ffmpeg -i input.mp3 -af "atempo=0.8" slow.mp3
```

### Speed up audio to 150% (1.5×)

```sh
ffmpeg -i input.mp3 -af "atempo=1.5" fast.mp3
```

### Speed up to 300% by chaining two instances

For ratios above 2.0, chaining two filters whose product equals the target avoids sample-skipping artifacts:

```sh
ffmpeg -i input.mp3 -af "atempo=sqrt(3),atempo=sqrt(3)" output.mp3
```

### Speed up to 400% using two 2.0× steps

```sh
ffmpeg -i input.mp3 -af "atempo=2.0,atempo=2.0" output.mp3
```

### Slow down to 25% by chaining two 0.5× steps

```sh
ffmpeg -i input.mp3 -af "atempo=0.5,atempo=0.5" output.mp3
```

## Notes

- The `tempo` parameter supports AVExpr expressions such as `sqrt(3)`, which is useful when chaining filters to achieve an exact combined ratio.
- For tempo values in the range 0.5–2.0, the filter uses a phase vocoder-style time-stretching algorithm. Outside this range (2.0–100.0), some samples are skipped rather than blended, which can introduce noticeable artifacts on musical content — chain multiple instances to stay within the blending range.
- The minimum supported value per instance is 0.5 (half speed). Values below 0.5 or above 100.0 will produce an error.
- `atempo` changes duration but not pitch. To change pitch without changing duration, use the `asetrate` filter followed by `aresample`.
- The `tempo` value can be updated at runtime using the `sendcmd` filter, which allows dynamic speed changes without re-encoding.

---

### atrim

> Trim an audio stream to a specified time range or sample range, discarding everything outside it.

**Source:** [libavfilter/trim.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/trim.c)

The `atrim` filter extracts a continuous subrange from an audio stream and drops all samples outside that range. It can be specified by wall-clock timestamps, PTS values in samples, or by absolute sample count. Use it to cut out a specific section of audio without re-encoding the container, or to chain with `asetpts` to reset timestamps after trimming.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "atrim=start=30:end=90" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | duration | — | Timestamp of the first sample to keep, in seconds (or as a time duration string). |
| end | duration | — | Timestamp of the first sample to drop (the sample immediately before this point is the last kept). |
| duration | duration | — | Maximum duration of the output. The stream ends after this many seconds even if `end` is not set. |
| start_pts | int64 | — | Start point expressed as a PTS value in samples rather than seconds. |
| end_pts | int64 | — | End point expressed as a PTS value in samples. |
| start_sample | int64 | — | Zero-based index of the first sample to include in the output. |
| end_sample | int64 | — | Zero-based index of the first sample to exclude from the output. |

## Examples

### Keep only the second minute of audio

```sh
ffmpeg -i input.mp3 -af "atrim=60:120" output.mp3
```

### Keep the first 30 seconds

```sh
ffmpeg -i input.mp3 -af "atrim=end=30" output.mp3
```

### Keep only the first 1000 samples

```sh
ffmpeg -i input.wav -af "atrim=end_sample=1000" output.wav
```

### Extract a clip and reset timestamps to start at zero

After trimming, the timestamps still reflect the original stream position. Add `asetpts` to renumber them from zero:

```sh
ffmpeg -i input.mp3 -af "atrim=start=60:end=120,asetpts=PTS-STARTPTS" clip.mp3
```

### Trim to a maximum duration of 10 seconds

```sh
ffmpeg -i input.mp3 -af "atrim=duration=10" short.mp3
```

## Notes

- `atrim` does not modify timestamps — the output samples still carry their original PTS values. Use `asetpts=PTS-STARTPTS` after trimming if downstream filters or muxers require timestamps starting at zero.
- The `start`/`end` and `start_pts`/`end_pts` options are timestamp-based and can give different results from `start_sample`/`end_sample` when timestamps are imprecise or do not start at zero.
- When multiple start or end constraints are set simultaneously, the filter keeps any sample that satisfies at least one constraint. To keep only samples matching all constraints, chain multiple `atrim` instances.
- The `type` field in the source JSON shows `video` — this is a known data artifact; `atrim` is the audio-specific trim filter (the video counterpart is `trim`).

---

### axcorrelate

> Compute the normalized cross-correlation between two audio streams over a sliding window, producing a correlation signal (-1 to +1) useful for sync detection.

**Source:** [libavfilter/af_axcorrelate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_axcorrelate.c)

The `axcorrelate` filter computes the normalized windowed cross-correlation between two input audio streams. The output value for each window ranges from −1 to +1: `+1` means the two inputs are identical in that window, `0` means uncorrelated, and `−1` means they are exactly out of phase (cancel each other when summed). It is used for audio synchronization detection, checking mono compatibility, and analyzing the relationship between two recordings of the same event.

## Quick Start

```sh
# Check correlation between left and right channels of stereo audio
ffmpeg -i stereo.wav -af "channelsplit,axcorrelate=size=1024" correlation.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size | int | `256` | Segment size in samples (2–131072). Larger = smoother, less time resolution. |
| algo | int | `best` | Algorithm: `slow` (accurate), `fast` (assumes zero mean), `best` (auto-select). |

## Examples

### Stereo channel correlation check

```sh
ffmpeg -i stereo.wav -af "channelsplit,axcorrelate=size=1024:algo=fast" correlation.wav
```

### Check sync between two recordings

```sh
ffmpeg -i recording1.wav -i recording2.wav \
  -filter_complex "[0:a][1:a]axcorrelate=size=4096" correlation.wav
```

### Print correlation values to stdout

```sh
ffmpeg -i stereo.wav \
  -af "channelsplit,axcorrelate=size=512,metadata=print:file=-" \
  -f null - 2>/dev/null
```

## Notes

- Output of `+1` throughout indicates the two streams are identical (or one is a scaled copy of the other).
- Output near `−1` means the streams cancel when summed to mono — problematic for broadcast mono downmix.
- `algo=fast` assumes signal mean is zero (valid for typical audio) and is significantly faster than `algo=slow`.
- For stereo phase visualization, `aphasemeter` provides a Lissajous display of the same relationship.

---

### channelmap

> Remap audio channels — reorder, duplicate, or select specific channels from the input to produce a different output channel layout.

**Source:** [libavfilter/af_channelmap.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_channelmap.c)

The `channelmap` filter remaps input audio channels to output positions, allowing you to reorder channels, extract a subset, duplicate channels, or fix incorrect channel assignments. The `map` parameter uses `|`-separated `input-output` pairs specified by channel name (e.g. `FL`, `FR`, `LFE`) or by index number. This is particularly useful for fixing 5.1 files with incorrectly ordered channels.

## Quick Start

```sh
# Swap left and right channels
ffmpeg -i input.wav -af "channelmap=map=FR-FL|FL-FR" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| map | string | (passthrough) | `\|`-separated list of `in_channel-out_channel` or `in_channel` mappings. |
| channel_layout | chlayout | (auto) | Output channel layout. If unspecified, guessed from the mapping. |

## Examples

### Extract downmix channels from 5.1+downmix

```sh
ffmpeg -i in.mov -af "channelmap=map=DL-FL|DR-FR" stereo.wav
```

### Fix AAC 5.1 channel order (AAC native → standard 5.1)

```sh
ffmpeg -i in.wav -af "channelmap=1|2|0|5|3|4:5.1" out.wav
```

### Duplicate left channel to both outputs (mono to dual-mono)

```sh
ffmpeg -i mono.wav -af "channelmap=map=FL-FL|FL-FR:channel_layout=stereo" dual_mono.wav
```

### Reorder 7.1 channels

```sh
ffmpeg -i surround.wav \
  -af "channelmap=map=FL-FL|FR-FR|FC-FC|LFE-LFE|SL-SL|SR-SR|BL-BL|BR-BR:7.1" \
  out.wav
```

## Notes

- Channel names: `FL`=front left, `FR`=front right, `FC`=front center, `LFE`=low frequency, `SL`/`SR`=side, `BL`/`BR`=back, `DL`/`DR`=downmix left/right.
- Mappings can use names (`FL-FR`) or indices (`0|1|2`), but mixing both types is not allowed.
- If `channel_layout` is not specified, FFmpeg guesses the output layout from the channel names used as destinations.
- For more complex channel routing with level control, use the `pan` filter instead.

---

### channelsplit

> Split a multi-channel audio stream into separate per-channel mono streams for independent processing or routing.

**Source:** [libavfilter/af_channelsplit.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_channelsplit.c)

The `channelsplit` filter splits a multi-channel audio stream into separate single-channel mono streams — one output per channel. This enables routing individual channels to different outputs, applying per-channel processing, or extracting specific channels (e.g. just the LFE from a 5.1 mix). It is a multiple-output filter and requires `-filter_complex`.

## Quick Start

```sh
# Split stereo into L and R
ffmpeg -i stereo.mp3 -filter_complex channelsplit out.mkv
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| channel_layout | chlayout | `stereo` | Channel layout of the input stream (e.g. `stereo`, `5.1`, `7.1`). |
| channels | string | `all` | Channels to extract, or `all`. E.g. `FL+FR`, `LFE`. |

## Examples

### Split stereo into separate L/R files

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex 'channelsplit=channel_layout=stereo[L][R]' \
  -map '[L]' left.wav \
  -map '[R]' right.wav
```

### Split 5.1 into 6 individual channel files

```sh
ffmpeg -i surround.wav \
  -filter_complex 'channelsplit=channel_layout=5.1[FL][FR][FC][LFE][SL][SR]' \
  -map '[FL]' front_left.wav \
  -map '[FR]' front_right.wav \
  -map '[FC]' center.wav \
  -map '[LFE]' lfe.wav \
  -map '[SL]' side_left.wav \
  -map '[SR]' side_right.wav
```

### Extract only the LFE channel

```sh
ffmpeg -i surround.wav \
  -filter_complex 'channelsplit=channel_layout=5.1:channels=LFE[lfe]' \
  -map '[lfe]' lfe.wav
```

### Merge L and R back together after independent processing

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex 'channelsplit=channel_layout=stereo[L][R];[L]highpass=f=200[Lp];[R]lowpass=f=8000[Rp];[Lp][Rp]amerge' \
  output.mp3
```

## Notes

- Specifying a `channel_layout` that doesn't match the actual input will result in a mismatch error — use `ffprobe` to check input channel layout first.
- Use `channels=all` (default) to extract every channel individually; use a named subset like `FL+FR` to extract only specific channels.
- The number and order of output pads matches the channels in the order specified by `channels`.
- To recombine split channels, use `amerge` (merge into multi-channel) or `join` (with explicit mapping).

---

### chorus

> Add a chorus effect to audio by mixing the signal with delayed, pitch-modulated copies.

**Source:** [libavfilter/af_chorus.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_chorus.c)

The `chorus` filter adds a chorus effect by mixing the original signal with one or more delayed and pitch-modulated copies. The pitch modulation is achieved by oscillating the delay time, simulating the slight timing and pitch variations that occur when multiple voices or instruments play in unison. Each chorus "voice" is defined by a set of delay, decay, speed, and depth values.

## Quick Start

```sh
# Single-voice chorus
ffmpeg -i input.mp3 -af "chorus=in_gain=0.5:out_gain=0.9:delays=50:decays=0.8:speeds=0.5:depths=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| in_gain | float | `0.4` | Input gain applied before the chorus effect. Range: 0–1. |
| out_gain | float | `0.4` | Output gain. Range: 0–1. |
| delays | string | — | Pipe-separated list of delay times in milliseconds per voice (e.g. `55\|60`). |
| decays | string | — | Pipe-separated list of decay (feedback) values per voice (e.g. `0.4\|0.4`). Range per voice: 0–1. |
| speeds | string | — | Pipe-separated list of LFO speeds in Hz per voice (e.g. `0.25\|0.5`). |
| depths | string | — | Pipe-separated list of depth (modulation amount) in milliseconds per voice. |

## Examples

### Subtle single-voice chorus

```sh
ffmpeg -i vocal.mp3 -af "chorus=in_gain=0.5:out_gain=0.9:delays=50:decays=0.8:speeds=0.5:depths=2" output.mp3
```

### Two-voice chorus for guitar

```sh
ffmpeg -i guitar.wav -af "chorus=in_gain=0.6:out_gain=0.9:delays=55|60:decays=0.4|0.4:speeds=0.25|0.5:depths=2|3" output.wav
```

### Rich three-voice vocal doubling

```sh
ffmpeg -i vocal.mp3 -af "chorus=0.5:0.9:50|60|40:0.8|0.7|0.8:0.5|0.3|0.7:2|2.5|1.5" output.mp3
```

### Slow deep chorus for strings

```sh
ffmpeg -i strings.wav -af "chorus=in_gain=0.4:out_gain=0.8:delays=70:decays=0.6:speeds=0.2:depths=4" output.wav
```

## Notes

- Each pipe-separated set (delays, decays, speeds, depths) must have the same number of elements — one per chorus voice.
- `delays` sets the base delay (in ms) around which the LFO oscillates. Typical values: 20–80 ms.
- `depths` sets the maximum additional delay from the LFO (also in ms). Higher values = more obvious pitch wobble.
- `in_gain` and `out_gain` together control the output level — reduce both if the output clips.

---

### compand

> Compress or expand the dynamic range of audio using a configurable transfer function and attack/decay times.

**Source:** [libavfilter/af_compand.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_compand.c)

The `compand` filter performs combined compression and expansion of audio dynamic range. Unlike `acompressor`, it specifies the transfer function as a series of (input, output) level points, with separate attack and decay time constants. It can both compress loud sounds and expand (boost) quiet ones, and supports an initial volume level and a time-delayed bypass for de-noising.

## Quick Start

```sh
# Gentle compression
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=0.8:points=-80/-80|-45/-15|0/-3:gain=3" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| attacks | string | `0.3` | Comma-separated attack times per channel in seconds. |
| decays | string | `0.8` | Comma-separated decay (release) times per channel in seconds. |
| points | string | — | Transfer function as `input/output` pairs in dBFS. E.g. `-70/-70\|-60/-20\|0/0`. |
| soft-knee | double | `0.01` | Softness of the knee in dB. |
| gain | double | `0.0` | Output gain in dB. |
| volume | double | `0.0` | Initial volume in dB (at startup). |
| delay | double | `0.0` | Delay in seconds before compression activates. |

## Examples

### Radio-style compression

Aggressive compression for broadcast/radio with high perceived loudness.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.3:decays=0.8:points=-70/-70|-60/-20|0/-3:soft-knee=6:gain=6" output.mp3
```

### Noise gate + compression combined

Silence signals below -50 dBFS, compress everything above -20 dBFS.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.2:decays=0.5:points=-90/-900|-50/-50|-20/-15|0/-3" output.mp3
```

### Expand quiet audio (reverse compression)

Boost signals below -40 dBFS to reduce noise floor.

```sh
ffmpeg -i input.mp3 -af "compand=attacks=0.05:decays=0.1:points=-80/-80|-40/-40|-10/-10|0/0:gain=4" output.mp3
```

## Notes

- `points` defines the transfer function: each `x/y` pair maps input level x dBFS to output level y dBFS. Connect at least 2 points; points must be in ascending input-level order.
- For a gate, set the output for low inputs to `-900` (silence): `points=-90/-900|-50/-50|0/0` silences everything below -50 dBFS.
- `attacks` and `decays` are in seconds (not milliseconds as in `acompressor`). Typical broadcast values: attack=0.3s, decay=0.8s.
- For a simpler ratio-based compressor, `acompressor` is easier to configure; `compand` provides more flexibility for complex multi-point transfer curves.

---

### deesser

> Reduce sibilance ('s', 'sh', 'ch' sounds) in vocal recordings by dynamically attenuating high-frequency harsh content.

**Source:** [libavfilter/af_deesser.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_deesser.c)

The `deesser` filter reduces harsh sibilant sounds — the piercing 's', 'sh', and 'ch' consonants common in vocal recordings — by detecting and attenuating the offending high-frequency energy. Unlike a static high-shelf EQ cut, it operates dynamically, only reducing treble when sibilance is detected. The `s` option lets you monitor just the removed frequencies to dial in the settings.

## Quick Start

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| i | double | `0` | Intensity: sibilance detection sensitivity. Range: 0–1. Higher = triggers more easily. |
| m | double | `0.5` | Amount of ducking on the treble portion. Range: 0–1. 1 = maximum attenuation. |
| f | double | `0.5` | Frequency content preservation. Range: 0–1. Higher = keep more original high frequencies. |
| s | int | `o` | Output mode: `i` (pass input unchanged), `o` (pass de-essed output), `e` (pass only removed ess). |

## Examples

### Basic de-essing on a vocal

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5" output.wav
```

### Aggressive de-essing for harsh microphone

```sh
ffmpeg -i harsh_vocal.wav -af "deesser=i=0.8:m=0.8:f=0.3" output.wav
```

### Subtle de-essing (minimal impact on sound)

```sh
ffmpeg -i interview.wav -af "deesser=i=0.3:m=0.3:f=0.7" output.wav
```

### Monitor what is being removed (`e` mode)

```sh
ffmpeg -i vocal.wav -af "deesser=i=0.5:m=0.5:s=e" ess_only.wav
```

## Notes

- Use `s=e` (ess-only output mode) to hear exactly what frequencies are being removed — this helps dial in `i` and `m` correctly before committing.
- `i` (intensity) controls when the de-esser triggers: low values only trigger on very strong sibilance; high values are more aggressive.
- `m` (max ducking) controls the reduction depth: `0.5` is moderate; `1.0` is maximum attenuation.
- `f` preserves original high-frequency content after de-essing — higher values sound more natural but may leave some sibilance.
- For clinical de-essing, pair with a high-shelf EQ cut to further tame the top end after de-essing.

---

### dynaudnorm

> Dynamically normalize audio on a frame-by-frame basis, evening out volume differences while preserving within-frame dynamic range.

**Source:** [libavfilter/af_dynaudnorm.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_dynaudnorm.c)

The `dynaudnorm` filter applies per-frame gain normalization so that each frame's peak magnitude approaches a target level. Unlike a static normalizer that computes one gain for the entire file, or a compressor that clips dynamic range, `dynaudnorm` uses a Gaussian-smoothed gain curve across frames to gently even out the volume of quiet and loud sections while retaining 100% of the dynamic range within each frame. It is well-suited for normalizing speech recordings, audio books, and archival material with highly variable loudness.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "dynaudnorm" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| framelen | int | 500 | Length of each analysis frame in milliseconds. Range: 10–8000 ms. (alias: `f`) |
| gausssize | int | 31 | Window size (in frames) of the Gaussian smoothing filter applied to the per-frame gain curve. Must be an odd number. Range: 3–301. (alias: `g`) |
| peak | double | 0.95 | Target peak magnitude for normalized output (0.0–1.0 linear). (alias: `p`) |
| maxgain | double | 10.0 | Maximum gain factor that can be applied to any frame. Prevents over-amplification of very quiet segments. (alias: `m`) |
| targetrms | double | 0.0 | If non-zero, normalize to this RMS level rather than the peak level. Disabled by default. (alias: `r`) |
| coupling | bool | true | When enabled, all channels receive the same gain factor (derived from the loudest channel), preserving stereo balance. (alias: `n`) |
| correctdc | bool | false | Enable DC bias correction to remove any DC offset before normalization. (alias: `c`) |
| altboundary | bool | false | Use silence (rather than the first/last frame value) as boundary condition for the Gaussian filter at stream edges. (alias: `b`) |
| compress | double | 0.0 | Pre-compression factor applied before normalization. 0.0 disables pre-compression. (alias: `s`) |
| threshold | double | 0.0 | Frames whose peak magnitude is below this value are treated as silence and excluded from normalization. (alias: `t`) |
| channels | string | all | Comma-separated list of channels to apply normalization to. (alias: `h`) |
| overlap | double | 0.0 | Fraction of frame overlap (0.0–1.0) to smooth transitions between frames. (alias: `o`) |

## Examples

### Default normalization (recommended starting point)

```sh
ffmpeg -i input.mp3 -af "dynaudnorm" output.mp3
```

### Faster adaptation (shorter frame, smaller Gaussian window)

A 200 ms frame with a window of 11 reacts more quickly to loudness changes — suitable for rapidly varying content:

```sh
ffmpeg -i podcast.mp3 -af "dynaudnorm=f=200:g=11" output.mp3
```

### Slower, more gradual normalization

A longer Gaussian window makes the normalizer behave more like a static loudness pass, with very gentle gain changes:

```sh
ffmpeg -i audiobook.mp3 -af "dynaudnorm=f=500:g=101" output.mp3
```

### Normalize with a maximum gain cap to avoid pumping

Cap gain at 5× to prevent over-amplification of near-silent passages:

```sh
ffmpeg -i input.mp3 -af "dynaudnorm=maxgain=5" output.mp3
```

### RMS-based normalization

Normalize to a target RMS level instead of peak — often sounds more consistent for speech:

```sh
ffmpeg -i speech.wav -af "dynaudnorm=targetrms=0.25" output.wav
```

## Notes

- The filter introduces latency equal to approximately half of `gausssize` × `framelen` milliseconds, because the Gaussian filter is centered around the current frame and needs to look ahead. This makes it unsuitable for real-time streaming.
- A larger `gausssize` produces a smoother gain curve (less audible gain pumping) but reduces responsiveness to sudden loudness changes. A smaller value makes the filter behave more like a dynamic range compressor.
- Setting `coupling=false` allows each channel to receive independent gain, which can alter stereo or surround image — leave it enabled for music and most stereo content.
- The `maxgain` cap is important: without it, a very quiet frame (e.g., room tone between words) could receive an extremely large gain boost, audibly amplifying background noise.

---

### earwax

> Apply a headphone spatialization effect that moves the stereo image outside the head, simulating speaker listening on headphones.

**Source:** [libavfilter/af_earwax.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_earwax.c)

The `earwax` filter adds head-related transfer function (HRTF) cues to stereo audio so that when listened to on headphones, the stereo image appears to come from in front of and around the listener rather than from inside the head. It processes 44.1kHz stereo audio (CD format) by applying cross-feed and spectral shaping. Ported from SoX.

## Quick Start

```sh
ffmpeg -i music.flac -af earwax output.wav
```

## Parameters

None. `earwax` takes no options.

## Examples

### Apply earwax to a music file

```sh
ffmpeg -i stereo.flac -af earwax -ar 44100 headphones.wav
```

### Real-time preview with ffplay

```sh
ffplay -i music.mp3 -af earwax
```

### Process and keep original as comparison

```sh
ffmpeg -i input.wav -af earwax processed.wav
ffplay input.wav &
ffplay processed.wav
```

## Notes

- `earwax` is designed specifically for **44.1kHz stereo** input — for other sample rates, resample first with `-ar 44100`.
- The effect is subjective and not universally preferred; some listeners find it distracting.
- For more control over stereo width and delay, use `haas` instead.
- Ported from the SoX audio toolkit's `earwax` effect.

---

### equalizer

> Apply a two-pole peaking EQ biquad filter to boost or cut a specific frequency band.

**Source:** [libavfilter/af_biquads.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_biquads.c)

The `equalizer` filter implements a standard two-pole peaking EQ — the same type found in hardware mixing consoles and digital audio workstations. It boosts or cuts a band of frequencies centered on a specified frequency, with the bandwidth controlled by the `width` parameter. Multiple `equalizer` instances can be chained in a single `-af` string to build a full parametric EQ.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "equalizer=f=1000:g=5:width_type=o:width=2" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Center frequency of the EQ band in Hz. (alias: `f`) |
| gain | double | 0.0 | Gain in dB to apply at the center frequency. Positive values boost, negative values cut. (alias: `g`) |
| width_type | int | q | How the `width` parameter is interpreted: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 1.0 | Bandwidth of the filter, in units determined by `width_type`. (alias: `w`) |
| mix | double | 1.0 | Wet/dry blend between filtered (1.0) and original (0.0) signal. (alias: `m`) |
| channels | string | all | Comma-separated list of channel names or numbers to apply the filter to. (alias: `c`) |
| normalize | bool | false | Normalize biquad filter coefficients to preserve 0 dB gain at DC. (alias: `n`) |
| transform | int | di | IIR filter transform type: `di` (direct form I), `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |
| blocksize | int | 0 | When > 0, process audio in blocks of this size for reduced latency (power-of-two values recommended). (alias: `b`) |

## Examples

### Boost presence at 3 kHz

A +4 dB boost at 3 kHz with a one-octave bandwidth adds clarity to vocals:

```sh
ffmpeg -i input.mp3 -af "equalizer=f=3000:g=4:width_type=o:width=1" output.mp3
```

### Cut muddiness at 300 Hz

A -6 dB notch at 300 Hz removes low-mid buildup common in room recordings:

```sh
ffmpeg -i input.mp3 -af "equalizer=f=300:g=-6:width_type=o:width=1" output.mp3
```

### Three-band parametric EQ

Chain multiple equalizer filters to create a full parametric EQ:

```sh
ffmpeg -i input.mp3 \
  -af "equalizer=f=80:g=3:width_type=o:width=1,equalizer=f=1000:g=-2:width_type=q:width=1.4,equalizer=f=8000:g=4:width_type=o:width=2" \
  output.mp3
```

### Precise Q-factor notch to remove a hum

A very narrow Q removes a 50 Hz mains hum without affecting surrounding frequencies:

```sh
ffmpeg -i input.wav -af "equalizer=f=50:g=-40:width_type=q:width=10" output.wav
```

### Apply EQ to the left channel only

```sh
ffmpeg -i input.mp3 -af "equalizer=f=2000:g=3:width_type=o:width=1:channels=FL" output.mp3
```

## Notes

- The `equalizer` filter is a peaking (bell) EQ only. For shelving or high/low-cut shapes use `highpass`, `lowpass`, `highshelf`, or `lowshelf`.
- Setting `width_type=q` with a high Q value (e.g., 30+) approximates a narrow notch filter, useful for removing tonal noise.
- Multiple `equalizer` instances on the same stream are processed in series; the order matters only when bands overlap significantly.
- The `texi_section` field in the source data is empty for this filter — details above are sourced from the FFmpeg biquad filter documentation and well-known defaults.

---

### extrastereo

> Widen or narrow the stereo image by linearly scaling the difference between left and right channels.

**Source:** [libavfilter/af_extrastereo.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_extrastereo.c)

The `extrastereo` filter widens or narrows the stereo field by scaling the difference between the left and right channels. A value above 1.0 exaggerates the stereo separation (wider), 1.0 is unchanged, 0.0 collapses to mono, and negative values swap or invert the channels. It is a simple and effective tool for adding perceived "width" or "air" to a stereo mix.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "extrastereo=m=2.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| m | float | `2.5` | Difference coefficient. 0 = mono, 1 = unchanged, >1 = wider, -1 = swap L/R. |
| c | bool | `1` | Enable clipping (prevent signal exceeding ±1.0). |

## Examples

### Wide stereo effect

```sh
ffmpeg -i stereo.mp3 -af "extrastereo=m=3.0" wide.mp3
```

### Mono collapse (m=0)

```sh
ffmpeg -i stereo.mp3 -af "extrastereo=m=0" mono.mp3
```

### Subtle widening

```sh
ffmpeg -i music.mp3 -af "extrastereo=m=1.5" wider.mp3
```

### Swap left and right channels

```sh
ffmpeg -i input.mp3 -af "extrastereo=m=-1" swapped.mp3
```

## Notes

- `m=0.0` averages both channels (mono); `m=1.0` passes audio unchanged; `m=2.5` (default) is a noticeably wider image.
- Very high values (>3.0) can cause clipping and phase issues — use with clipping enabled (`c=1`) to prevent distortion.
- For more control over stereo processing (M/S, balance, delay), use `stereotools` instead.
- This filter supports runtime commands for all options, allowing dynamic stereo width automation.

---

### flanger

> Apply a flanging effect to audio using a short modulated delay line.

**Source:** [libavfilter/af_flanger.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_flanger.c)

The `flanger` filter applies a flanging effect by mixing the original signal with a slightly delayed copy whose delay time is swept back and forth by a low-frequency oscillator. This creates a characteristic jet-engine or comb-filter sweep sound. It is similar to phasing but uses a physical delay line, producing a more pronounced and metallic-sounding effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "flanger" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| delay | double | `0.0` | Base delay in milliseconds. Range: 0–30. |
| depth | double | `2.0` | Swept delay range in milliseconds. Range: 0–10. |
| regen | double | `0.0` | Feedback percentage (regeneration). Range: -95–95. |
| width | double | `71.0` | Percentage of delayed signal mixed with original. Range: 0–100. |
| speed | double | `0.5` | LFO sweep rate in Hz. Range: 0.1–10. |
| shape | int | `sinusoidal` | LFO waveform: `triangular` or `sinusoidal`. |
| phase | double | `25.0` | Stereo phase difference 0–100 (%). Range: 0–100. |
| interp | int | `linear` | Interpolation for delay: `linear` or `quadratic`. |

## Examples

### Classic flanger

```sh
ffmpeg -i input.mp3 -af "flanger=delay=0:depth=2:regen=0:speed=0.5" output.mp3
```

### Fast jet-plane flanger

```sh
ffmpeg -i guitar.wav -af "flanger=speed=2:depth=4:regen=30" output.wav
```

### Stereo flanger with phase offset

```sh
ffmpeg -i input.mp3 -af "flanger=phase=50:speed=0.5:depth=2" output.mp3
```

### Negative feedback (hollow, metallic sound)

```sh
ffmpeg -i synth.mp3 -af "flanger=regen=-60:depth=3:speed=0.3" output.mp3
```

## Notes

- `regen` (feedback) is the primary control for intensity. Positive feedback creates resonant peaks; negative feedback creates notches. Values above ±70 can be very extreme.
- `depth` sets the range of delay sweep; larger values create a wider, more obvious sweep.
- Unlike `aphaser` (all-pass filters), flanger uses an actual delay line, which produces a stronger, more obvious effect — particularly on high-frequency content.
- `phase` controls the L/R stereo phase offset of the LFO; 90° creates a swirling stereo effect.

---

### haas

> Apply the Haas effect (precedence effect) to create stereo width from mono or narrow-stereo audio using inter-channel delays.

**Source:** [libavfilter/af_haas.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_haas.c)

The `haas` filter implements the Haas effect (also called the precedence effect) — a psychoacoustic technique that creates a sense of stereo width by introducing a small delay (typically 1–40ms) between channels. Applied to mono audio, it makes the signal appear to come from a wider soundstage. The filter gives independent control over the delay, gain, balance, and phase of each output channel.

## Quick Start

```sh
# Apply Haas effect to mono signal for stereo widening
ffmpeg -i mono.wav -af "haas" stereo.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain (linear). |
| level_out | double | `1.0` | Output gain (linear). |
| side_gain | double | `1.0` | Gain applied to the side (difference) component. |
| middle_source | int | `mid` | Middle source: `left`, `right`, `mid`, `side`. |
| middle_phase | bool | `false` | Invert phase of the middle channel. |
| left_delay | double | `2.05` | Left channel delay in milliseconds. |
| left_balance | double | `-1.0` | Left channel balance (−1 = full left). |
| left_gain | double | `1.0` | Left channel gain. |
| left_phase | bool | `false` | Invert phase of left channel. |
| right_delay | double | `2.12` | Right channel delay in milliseconds. |
| right_balance | double | `1.0` | Right channel balance (+1 = full right). |
| right_gain | double | `1.0` | Right channel gain. |
| right_phase | bool | `true` | Invert phase of right channel (default enabled). |

## Examples

### Basic stereo widening of mono signal

```sh
ffmpeg -i mono.wav -af haas widened.wav
```

### Custom delays for more pronounced effect

```sh
ffmpeg -i input.wav -af "haas=left_delay=5:right_delay=8" wider.wav
```

### Use left channel as middle source

```sh
ffmpeg -i input.wav -af "haas=middle_source=left" output.wav
```

### Stereo widening with gain adjustment

```sh
ffmpeg -i input.wav -af "haas=level_out=0.8:side_gain=1.5" output.wav
```

## Notes

- The Haas effect works best on **mono** or narrow-stereo signals; apply to a mid/side split for controlled widening of existing stereo.
- Delays under 40ms are perceived as stereo width (precedence effect); delays over 40ms become audible echoes.
- The asymmetric default delays (2.05ms left, 2.12ms right) add a subtle natural asymmetry.
- For simple time-based stereo effects, compare with `earwax` (HRTF-based) and `apulsator` (LFO-based panning).

---

### highpass

> Apply a high-pass biquad filter to attenuate frequencies below a specified cutoff frequency.

**Source:** [libavfilter/af_biquads.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_biquads.c)

The `highpass` filter attenuates frequencies below its cutoff (the 3 dB point) and passes frequencies above it largely unchanged. It is implemented as a biquad IIR filter and supports both single-pole (6 dB/octave) and two-pole (12 dB/octave) configurations. Common uses include removing low-frequency rumble, wind noise, or DC offset from recordings.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "highpass=f=200" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Cutoff frequency in Hz — the -3 dB point. (alias: `f`) |
| width_type | int | q | Interpretation of the `width` parameter: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 0.707 | Bandwidth or resonance of the filter, in units set by `width_type`. Only meaningful when `poles=2`. (alias: `w`) |
| poles | int | 2 | Number of filter poles. `1` gives a gentle 6 dB/octave roll-off; `2` gives a steeper 12 dB/octave roll-off. (alias: `p`) |
| mix | double | 1.0 | Wet/dry blend: 1.0 is fully filtered, 0.0 is the original signal. (alias: `m`) |
| channels | string | all | Channels to filter, e.g., `FL|FR`. (alias: `c`) |
| normalize | bool | false | Normalize filter coefficients so the passband gain is 0 dB. (alias: `n`) |
| transform | int | di | IIR transform type: `di`, `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |

## Examples

### Remove low-frequency rumble from a recording

A 100 Hz highpass is a standard rumble filter for voice and instrument recordings:

```sh
ffmpeg -i input.wav -af "highpass=f=100" output.wav
```

### Remove wind noise from a field recording

Wind noise typically concentrates below 200 Hz:

```sh
ffmpeg -i outdoor.mp3 -af "highpass=f=200" output.mp3
```

### Gentle single-pole roll-off

A single pole provides a subtle 6 dB/octave slope suitable for thinning a bass-heavy mix:

```sh
ffmpeg -i input.mp3 -af "highpass=f=150:poles=1" output.mp3
```

### Telephone or radio effect (combined with lowpass)

Bandpass a voice track to simulate a telephone by combining a highpass and lowpass:

```sh
ffmpeg -i voice.mp3 -af "highpass=f=300,lowpass=f=3400" telephone.mp3
```

### Apply only to the center channel in a 5.1 stream

```sh
ffmpeg -i surround.mp4 -af "highpass=f=80:channels=FC" output.mp4
```

## Notes

- The default two-pole configuration rolls off at 12 dB/octave below the cutoff. For a steeper slope, chain multiple `highpass` filters.
- The `width_type=q` default uses a Q of 0.707 (Butterworth response), which gives a maximally flat passband with no resonance peak. Higher Q values add resonance near the cutoff.
- This filter shares its implementation (`af_biquads.c`) with `lowpass`, `equalizer`, `highshelf`, `lowshelf`, and other biquad filters.
- The `texi_section` field in the source data is empty for this filter; parameters and defaults are sourced from the shared biquad implementation.

---

### loudnorm

> Normalize audio loudness to EBU R128 targets with optional two-pass linear mode.

**Source:** [libavfilter/af_loudnorm.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_loudnorm.c)

The `loudnorm` filter normalizes audio to EBU R128 loudness standards, targeting integrated loudness (LUFS), loudness range (LU), and true peak (dBTP). In single-pass mode it uses dynamic compression to hit targets in real time. In two-pass mode (`linear=true`), it first measures the file then applies a precise linear gain in the second pass — producing better quality with no dynamic processing.

## Quick Start

```sh
# Single-pass normalization to -23 LUFS (EBU R128)
ffmpeg -i input.mp3 -af "loudnorm=I=-23:TP=-1:LRA=7" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| I / i | double | `-24.0` | Integrated loudness target in LUFS (ITU-R BS.1770). Range: -70–-5. |
| LRA / lra | double | `7.0` | Loudness range target in LU. Range: 1–50. |
| TP / tp | double | `-2.0` | Maximum true peak in dBTP. Range: -9–0. |
| measured_I | double | — | Measured integrated loudness from first pass (enables linear mode). |
| measured_LRA | double | — | Measured loudness range from first pass. |
| measured_TP | double | — | Measured true peak from first pass. |
| measured_thresh | double | — | Measured threshold from first pass. |
| offset | double | `0.0` | Gain offset in LU to apply on top of normalization. |
| linear | bool | `true` | Use linear gain when first-pass measurements are provided. |
| dual_mono | bool | `false` | Treat mono content as dual-mono (applies +3 LU correction). |
| print_format | int | `none` | Output format: `none`, `json`, `summary`. Use `json` in first pass. |

## Examples

### Single-pass normalization (streaming/fast mode)

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.mp3
```

### Two-pass normalization (best quality)

**Pass 1** — measure the file:

```sh
ffmpeg -i input.mp3 -af "loudnorm=I=-23:TP=-2:LRA=7:print_format=json" -f null -
```

Capture the JSON output, then use the measured values in **Pass 2**:

```sh
ffmpeg -i input.mp3 -af \
  "loudnorm=I=-23:TP=-2:LRA=7:measured_I=-18.5:measured_LRA=9.2:measured_TP=-1.3:measured_thresh=-28.4:linear=true" \
  output.mp3
```

### Broadcast normalization to -23 LUFS

EBU R128 standard for broadcast.

```sh
ffmpeg -i voice.wav -af "loudnorm=I=-23:TP=-1:LRA=7" normalized.wav
```

### Streaming platform normalization (-14 LUFS)

Target for YouTube/Spotify/Apple Music.

```sh
ffmpeg -i music.mp3 -af "loudnorm=I=-14:TP=-1:LRA=11" streaming.mp3
```

## Notes

- The EBU R128 standard for broadcast is I=-23 LUFS, TP=-1 dBTP, LRA=7 LU. For online streaming, I=-14 LUFS is common.
- Single-pass (`linear=false`) uses dynamic processing (compression/limiting) which can affect transients. Two-pass linear mode preserves the original dynamics.
- `dual_mono=true` adds +3 LU to match how mono files measured in stereo containers are perceived by the R128 algorithm.
- The `print_format=json` output from pass 1 includes all measured_ values needed for pass 2. Parse the `[Parsed_loudnorm]` section of stderr.

---

### lowpass

> Apply a low-pass biquad filter to attenuate frequencies above a specified cutoff frequency.

**Source:** [libavfilter/af_biquads.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_biquads.c)

The `lowpass` filter attenuates frequencies above its cutoff (the 3 dB point) and passes lower frequencies unchanged. Like `highpass`, it uses a biquad IIR design and supports one or two poles. Common uses include anti-aliasing before downsampling, removing high-frequency noise or hiss, and creating a warm or muffled sound effect.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "lowpass=f=3000" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | double | — | Cutoff frequency in Hz — the -3 dB point. (alias: `f`) |
| width_type | int | q | Interpretation of the `width` parameter: `h` = Hz, `q` = Q-factor, `o` = octaves, `s` = slope, `k` = kHz. (alias: `t`) |
| width | double | 0.707 | Bandwidth or resonance of the filter, in units set by `width_type`. Only meaningful when `poles=2`. (alias: `w`) |
| poles | int | 2 | Number of filter poles. `1` gives a 6 dB/octave roll-off; `2` gives a 12 dB/octave roll-off. (alias: `p`) |
| mix | double | 1.0 | Wet/dry blend: 1.0 is fully filtered, 0.0 is the original signal. (alias: `m`) |
| channels | string | all | Channels to filter, e.g., `FL|FR`. (alias: `c`) |
| normalize | bool | false | Normalize filter coefficients so the passband gain is 0 dB. (alias: `n`) |
| transform | int | di | IIR transform type: `di`, `dii`, `tdii`, `latt`, `svf`, `zdf`. (alias: `a`) |
| precision | int | auto | Processing precision: `auto`, `s16`, `s32`, `f32`, `f64`. (alias: `r`) |

## Examples

### Remove high-frequency hiss

An 8 kHz cutoff reduces tape hiss and high-frequency noise while preserving most speech intelligibility:

```sh
ffmpeg -i noisy.wav -af "lowpass=f=8000" output.wav
```

### Telephone or radio bandpass (with highpass)

Combine `highpass` and `lowpass` to simulate a narrow telephony bandwidth:

```sh
ffmpeg -i voice.mp3 -af "highpass=f=300,lowpass=f=3400" telephone.mp3
```

### Warm up a harsh recording

A gentle 10 kHz cutoff rolls off harshness while keeping the sound natural:

```sh
ffmpeg -i guitar.mp3 -af "lowpass=f=10000:poles=1" warm.mp3
```

### Anti-aliasing before downsampling

Apply a low-pass before reducing the sample rate to avoid aliasing artifacts (FFmpeg often does this automatically via `aresample`, but explicit control is sometimes needed):

```sh
ffmpeg -i input_48k.flac -af "lowpass=f=20000,aresample=44100" output_44k.flac
```

### Partial mix for parallel processing

Blend 70% filtered with 30% dry signal to preserve some high-frequency detail:

```sh
ffmpeg -i input.mp3 -af "lowpass=f=5000:mix=0.7" output.mp3
```

## Notes

- The default two-pole (12 dB/octave) Butterworth response is the most common choice for transparent roll-off. Use `poles=1` for a subtler 6 dB/octave effect.
- Chain multiple `lowpass` instances to achieve steeper slopes (e.g., two two-pole filters in series give 24 dB/octave).
- This filter shares its implementation with `highpass` and the other biquad filters in `af_biquads.c`.
- The `texi_section` field in the source data is empty for this filter; parameters and defaults are sourced from the shared biquad implementation.

---

### mcompand

> Multiband dynamic range compressor/expander that splits audio into frequency bands and applies independent compander settings per band.

**Source:** [libavfilter/af_mcompand.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_mcompand.c)

The `mcompand` filter is a multiband dynamic range processor. It splits audio into frequency bands using 4th-order Linkwitz-Riley crossover filters (the same design used in loudspeaker crossovers, ensuring flat frequency response when all bands are combined at unity gain). Each band has independent attack/decay times and a compander transfer curve defined by input/output point pairs. This enables frequency-aware compression — for example, tighter control of low-frequency dynamics without affecting treble.

## Quick Start

```sh
# Two-band compander: different settings for bass and treble
ffmpeg -i input.wav -af "mcompand=args=0.005,0.1 6 -47/-40,-34/-34,-17/-33 | 0.003,0.05 6 -47/-40,-34/-34,-17/-33:crossover_freq=1500" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | string | — | Band definitions separated by `\|`. Each band: `attack,decay,[attack,decay] soft-knee points crossover_frequency [delay [init_volume [gain]]]`. |

## Band Syntax

```
attack,decay soft-knee points crossover_freq
```

- `attack,decay`: Attack and decay times in seconds
- `soft-knee`: Soft-knee width in dB
- `points`: Space-separated `in/out` dB point pairs defining the transfer curve
- `crossover_freq`: Upper crossover frequency of this band (Hz)

## Examples

### Simple two-band compression

```sh
ffmpeg -i input.wav \
  -af "mcompand=args=0.005,0.1 6 -47/-40,-34/-34,-17/-33 | 0.003,0.05 6 -47/-40,-34/-34,-17/-33:crossover_freq=1000" \
  output.wav
```

### Three-band with different ratios

```sh
ffmpeg -i music.wav \
  -af "mcompand=args=0.1,0.3 6 -50/-50,-30/-25,-15/-10 | 0.05,0.1 6 -50/-50,-30/-22,-15/-8 | 0.02,0.05 6 -50/-50,-30/-20,-15/-6:crossover_freq=200,2000" \
  mastered.wav
```

## Notes

- The `args` syntax is complex — refer to the `compand` filter documentation for point-pair transfer curve details.
- Because Linkwitz-Riley crossovers have flat summed response, the filter is transparent at unity gain (no transfer curve applied).
- For simpler single-band compression, use `compand` or `acompressor`.
- More bands = more CPU usage; two or three bands is typical for practical use.

---

### pan

> Remix, remap, or pan audio channels with arbitrary gain coefficients to produce any output channel layout.

**Source:** [libavfilter/af_pan.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_pan.c)

The `pan` filter provides full control over how input audio channels are combined into output channels. Unlike the `-ac` option, which applies a fixed automatic downmix, `pan` lets you specify exact gain coefficients for each output channel, making it suitable for custom stereo downmixes from surround sources, channel remapping, muting individual channels, and panning mono signals anywhere in a multi-channel layout.

## Quick Start

```sh
ffmpeg -i input.mp4 -af "pan=stereo|FL=FL|FR=FR" output.mp4
```

## Syntax

The filter takes a single string argument with the format:

```
pan=layout|out_ch=expr|out_ch=expr|...
```

- `layout`: output channel layout name (e.g., `stereo`, `5.1`, `mono`) or number of channels (e.g., `2`).
- `out_ch`: output channel name (`FL`, `FR`, `FC`, etc.) or number (`c0`, `c1`, …).
- `expr`: a sum of `[gain*]in_channel` terms. Use `+` or `-` to combine channels.
- Replace `=` with `<` to auto-normalize the gains for that output channel so their sum equals 1.

## Examples

### Stereo to mono with equal weight

```sh
ffmpeg -i stereo.mp3 -af "pan=1c|c0=0.5*c0+0.5*c1" mono.mp3
```

### Stereo to mono with more weight on the left

```sh
ffmpeg -i stereo.mp3 -af "pan=1c|c0=0.9*c0+0.1*c1" mono.mp3
```

### 5.1 to stereo downmix preserving surround information

The `<` operator normalizes the gains automatically to prevent clipping. Works for 3, 4, 5, and 7-channel sources:

```sh
ffmpeg -i surround.mp4 \
  -af "pan=stereo|FL<FL+0.5*FC+0.6*BL+0.6*SL|FR<FR+0.5*FC+0.6*BR+0.6*SR" \
  stereo.mp4
```

### 5.1 to stereo by keeping only front left and right

Pure channel remapping (no mixing) — FFmpeg detects this and uses a lossless copy path:

```sh
ffmpeg -i surround.mkv -af "pan=stereo|c0=FL|c1=FR" stereo.mkv
```

### Swap left and right channels in a stereo stream

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c0=c1|c1=c0" swapped.mp3
```

### Mute the left channel of a stereo stream

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c1=c1" muted_left.mp3
```

### Copy the right channel to both outputs

```sh
ffmpeg -i input.mp3 -af "pan=stereo|c0=FR|c1=FR" right_both.mp3
```

## Notes

- When all gain coefficients are 0 or 1 and each output channel draws from exactly one input channel, FFmpeg detects a "pure channel mapping" and uses a highly optimized, lossless path.
- The `pan` filter supports many formats (integer and float). For floating-point-only mixing of many inputs, `amix` can be more convenient.
- Named channel identifiers (`FL`, `FR`, `FC`, `LFE`, `BL`, `BR`, `SL`, `SR`) and numbered identifiers (`c0`, `c1`, …) cannot be mixed within a single channel specification.
- FFmpeg's built-in `-ac` downmix is preferred for standard conversions; use `pan` only when you need precise control over gain coefficients.

---

### sidechaincompress

> Apply dynamic range compression to audio where the gain reduction is triggered by a sidechain signal.

**Source:** [libavfilter/af_sidechaincompress.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_sidechaincompress.c)

The `sidechaincompress` filter compresses one audio stream based on the level of a second, independent "sidechain" signal. The classic application is "ducking": the background music is compressed whenever a voice-over signal is active, automatically lowering the music volume under speech. It requires `filter_complex` with two audio inputs: the signal to compress and the sidechain trigger.

## Quick Start

```sh
# Duck music under voice: music is compressed when voice is loud
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300[aout]" \
  -map "[aout]" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before compression. |
| mode | int | `downward` | `downward` (compress loud peaks) or `upward` (boost quiet signals). |
| threshold | double | `0.125` | Sidechain level at which compression begins (linear amplitude). |
| ratio | double | `2.0` | Compression ratio above the threshold. Range: 1–20. |
| attack | double | `20.0` | Time in ms for compression to engage when sidechain exceeds threshold. |
| release | double | `250.0` | Time in ms for compression to release when sidechain drops below threshold. |
| makeup | double | `1.0` | Post-compression gain multiplier. |
| knee | double | `2.828` | Soft-knee width in dB around the threshold. |
| link | int | `average` | Level detection link: `average` (mean of all channels) or `maximum`. |
| detection | int | `rms` | Sidechain level detection: `rms` or `peak`. |
| level_sc | double | `1.0` | Gain applied to the sidechain signal before level detection. |
| mix | double | `1.0` | Wet/dry mix (1.0 = fully compressed). |

## Examples

### Duck music when voice is active

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=6:attack=10:release=200[aout]" \
  -map "[aout]" output.mp3
```

### Aggressive ducking (ratio 20:1 ≈ limiting)

```sh
ffmpeg -i bg_music.mp3 -i narration.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.01:ratio=20:attack=5:release=300[out]" \
  -map "[out]" output.mp3
```

### Also normalise output volume after ducking

```sh
ffmpeg -i music.mp3 -i voice.mp3 \
  -filter_complex "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=4:attack=10:release=300:makeup=2[out]" \
  -map "[out]" output.mp3
```

## Notes

- The first input (`[0:a]`) is the audio to be compressed; the second (`[1:a]`) is the sidechain trigger (e.g. voice). The sidechain audio is NOT included in the output.
- `threshold` uses linear amplitude. For dBFS conversion: `linear = 10^(dBFS/20)`. A threshold of 0.02 ≈ -34 dBFS is suitable for activating on speech.
- `attack` and `release` are key for natural-sounding ducking: fast attack (5–20 ms), medium-slow release (200–500 ms).
- To duck on every audio channel simultaneously, use `link=average`; to trigger on only the loudest channel, use `link=maximum`.

---

### sidechaingate

> Apply a noise gate to audio where the gate is triggered by an external sidechain signal.

**Source:** [libavfilter/af_agate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_agate.c)

The `sidechaingate` filter applies a noise gate controlled by an external sidechain signal rather than the input signal itself. The gate opens when the sidechain exceeds the threshold and closes when it drops below. A classic use case is keying a reverb tail — when a dry vocal drops below the threshold, the reverb send is gated off. It requires `filter_complex` with two audio inputs.

## Quick Start

```sh
# Gate the reverb (second input) based on the dry signal (first input)
ffmpeg -i reverb.mp3 -i dry_signal.mp3 \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.02:attack=10:release=200[out]" \
  -map "[out]" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1.0` | Input gain before gating. Range: 0.015625–64. |
| mode | int | `downward` | Gate mode: `downward` (attenuate when sidechain is quiet) or `upward`. |
| range | double | `0.06125` | Attenuation when gate is closed. 0 = silence, 1 = passthrough. |
| threshold | double | `0.125` | Sidechain level at which the gate opens (linear amplitude). |
| ratio | double | `2.0` | Rate of attenuation below threshold. |
| attack | double | `20.0` | Time in ms for gate to open. |
| release | double | `250.0` | Time in ms for gate to close. |
| makeup | double | `1.0` | Output gain after gating. |
| knee | double | `2.828` | Soft-knee transition width in dB. |
| detection | int | `rms` | Sidechain level detection: `rms` or `peak`. |
| link | int | `average` | Multi-channel link: `average` or `maximum`. |

## Examples

### Gate reverb with dry vocal as sidechain

The reverb opens when the vocal is active, closes in the spaces between words.

```sh
ffmpeg -i reverb_return.wav -i dry_vocal.wav \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.02:attack=5:release=300:range=0[out]" \
  -map "[out]" gated_reverb.wav
```

### Duck noise floor using a reference signal

Gate background noise based on a click track or guide track.

```sh
ffmpeg -i noisy_bg.mp3 -i reference.mp3 \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.05:release=500[out]" \
  -map "[out]" output.mp3
```

### Tight sidechain gating (live performance)

Fast attack and release to gate a live instrument tightly.

```sh
ffmpeg -i guitar.wav -i pick_trigger.wav \
  -filter_complex "[0:a][1:a]sidechaingate=threshold=0.1:attack=2:release=50:range=0[out]" \
  -map "[out]" output.wav
```

## Notes

- The first input (`[0:a]`) is the audio to be gated; the second (`[1:a]`) is the sidechain trigger. Only the first stream appears in the output.
- `threshold` uses linear amplitude. For dBFS: `linear = 10^(dBFS/20)`. A threshold of 0.02 ≈ -34 dBFS.
- `range=0` completely silences the gated stream when closed. `range=0.06` (default) gives ~-24 dB attenuation.
- For gating triggered by the signal itself, use the simpler `agate` filter.

---

### silencedetect

> Detect silent intervals in an audio stream and emit timing metadata for each silence period.

**Source:** [libavfilter/af_silencedetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c)

The `silencedetect` filter analyzes an audio stream and logs a message and metadata whenever the signal level stays at or below a noise threshold for a minimum specified duration. The audio is passed through unmodified. The metadata keys it emits can be used by downstream filters (such as `ametadata`) to cut, split, or annotate the stream at silence boundaries.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise | double | -60dB (0.001) | Noise floor threshold. Frames at or below this level are considered silent. Accepts a linear amplitude value or a dB string (e.g., `-50dB`). (alias: `n`) |
| duration | duration | 2.0 | Minimum duration of silence in seconds before a silence event is reported. (alias: `d`) |
| mono | bool | false | When enabled, each channel is evaluated independently and separate metadata keys with a `.X` suffix are emitted per channel. (alias: `m`) |

## Metadata Output

The filter writes the following metadata keys to the frame that marks the end of a silence period (or when using `mono=1`, per-channel variants with a `.X` suffix):

| Key | Description |
|-----|-------------|
| `lavfi.silence_start` | Timestamp (in seconds) of the first frame of the silence period. |
| `lavfi.silence_end` | Timestamp of the first frame after the silence ends. |
| `lavfi.silence_duration` | Duration of the silence period in seconds. |

## Examples

### Detect silences longer than 0.5 seconds at -50 dB

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5" -f null -
```

### Detect silences with a very low noise tolerance (near-digital silence)

```sh
ffmpeg -i silence.mp3 -af "silencedetect=noise=0.0001" -f null -
```

### Log all silence intervals to a text file

Redirect FFmpeg's log output to capture the silence timestamps:

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-40dB:d=1" -f null - 2>&1 | grep silence
```

### Detect silence per channel separately

```sh
ffmpeg -i stereo.wav -af "silencedetect=n=-50dB:d=0.3:mono=1" -f null -
```

### Use metadata to split on silence boundaries

Combine with `ametadata` and `asegment` for practical audio splitting:

```sh
ffmpeg -i input.mp3 -af "silencedetect=n=-50dB:d=0.5,ametadata=print:file=silence_log.txt" -f null -
```

## Notes

- The filter passes audio through unchanged — it is a pure analysis filter and does not remove or modify samples.
- The noise threshold default of -60 dB (`0.001` linear) is suitable for most recordings. For very quiet sources or high-resolution audio, consider lowering it to `-70dB` or `-80dB`.
- The `duration` parameter controls the minimum silence length reported; very short values (below 0.1 s) may generate many false positives from breath sounds or room tone.
- When `mono=1`, silence in any single channel does not trigger the combined event — each channel is tracked independently with `.X`-suffixed metadata keys (e.g., `lavfi.silence_start.0`, `lavfi.silence_start.1`).

---

### silenceremove

> Remove silence from the beginning, end, or middle of audio based on configurable threshold and duration settings.

**Source:** [libavfilter/af_silenceremove.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silenceremove.c)

The `silenceremove` filter trims silence from the beginning, end, or middle of audio. Configurable threshold and duration settings control what counts as silence. The `start_periods` parameter controls how many silence periods to skip at the start (typically 1), and `stop_periods` controls the end (negative values enable silence removal from the middle of the audio).

## Quick Start

```sh
# Remove leading and trailing silence
ffmpeg -i padded.wav -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=1:stop_threshold=-50dB" trimmed.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_periods | int | `0` | Number of silence periods to skip at start before audio begins. 0 = disabled. |
| start_duration | duration | `0` | Min non-silence duration before trimming stops at start. |
| start_threshold | double | `0` | Silence threshold for start detection. In dB (e.g. `-50dB`) or amplitude ratio. |
| start_silence | duration | `0` | How much silence to keep at start after trimming. |
| start_mode | int | `any` | Multi-channel trigger: `any` (any non-silent channel) or `all` (all channels). |
| stop_periods | int | `0` | Silence periods to skip at end. Negative = remove middle silence (repeating). |
| stop_duration | duration | `0` | Min silence duration to trigger end trimming. |
| stop_threshold | double | `0` | Silence threshold for end detection. |
| stop_silence | duration | `0` | How much silence to keep at end after trimming. |
| detection | int | `avg` | Silence detection method: `avg` (RMS average) or `peak`. |
| window | duration | `0.02` | Duration of the detection window for silence measurement. |
| timestamp | int | `write` | Timestamp mode: `write` (update) or `copy` (preserve original). |

## Examples

### Remove leading silence only

```sh
ffmpeg -i input.wav -af "silenceremove=start_periods=1:start_threshold=-60dB" output.wav
```

### Remove leading and trailing silence

```sh
ffmpeg -i padded.wav \
  -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=1:stop_duration=0.1:stop_threshold=-50dB" \
  trimmed.wav
```

### Remove silence from the middle (podcast editing)

Use negative `stop_periods` to keep stripping silent gaps.

```sh
ffmpeg -i interview.wav \
  -af "silenceremove=stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB" \
  compact.wav
```

### Leave 0.1s of silence at start after trim

```sh
ffmpeg -i input.wav \
  -af "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1" \
  output.wav
```

## Notes

- `start_periods=1` removes silence up to and including the first non-silent period. Higher values skip N periods of silence (e.g. `2` removes the first silent section and the first audio section, then starts at the second audio).
- Negative `stop_periods` enables repeating removal of internal silence — effectively compacting the audio by removing all pauses above `stop_duration`.
- Threshold can be given in dB (`-50dB`) or amplitude ratio (`0.001`). dB format is easier to reason about for practical use.
- `detection=peak` reacts to the peak sample value; `detection=avg` uses RMS averaging for smoother behavior on transient-heavy audio.
- Always audition the result — aggressive settings can clip words or cut room tone that's needed for natural-sounding audio.

---

### stereotools

> Comprehensive stereo signal processor with M/S encoding/decoding, balance, phase inversion, delay, and stereo base control.

**Source:** [libavfilter/af_stereotools.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_stereotools.c)

The `stereotools` filter provides a comprehensive set of stereo processing utilities in a single filter: M/S (Mid/Side) encoding and decoding, input/output level and balance control, phase inversion, inter-channel delay, stereo base adjustment, and soft clipping. It is especially useful for mastering, broadcast loudness normalization, and correcting stereo recordings made in M/S microphone technique.

## Quick Start

```sh
# Convert M/S microphone recording to L/R
ffmpeg -i ms_recording.wav -af "stereotools=mode=ms>lr" output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| level_in | double | `1` | Input gain for both channels. Range: 0.015625–64. |
| level_out | double | `1` | Output gain for both channels. Range: 0.015625–64. |
| balance_in | double | `0` | Input balance (-1 = full left, +1 = full right). |
| balance_out | double | `0` | Output balance. |
| softclip | bool | `0` | Enable soft clipping (analog-style limiting). |
| mutel | bool | `0` | Mute left channel. |
| muter | bool | `0` | Mute right channel. |
| phasel | bool | `0` | Invert phase of left channel. |
| phaser | bool | `0` | Invert phase of right channel. |
| mode | int | `lr>lr` | Conversion mode (see below). |
| slev | double | `1` | Side signal level. Range: 0.015625–64. |
| mlev | double | `1` | Middle signal level. Range: 0.015625–64. |
| mpan | double | `0` | Middle signal pan (-1 to 1). |
| base | double | `0` | Stereo base (-1=inverted mono, 0=unchanged, 1=max width). |
| delay | double | `0` | Inter-channel delay in ms (±20 ms). |
| phase | double | `0` | Stereo phase in degrees (0–360). |
| bmode_in / bmode_out | int | `balance` | Balance mode: `balance`, `amplitude`, or `power`. |

### Mode Values

| Mode | Description |
|------|-------------|
| `lr>lr` | L/R to L/R (passthrough, default) |
| `lr>ms` | Encode L/R to M/S |
| `ms>lr` | Decode M/S to L/R |
| `lr>ll` | Duplicate left to both channels |
| `lr>rr` | Duplicate right to both channels |
| `lr>rl` | Swap L/R |

## Examples

### Decode M/S microphone recording

```sh
ffmpeg -i ms_mic.wav -af "stereotools=mode=ms>lr" lr_output.wav
```

### Karaoke effect (remove center/vocals)

```sh
ffmpeg -i music.mp3 -af "stereotools=mlev=0.015625" karaoke.mp3
```

### Widen stereo base

```sh
ffmpeg -i mix.mp3 -af "stereotools=base=0.5:slev=1.2" wider.mp3
```

### Fix phase issue on left channel

```sh
ffmpeg -i input.wav -af "stereotools=phasel=1" fixed.wav
```

### Swap L/R channels

```sh
ffmpeg -i input.wav -af "stereotools=mode=lr>rl" swapped.wav
```

## Notes

- `mode=ms>lr` is the key feature for M/S microphone recordings: Mid = sum (mono center), Side = difference (stereo width).
- `mlev=0.015625` (near zero) removes the center (Mid) signal, creating a karaoke-like effect that strips center-panned vocals.
- `base` adjusts stereo width without M/S conversion: `-1` = inverted mono, `0` = unchanged, `1` = maximum separation.
- `delay` (Haas effect) adds subtle timing offset between channels to widen perceived stereo space.
- Supports runtime commands for all options, enabling dynamic stereo processing automation.

---

### superequalizer

> Apply an 18-band graphic equalizer with bands spanning 65 Hz to 20 kHz, adjustable in dB per band.

**Source:** [libavfilter/af_superequalizer.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_superequalizer.c)

The `superequalizer` filter provides an 18-band graphic equalizer with fixed center frequencies spanning 65 Hz to 20 kHz. Each band gain is set in dB, defaulting to 1.0 (unity, 0 dB). It is the simplest way to apply broadband tonal shaping without the complexity of parametric EQ chains. Typical uses include voice enhancement, music frequency balancing, and correcting room acoustics.

## Quick Start

```sh
# Boost bass and reduce highs
ffmpeg -i input.wav -af "superequalizer=1b=3:2b=2:17b=0.5:18b=0.3" output.wav
```

## Parameters

| Band | Center Frequency | Band | Center Frequency |
|------|-----------------|------|-----------------|
| `1b` | 65 Hz | `10b` | 1480 Hz |
| `2b` | 92 Hz | `11b` | 2093 Hz |
| `3b` | 131 Hz | `12b` | 2960 Hz |
| `4b` | 185 Hz | `13b` | 4186 Hz |
| `5b` | 262 Hz | `14b` | 5920 Hz |
| `6b` | 370 Hz | `15b` | 8372 Hz |
| `7b` | 523 Hz | `16b` | 11840 Hz |
| `8b` | 740 Hz | `17b` | 16744 Hz |
| `9b` | 1047 Hz | `18b` | 20000 Hz |

All gains default to `1.0`. Values > 1.0 boost; values < 1.0 cut.

## Examples

### Bass boost

```sh
ffmpeg -i input.mp3 -af "superequalizer=1b=2.5:2b=2:3b=1.5" bass_boosted.mp3
```

### Voice clarity boost (presence at 2–5kHz)

```sh
ffmpeg -i voice.wav -af "superequalizer=11b=1.8:12b=2.0:13b=1.6:4b=0.7:5b=0.8" enhanced.wav
```

### Flat (default, no change)

```sh
ffmpeg -i input.wav -af superequalizer output.wav  # same as input
```

### Loudness curve (bass + treble boost, mid cut)

```sh
ffmpeg -i input.wav -af "superequalizer=1b=2:2b=1.8:3b=1.4:9b=0.8:10b=0.7:15b=1.3:16b=1.5" output.wav
```

## Notes

- Gain values are **linear** (not dB), where `1.0` = 0 dB, `2.0` ≈ +6 dB, `0.5` ≈ −6 dB.
- For parametric EQ with precise frequency, bandwidth, and gain control, use the `equalizer` filter instead.
- Combine multiple `equalizer` filter instances in a chain for more targeted shaping than `superequalizer` allows.
- Heavy boosting may cause clipping — follow with `volume` or `alimiter` if needed.

---

### tremolo

> Apply a tremolo effect by modulating the amplitude of audio at a set frequency and depth.

**Source:** [libavfilter/af_tremolo.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_tremolo.c)

The `tremolo` filter applies amplitude modulation (AM) to audio, creating a regular volume pulsation. It is the classic "tremolo arm" effect used on electric guitars and organ music. Unlike `vibrato` (which modulates pitch), tremolo modulates volume — making the sound swell and recede rhythmically.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "tremolo=f=5:d=0.8" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | double | `5.0` | Tremolo frequency in Hz. Range: 0.1–20000. |
| d | double | `0.5` | Depth as a fraction 0–1. 0 = no effect, 1 = silence on each down-cycle. |

## Examples

### Classic guitar tremolo (5 Hz, moderate depth)

```sh
ffmpeg -i guitar.wav -af "tremolo=f=5:d=0.6" output.wav
```

### Slow, deep swell effect

```sh
ffmpeg -i strings.wav -af "tremolo=f=1.5:d=0.9" output.wav
```

### Fast shimmering tremolo

```sh
ffmpeg -i keys.mp3 -af "tremolo=f=10:d=0.5" output.mp3
```

### Sync to tempo (120 BPM = 2 Hz for quarter notes)

```sh
ffmpeg -i input.mp3 -af "tremolo=f=2:d=0.7" output.mp3
```

## Notes

- `f` in Hz can be synced to musical tempo: frequency = BPM / 60 / beat_division (e.g. 120 BPM quarter notes = 120/60/1 = 2 Hz).
- `d=1.0` produces complete silence at the bottom of each cycle (full amplitude modulation). `d=0.3` is subtle.
- Tremolo modulates amplitude (volume); `vibrato` modulates frequency (pitch). Both use the same `f` and `d` parameters.
- For tube-amp-style tremolo with a slight asymmetry, combine with a very subtle `aphaser`.

---

### vibrato

> Apply a vibrato effect by modulating the frequency (pitch) of audio at a set rate and depth.

**Source:** [libavfilter/af_vibrato.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_vibrato.c)

The `vibrato` filter applies frequency modulation (FM) to audio, creating a regular pitch oscillation — the same effect used by singers and instrumentalists when they apply vibrato. Unlike `tremolo` (which modulates amplitude/volume), vibrato modulates pitch. The `f` parameter sets how fast the pitch oscillates, and `d` controls how wide the pitch swings.

## Quick Start

```sh
ffmpeg -i input.mp3 -af "vibrato=f=5:d=0.5" output.mp3
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | double | `5.0` | Vibrato frequency in Hz. Range: 0.1–20000. Typical musical range: 4–8 Hz. |
| d | double | `0.5` | Depth as a fraction 0–1. Controls the pitch swing width. |

## Examples

### Classic vocal vibrato

```sh
ffmpeg -i vocal.wav -af "vibrato=f=5.5:d=0.5" output.wav
```

### Deep, slow string-instrument vibrato

```sh
ffmpeg -i violin.wav -af "vibrato=f=3.5:d=0.7" output.wav
```

### Fast, shallow guitar vibrato

```sh
ffmpeg -i guitar.wav -af "vibrato=f=7:d=0.3" output.wav
```

### Extreme pitch wobble effect

```sh
ffmpeg -i input.mp3 -af "vibrato=f=8:d=1.0" output.mp3
```

## Notes

- `f` in Hz corresponds to the vibrato rate: 4–6 Hz is typical for vocal vibrato, 5–8 Hz for string instruments.
- `d=0.5` is a moderate depth; `d=1.0` is very wide pitch swing (almost a wobble/whammy effect); `d=0.2` is subtle.
- Vibrato modulates pitch (frequency); `tremolo` modulates volume (amplitude). Both use the same parameter names and ranges.
- For tempo-synced vibrato, calculate `f = BPM / 60 / beat_division` (e.g. 8th-note vibrato at 120 BPM = 4 Hz).

---

### volume

> Adjust the input audio volume using a scalar value, dB notation, or a dynamic expression.

**Source:** [libavfilter/af_volume.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_volume.c)

The `volume` filter changes the loudness of an audio stream by multiplying each sample by a configurable gain factor. It accepts simple numeric values, decibel strings like `6dB`, or full mathematical expressions that can reference per-frame variables such as timestamps. Use it whenever you need static level adjustment, loudness matching, or time-varying gain automation.

## Quick Start

```sh
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| volume | string | 1.0 | Volume adjustment expression. Accepts a linear multiplier (`0.5`), dB value (`-6dB`), or any AVExpr expression. |
| precision | int | float | Mathematical precision: `fixed` (8-bit fixed, limits formats to U8/S16/S32), `float` (32-bit, FLT), `double` (64-bit, DBL). |
| eval | int | once | When to evaluate the expression: `once` (at init or on command) or `frame` (every frame). |
| replaygain | int | drop | Behaviour when ReplayGain side data is present: `drop`, `ignore`, `track`, `album`. |
| replaygain_preamp | double | 0.0 | Pre-amplification in dB applied on top of the ReplayGain gain value. |
| replaygain_noclip | bool | true | When enabled, limits the gain to prevent clipping when using ReplayGain. |

## Expression Variables

When `eval=frame` is set, the `volume` expression is re-evaluated for every incoming audio frame. The following variables are available:

| Variable | Description |
|----------|-------------|
| `n` | Frame number, starting at 0. |
| `t` | Frame timestamp in seconds. |
| `nb_samples` | Number of samples in the current frame. |
| `nb_channels` | Number of audio channels. |
| `nb_consumed_samples` | Total samples consumed by the filter so far. |
| `pts` | Frame PTS (presentation timestamp). |
| `sample_rate` | Input sample rate. |
| `startpts` | PTS at the start of the stream. |
| `startt` | Time at the start of the stream. |
| `tb` | Timestamp timebase. |
| `volume` | The last volume value that was set. |

Note: when `eval=once`, only `sample_rate` and `tb` are valid; all other variables evaluate to NaN.

## Examples

### Halve the volume (three equivalent forms)

All three expressions produce the same result — a 6 dB reduction:

```sh
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4
ffmpeg -i input.mp4 -af "volume=1/2" output.mp4
ffmpeg -i input.mp4 -af "volume=-6.0206dB" output.mp4
```

### Boost volume by 6 dB with fixed-point precision

```sh
ffmpeg -i input.mp4 -af "volume=6dB:precision=fixed" output.mp4
```

### Fade volume to silence over 5 seconds starting at t=10

The expression evaluates to 1 before the 10-second mark, then linearly ramps to 0 over the following 5 seconds:

```sh
ffmpeg -i input.mp4 -af "volume='if(lt(t,10),1,max(1-(t-10)/5,0))':eval=frame" output.mp4
```

### Apply ReplayGain track gain from metadata

```sh
ffmpeg -i input.flac -af "volume=replaygain=track" output.flac
```

### Gradually increase volume from silence to full over the first 3 seconds

```sh
ffmpeg -i input.mp3 -af "volume='min(t/3,1)':eval=frame" output.mp3
```

## Notes

- Output samples are always clipped to the maximum value for the chosen format; use `precision=double` for the most headroom when processing large gain boosts.
- When `eval=frame` is used, the expression is parsed and evaluated for every single frame, which adds measurable CPU overhead on long files or high sample rates.
- Setting `volume=0` produces silence but does not remove the stream; use `-an` if you want to drop audio entirely.
- The `volume` command can be sent at runtime via the `sendcmd` filter or the `avfilter_graph_send_command` API, allowing dynamic adjustment without re-encoding.

---

## Test Sources

### aevalsrc

> Generate audio samples from a mathematical expression, allowing arbitrary waveform synthesis using FFmpeg's expression engine.

**Source:** [libavfilter/aeval.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/aeval.c)

The `aevalsrc` source generates audio by evaluating a mathematical expression for each sample. It supports multi-channel output with separate expressions per channel, and provides access to sample time (`t`), sample number (`n`), and sample rate (`s`) in the expression. This is the most flexible audio source — any waveform that can be expressed mathematically can be generated.

## Quick Start

```sh
# 440 Hz sine wave
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t)" -t 5 output.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exprs | string | — | `\|`-separated expressions, one per channel. **Required.** |
| channel_layout / c | string | (auto) | Output channel layout (e.g. `stereo`, `5.1`). |
| sample_rate / s | string | `44100` | Sample rate in Hz. |
| duration / d | duration | infinite | Total duration. |
| nb_samples / n | int | `1024` | Samples per output frame. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `n` | Sample number (starts at 0) |
| `t` | Time in seconds |
| `s` | Sample rate |

## Examples

### Simple 440 Hz sine wave

```sh
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t):s=48000" -t 5 sine.wav
```

### Stereo with different frequencies per channel

```sh
ffmpeg -f lavfi -i "aevalsrc=sin(440*2*PI*t)|sin(550*2*PI*t):c=stereo:s=44100" -t 5 stereo.wav
```

### Amplitude-modulated signal

```sh
ffplay -f lavfi "aevalsrc=sin(10*2*PI*t)*sin(880*2*PI*t):s=44100"
```

### White noise from random()

```sh
ffmpeg -f lavfi -i "aevalsrc=-2+random(0)" -t 5 whitenoise.wav
```

### 2.5 Hz binaural beats on a 360 Hz carrier

```sh
ffmpeg -f lavfi -i "aevalsrc=0.1*sin(2*PI*(360-1.25)*t)|0.1*sin(2*PI*(360+1.25)*t):c=stereo" -t 30 binaural.wav
```

### Silence

```sh
ffmpeg -f lavfi -i "aevalsrc=0" -t 5 silence.wav
```

## Notes

- Multiple channels are separated by `|` in the `exprs` string; `channel_layout` must match the number of expressions.
- Use `sin()`, `cos()`, `random()`, `floor()`, `mod()` and any FFmpeg math functions in expressions.
- `random(n)` returns a random value in [-1, 1] from PRNG seed `n` — useful for deterministic noise.
- For simple sine tones, `sine` source is simpler; `aevalsrc` is for custom/complex waveforms.

---

### allrgb

> Generate a 4096×4096 frame containing every possible 24-bit RGB color exactly once.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `allrgb` source generates a single 4096×4096 frame (16 million pixels) containing every possible 24-bit RGB color exactly once. It is a mathematically complete color space visualization, useful for testing LUT (Look Up Table) filters, color transforms, and any processing that needs to operate on the entire RGB gamut simultaneously. Output size is fixed at 4096×4096 and cannot be changed.

## Quick Start

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 allrgb.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Frames per second (for animated output). |
| duration / d | duration | infinite | Total duration. |

## Examples

### Export single frame as PNG

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 allrgb.png
```

### Apply a LUT and verify it covers all colors

```sh
ffmpeg -f lavfi -i "allrgb" -frames:v 1 -vf "lut3d=lut_file.cube" allrgb_graded.png
```

### Generate a short animated clip

```sh
ffmpeg -f lavfi -i "allrgb" -t 1 allrgb.mp4
```

## Notes

- Output is always 4096×4096 pixels — this cannot be resized with the `size` parameter (unlike other test sources).
- Each of the 16,777,216 pixels has a unique RGB value; the arrangement is space-filling curve order.
- `allyuv` is the YUV equivalent, generating all possible YUV color combinations.
- The output file will be large (~50 MB as lossless PNG); use with care.

---

### allyuv

> Generate a 4096×4096 frame containing every possible YUV color combination exactly once.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `allyuv` source generates a single 4096×4096 frame containing every possible YUV color combination exactly once — the YUV equivalent of `allrgb`. It is useful for testing color conversions, LUT filters, and chroma subsampling effects across the full YUV gamut. Output size is fixed at 4096×4096.

## Quick Start

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 allyuv.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |

## Examples

### Export as PNG

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 allyuv.png
```

### Apply YUV color grading and export

```sh
ffmpeg -f lavfi -i "allyuv" -frames:v 1 -vf "colorbalance=rs=0.1" allyuv_graded.png
```

## Notes

- Output is always fixed at 4096×4096 — the `size` parameter has no effect.
- Useful for verifying that color conversion filters preserve the full YUV gamut without clipping or banding.
- `allrgb` is the RGB-space equivalent.

---

### anoisesrc

> Generate a noise audio signal in various colors: white, pink, brown, blue, violet, or velvet noise.

**Source:** [libavfilter/asrc_anoisesrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/asrc_anoisesrc.c)

The `anoisesrc` source generates noise audio signals with selectable spectral color — white (flat spectrum), pink (−3 dB/octave), brown (−6 dB/octave), blue (+3 dB/octave), violet (+6 dB/octave), or velvet (sparse random spikes). Noise sources are used for acoustic testing, psychoacoustic masking tests, dithering reference signals, and creative audio design.

## Quick Start

```sh
# 30 seconds of pink noise
ffmpeg -f lavfi -i "anoisesrc=d=30:c=pink" pink_noise.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sample_rate / r | int | `48000` | Output sample rate in Hz. |
| amplitude / a | double | `1.0` | Amplitude (0.0–1.0). |
| duration / d | duration | infinite | Total duration. |
| color / colour / c | int | `white` | Noise color: `white`, `pink`, `brown`, `blue`, `violet`, `velvet`. |
| seed / s | int64 | random | PRNG seed for reproducible noise. |
| nb_samples / n | int | `1024` | Samples per output frame. |
| density | double | `0.05` | Density for velvet noise (0–1). |

## Examples

### White noise (flat spectrum)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=white:d=10" white_noise.wav
```

### Pink noise (most common for audio testing)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=pink:r=44100:a=0.5:d=60" pink_noise.wav
```

### Brown noise (deep rumble)

```sh
ffplay -f lavfi "anoisesrc=c=brown:r=44100"
```

### Velvet noise (sparse impulses, for reverb seeding)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=velvet:density=0.1:d=5" velvet.wav
```

### Reproducible noise (fixed seed)

```sh
ffmpeg -f lavfi -i "anoisesrc=c=pink:seed=42:d=10" repeatable.wav
```

## Notes

- **White**: flat power spectral density — equally loud at all frequencies (sounds harsh/hissy).
- **Pink**: −3 dB/octave — equal power per octave, matching human loudness perception (most natural-sounding noise).
- **Brown** (red): −6 dB/octave — deep, rumbling noise resembling a waterfall or ocean surf.
- **Blue**: +3 dB/octave — emphasizes high frequencies; sounds thin and bright.
- **Violet**: +6 dB/octave — very high-frequency emphasis; useful for dithering.
- **Velvet**: sparse random spikes at a given density; used in reverberation algorithms and spatial audio.

---

### cellauto

> Generate video from an elementary cellular automaton (Wolfram rules), producing evolving 1D patterns scrolled into a 2D video.

**Source:** [libavfilter/vsrc_cellauto.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_cellauto.c)

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

---

### life

> Simulate Conway's Game of Life (or generalized life rules) and render each generation as a video frame.

**Source:** [libavfilter/vsrc_life.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_life.c)

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

---

### mandelbrot

> Render an animated Mandelbrot set fractal that progressively zooms toward a configurable point.

**Source:** [libavfilter/vsrc_mandelbrot.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_mandelbrot.c)

The `mandelbrot` source renders the Mandelbrot set fractal and animates a smooth zoom toward a configurable complex-plane point. Both inner (set interior) and outer (escape time) coloring modes are configurable. The zoom is logarithmic from `start_scale` to `end_scale` over `end_pts` frames.

## Quick Start

```sh
ffplay -f lavfi "mandelbrot=size=800x600:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `640x480` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| start_x | double | `-0.7436...` | Initial real-axis position (zoom target). |
| start_y | double | `-0.1318...` | Initial imaginary-axis position. |
| start_scale | double | `3.0` | Initial scale (zoom out). |
| end_scale | double | `0.3` | Terminal scale (zoom in). |
| end_pts | double | `400` | Frame number at which zoom ends. |
| maxiter | int | `7189` | Maximum iterations per pixel (higher = sharper boundaries). |
| bailout | double | `10.0` | Escape radius. |
| inner | int | `mincol` | Interior coloring: `black`, `period`, `convergence`, `mincol`. |
| outer | int | `normalized_iteration_count` | Exterior coloring: `iteration_count`, `normalized_iteration_count`. |

## Examples

### Default zoom into the Seahorse Valley

```sh
ffplay -f lavfi "mandelbrot=size=800x600:rate=25"
```

### Zoom into the elephant valley

```sh
ffplay -f lavfi "mandelbrot=size=800x600:start_x=0.3:start_y=0.0:start_scale=0.5:end_scale=0.001"
```

### High-detail render

```sh
ffmpeg -f lavfi -i "mandelbrot=size=1920x1080:rate=25:maxiter=20000" -t 16 fractal.mp4
```

### Black interior, slower zoom

```sh
ffplay -f lavfi "mandelbrot=size=800x600:inner=black:end_pts=800"
```

## Notes

- The default zoom target (`start_x`, `start_y`) is the tip of the Seahorse Valley, a famous fractal detail region.
- Increase `maxiter` for sharper, more detailed boundaries — but each doubling roughly doubles render time.
- `normalized_iteration_count` outer coloring produces smooth color gradients; `iteration_count` produces banded coloring.
- The zoom is exponential — `end_scale / start_scale` gives the total zoom factor.

---

### pal100bars

> Generate EBU PAL 100% color bars for European broadcast calibration.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `pal100bars` source generates EBU (European Broadcasting Union) PAL color bars at 100% amplitude. Unlike `pal75bars` (75% amplitude) and the SMPTE variants, PAL 100% bars drive the color components to full amplitude, making them useful for peak signal level testing and gamut verification on European broadcast equipment.

## Quick Start

```sh
ffplay -f lavfi "pal100bars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### PAL SD 100% bars

```sh
ffplay -f lavfi "pal100bars=size=720x576:rate=25"
```

### Generate bars clip

```sh
ffmpeg -f lavfi -i "pal100bars=size=720x576:rate=25" -t 10 pal100bars.mp4
```

## Notes

- EBU PAL 100% bars: all seven color bars at 100% amplitude (white, yellow, cyan, green, magenta, red, blue).
- Use `pal75bars` for the more common 75% level variant used in standard PAL test recordings.
- SMPTE bars (`smptebars`, `smptehdbars`) are the North American equivalents.

---

### pal75bars

> Generate EBU PAL 75% color bars — the standard European broadcast test signal for monitor calibration.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `pal75bars` source generates EBU PAL 75% color bars — the standard European broadcast test signal. The 75% amplitude is the EBU recommended level for color bar generators, matching the output of most European broadcast equipment and VTR leaders. These are the go-to bars for calibrating PAL monitors and VTR decks.

## Quick Start

```sh
ffplay -f lavfi "pal75bars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard PAL 75% bars

```sh
ffplay -f lavfi "pal75bars=size=720x576:rate=25"
```

### Embed as test leader in a PAL production file

```sh
ffmpeg -f lavfi -i "pal75bars=size=720x576:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 60 -pix_fmt yuv420p leader.mov
```

## Notes

- 75% bars are the EBU standard for PAL broadcast test recordings; `pal100bars` provides full-amplitude bars.
- The seven color patches are: white, yellow, cyan, green, magenta, red, blue — all at 75% of peak amplitude.
- Use with `vectorscope` to verify the bars land on their expected targets in the scope.

---

### rgbtestsrc

> Generate an RGB test pattern with red, green, and blue vertical stripes for verifying channel ordering.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `rgbtestsrc` source generates a simple test pattern with red, green, and blue vertical stripes from top to bottom. It is primarily used to diagnose RGB channel order issues — if the red stripe appears blue and vice versa, the input/output channel mapping is swapped.

## Quick Start

```sh
ffplay -f lavfi "rgbtestsrc=size=640x480"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Check RGB channel order

```sh
ffplay -f lavfi "rgbtestsrc=size=640x480"
```

### Generate a single test frame

```sh
ffmpeg -f lavfi -i "rgbtestsrc=size=640x480" -frames:v 1 rgb_test.png
```

### Verify a codec/container preserves colors

```sh
ffmpeg -f lavfi -i "rgbtestsrc=size=640x480:rate=1" -t 1 test.mov
ffplay test.mov
```

## Notes

- You should see three horizontal bands from top to bottom: **red**, **green**, **blue**.
- If the red and blue bands are swapped, the pixel format has reversed RGB channel order (a common issue with some codecs or pixel format conversions).
- `yuvtestsrc` generates the equivalent Y/Cb/Cr stripe pattern for YUV format diagnostics.

---

### sine

> Generate a pure sine wave audio signal at a configurable frequency, with an optional periodic beep.

**Source:** [libavfilter/asrc_sine.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/asrc_sine.c)

The `sine` source generates a bit-exact sine wave audio signal at a specified frequency. It is the standard way to produce a test tone in FFmpeg — commonly used as a 1 kHz calibration tone in broadcast leaders, or as a reference signal for audio testing. An optional periodic beep at a harmonic frequency can also be enabled.

## Quick Start

```sh
# 1 kHz test tone for 10 seconds
ffmpeg -f lavfi -i "sine=frequency=1000:duration=10" tone_1khz.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency / f | double | `440` | Carrier frequency in Hz. |
| beep_factor / b | double | `0` | Periodic beep at `frequency × beep_factor` Hz (0 = disabled). |
| sample_rate / r | int | `44100` | Output sample rate in Hz. |
| duration / d | duration | infinite | Total duration. |
| samples_per_frame | expression | `1024` | Samples per output frame. |

## Examples

### 1 kHz broadcast test tone

```sh
ffmpeg -f lavfi -i "sine=frequency=1000:sample_rate=48000" -t 60 tone.wav
```

### 440 Hz concert A with beep every second at 880 Hz

```sh
ffplay -f lavfi "sine=frequency=440:beep_factor=2"
```

### 220 Hz with 880 Hz beep, 5 second duration

```sh
ffmpeg -f lavfi -i "sine=f=220:b=4:d=5" sine_test.wav
```

### Pair with SMPTE bars for a broadcast leader

```sh
ffmpeg -f lavfi -i "smptehdbars=size=1920x1080:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 60 broadcast_leader.mxf
```

## Notes

- The output amplitude is fixed at 1/8 (approximately -18 dBFS) — a standard reference level for broadcast.
- `beep_factor=2` gives a beep at double the carrier frequency (one octave up); `beep_factor=4` gives two octaves up.
- Specify `sample_rate=48000` for broadcast work (48 kHz is the professional audio standard).
- The signal is bit-exact — the same settings will always produce identical samples.

---

### smptebars

> Generate SMPTE EG 1-1990 standard-definition color bars for broadcast calibration and signal testing.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `smptebars` source generates the classic SMPTE EG 1-1990 color bar pattern used in SD (standard definition) broadcast for monitor calibration, signal level testing, and tape leader. The pattern includes the 7 standard colors at 75% amplitude plus the PLUGE sub-black test signal in the lower section.

## Quick Start

```sh
ffplay -f lavfi "smptebars=size=720x576:rate=25"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard PAL SD color bars

```sh
ffplay -f lavfi "smptebars=size=720x576:rate=25"
```

### Standard NTSC SD color bars

```sh
ffplay -f lavfi "smptebars=size=720x480:rate=30000/1001"
```

### Generate a 10-second bars clip with tone

```sh
ffmpeg -f lavfi -i "smptebars=size=720x576:rate=25" \
       -f lavfi -i "sine=frequency=1000:sample_rate=48000" \
       -t 10 bars_with_tone.mp4
```

### Single frame for documentation

```sh
ffmpeg -f lavfi -i "smptebars=size=1280x720" -frames:v 1 smptebars.png
```

## Notes

- Based on SMPTE EG 1-1990 for SD content. For HD use `smptehdbars` (SMPTE RP 219-2002).
- The pattern includes 7 standard color bars (white, yellow, cyan, green, magenta, red, blue) at 75% amplitude plus the PLUGE signal (sub-black, black, super-black) in the lower portion.
- PLUGE is used for CRT monitor black level calibration; in modern workflows it is less critical but still standard for tape leaders.
- Pair with a 1 kHz sine tone (`sine=frequency=1000`) for a complete broadcast test leader.

---

### smptehdbars

> Generate SMPTE RP 219-2002 high-definition color bars for HD broadcast calibration and signal testing.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

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

---

### testsrc

> Generate an animated test video pattern showing color bars, a scrolling gradient, and a frame timestamp counter.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `testsrc` source generates an animated test video pattern with a color patch grid, a scrolling gradient bar, and a live frame-number counter. It is mainly used for pipeline testing, format verification, and building filter graphs without needing a real input file. All video test sources share the same common parameters (`size`, `rate`, `duration`, `sar`).

## Quick Start

```sh
# 10-second 1080p test pattern at 30fps
ffmpeg -f lavfi -i "testsrc=size=1920x1080:rate=30" -t 10 output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. Accepts named sizes (`hd1080`, `vga`) or `WxH`. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. Omit for infinite stream. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Standard definition test pattern (PAL)

```sh
ffplay -f lavfi "testsrc=size=720x576:rate=25"
```

### Generate 5 seconds as PNG images

```sh
ffmpeg -f lavfi -i "testsrc=size=640x480:rate=1" -t 5 frame_%04d.png
```

### Use as input in a filter_complex

```sh
ffmpeg -f lavfi -i "testsrc=size=1280x720:rate=30" -vf "drawtext=text='Hello'" -t 5 out.mp4
```

### Generate a single frame

```sh
ffmpeg -f lavfi -i "testsrc=size=1920x1080" -frames:v 1 test_frame.png
```

## Notes

- The pattern includes: a 7-color bar section, a scrolling luminance gradient, a 100% white box, and a frame counter in the bottom-right corner.
- `testsrc2` supports more pixel formats (beyond `rgb24`) and is preferred when testing filters that operate on YUV or high bit-depth formats.
- All video test sources (`smptebars`, `rgbtestsrc`, `yuvtestsrc`, etc.) accept the same `size`, `rate`, `duration`, `sar` parameters.
- Use `-f lavfi` when specifying the source on the command line; in `-filter_complex` it is used directly as `[testsrc=...]`.

---

### testsrc2

> Generate an animated test video pattern similar to testsrc but with support for a wider range of pixel formats.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `testsrc2` source is nearly identical to `testsrc` but supports more pixel formats beyond the `rgb24` that `testsrc` is limited to. This makes it the preferred choice when testing filters that operate on YUV, planar, or high bit-depth pixel formats, since it avoids a forced format conversion before the test filter.

## Quick Start

```sh
ffplay -f lavfi "testsrc2=size=1280x720:rate=30"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Test a YUV-native filter without format conversion

```sh
ffmpeg -f lavfi -i "testsrc2=size=1280x720:rate=25" -vf "unsharp" -t 5 out.mp4
```

### Generate 10-bit test frames

```sh
ffmpeg -f lavfi -i "testsrc2=size=1920x1080:rate=25" -pix_fmt yuv420p10le -t 5 out.mkv
```

### Preview in ffplay

```sh
ffplay -f lavfi "testsrc2=size=640x480:rate=30"
```

## Notes

- Prefer `testsrc2` over `testsrc` when testing filters on YUV or non-RGB pixel formats.
- The visual pattern is the same as `testsrc`: color grid, scrolling gradient, frame counter.
- Both `testsrc` and `testsrc2` produce an animated pattern; use `-frames:v 1` for a single still frame.

---

### yuvtestsrc

> Generate a YUV test pattern with Y, Cb, and Cr vertical stripes for verifying YUV channel ordering.

**Source:** [libavfilter/vsrc_testsrc.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vsrc_testsrc.c)

The `yuvtestsrc` source generates a test pattern with Y (luma), Cb, and Cr (chroma) vertical stripes, useful for verifying that YUV components are mapped correctly and that chroma channel ordering is preserved through a processing pipeline.

## Quick Start

```sh
ffplay -f lavfi "yuvtestsrc=size=640x480"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `320x240` | Output frame size. |
| rate / r | video_rate | `25` | Frames per second. |
| duration / d | duration | infinite | Total duration. |
| sar | rational | `1/1` | Sample aspect ratio. |

## Examples

### Verify YUV channel order

```sh
ffplay -f lavfi "yuvtestsrc=size=640x480"
```

### Generate a single YUV test frame

```sh
ffmpeg -f lavfi -i "yuvtestsrc=size=640x480" -frames:v 1 yuv_test.png
```

### Test YUV format round-trip

```sh
ffmpeg -f lavfi -i "yuvtestsrc=size=640x480:rate=1" -pix_fmt yuv420p -t 1 test.mkv
ffplay test.mkv
```

## Notes

- You should see three horizontal bands: **Y (luma)**, **Cb**, **Cr** from top to bottom.
- If the Cb and Cr stripes appear swapped, the chroma plane ordering in the pixel format is reversed.
- Use `rgbtestsrc` for testing RGB channel ordering instead.

---

## Visualization

### a3dscope

> Render audio samples as a 3D waveform scope video, displaying amplitude over time in a 3D rotating view.

**Source:** [libavfilter/avf_a3dscope.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_a3dscope.c)

The `a3dscope` filter converts audio into a 3D waveform visualization rendered as a video stream. The audio waveform is displayed in three dimensions with configurable camera angles, field of view, and zoom. The result is an animated 3D scope view that rotates through samples over time — primarily used for artistic audio visualizations.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,a3dscope"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `800x600` | Output video size. |
| fov | float | `90.0` | Field of view (degrees). |
| roll | float | `0.0` | Camera roll angle (degrees). |
| pitch | float | `0.0` | Camera pitch angle (degrees). |
| yaw | float | `0.0` | Camera yaw angle (degrees). |
| xzoom | float | `1.0` | Zoom on X axis. |
| yzoom | float | `1.0` | Zoom on Y axis. |
| zzoom | float | `1.0` | Zoom on Z axis. |
| xpos | float | `0.0` | X position offset. |
| ypos | float | `0.0` | Y position offset. |
| zpos | float | `0.0` | Z position offset. |
| length | int | `15` | Number of audio segments to render. |

## Examples

### Basic 3D scope

```sh
ffplay -f lavfi "amovie=music.mp3,a3dscope=size=800x600"
```

### Angled view

```sh
ffplay -f lavfi "amovie=music.mp3,a3dscope=pitch=30:yaw=45"
```

### Save 3D scope video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]a3dscope=size=1280x720[v]" \
  -map "[v]" scope3d.mp4
```

## Notes

- `a3dscope` is primarily artistic — for technical audio analysis, use `showwaves`, `showfreqs`, or `aphasemeter`.
- Adjust `fov` (default 90°) to widen or narrow the perspective; higher values give a more dramatic effect.
- `length` controls how many past audio segments are visible — higher values show more history.

---

### abitscope

> Visualize audio sample bit patterns as a video scope, showing which bits are active across samples.

**Source:** [libavfilter/avf_abitscope.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_abitscope.c)

The `abitscope` filter renders a video visualization of the bit patterns in audio samples. Each horizontal row represents a bit position (MSB at top), and the display scrolls in time showing which bits are set across samples. It is primarily useful for analyzing the true bit depth of audio — distinguishing between genuine 24-bit content and 16-bit audio upsampled to 24-bit (which shows blank lower bits).

## Quick Start

```sh
ffplay -f lavfi "amovie=input.wav,abitscope"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `512x256` | Output video size. |
| colors | string | `red\|green\|blue\|…` | Per-channel colors. |
| mode / m | int | `combined` | Channel display: `combined` or `separate`. |

## Examples

### Inspect bit depth of a WAV file

```sh
ffplay -f lavfi "amovie=audio.wav,abitscope=size=800x400"
```

### Separate channel display

```sh
ffplay -f lavfi "amovie=stereo.flac,abitscope=mode=separate"
```

### Save bit scope video

```sh
ffmpeg -i input.wav \
  -filter_complex "[0:a]abitscope=size=512x256[v]" \
  -map "[v]" bitscope.mp4
```

## Notes

- Genuine 24-bit audio shows activity down to the lowest bit rows; upsampled 16-bit audio shows the bottom 8 rows as blank.
- The display is most informative for uncompressed PCM sources (WAV, FLAC, AIFF).
- For waveform and frequency visualization, `showwaves` and `showfreqs` are more commonly used.

---

### aphasemeter

> Render a stereo phase correlation meter (Lissajous-style) as a video stream, showing the stereo phase relationship between left and right channels.

**Source:** [libavfilter/avf_aphasemeter.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_aphasemeter.c)

The `aphasemeter` filter renders a stereo phase meter — a Lissajous-style display where left and right audio channels drive the X and Y axes. When the stereo image is perfectly mono (identical channels), dots cluster on the vertical center line. Wide stereo spreads diagonally, while out-of-phase content spreads horizontally. It can optionally detect and log "out-of-phase" conditions where mono sum would cause cancellation. The audio passes through unchanged.

## Quick Start

```sh
ffplay -f lavfi "amovie=stereo.mp3,aphasemeter"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| size / s | image_size | `800x400` | Output video size. |
| rc | int | `2` | Red component of phase dot color. |
| gc | int | `7` | Green component of phase dot color. |
| bc | int | `1` | Blue component of phase dot color. |
| mpc | color | `orange` | Color for the out-of-phase indicator. |
| video | bool | `1` | Enable video output. |
| phasing | bool | `0` | Enable out-of-phase detection. |
| tolerance / t | float | `0.0` | Phase tolerance (0–1) before triggering out-of-phase alert. |
| angle / a | float | `170.0` | Angle (degrees) defining the out-of-phase detection zone. |
| duration / d | duration | `2s` | Duration before triggering an out-of-phase event. |

## Examples

### Basic phase meter

```sh
ffplay -f lavfi "amovie=stereo.flac,aphasemeter"
```

### With out-of-phase detection

```sh
ffmpeg -i stereo.wav -af "aphasemeter=phasing=1:duration=1" -f null - 2>&1 | grep phase
```

### Combine phase meter with audio in output

```sh
ffmpeg -i stereo.mp3 \
  -filter_complex "[0:a]aphasemeter=size=400x200,format=yuva420p[scope];[0:a]anull[aud]" \
  -map "[scope]" -map "[aud]" output.mp4
```

### Save phase meter video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]aphasemeter=size=600x300[v]" \
  -map "[v]" phasemeter.mp4
```

## Notes

- A vertical line indicates perfectly mono-compatible audio; a horizontal spread indicates out-of-phase content that will cancel when summed to mono.
- Enable `phasing=1` to log metadata events when extended out-of-phase conditions are detected — useful for broadcast QC.
- The Lissajous display is the industry-standard tool for checking stereo compatibility before broadcast or streaming.
- For mono content, all dots will appear on the center diagonal (Y = X line).

---

### ciescope

> Overlay a CIE 1931 chromaticity diagram on video to visualize the color gamut and distribution of pixel colors.

**Source:** [libavfilter/vf_ciescope.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_ciescope.c)

The `ciescope` filter renders a CIE 1931 xy chromaticity diagram and plots the colors present in the input video onto it. The horseshoe-shaped diagram represents all visible colors, with white at the center. Each video frame's pixel colors appear as dots or a heatmap, showing how the content's gamut compares to standard color spaces (sRGB, DCI-P3, BT.2020, etc.). It is used in color grading QC to verify gamut compliance and spot out-of-gamut colors.

## Quick Start

```sh
ffplay -i input.mp4 -vf ciescope
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| system | int | `hdtv` | Reference color system to display: `ntsc`, `470m`, `ebu`, `470bg`, `smpte`, `240m`, `film`, `hdtv`, `cie1931`, `2020`, `dcip3`. |
| cie | int | `xyy` | CIE diagram type: `xyy`, `ucs`, `luv`. |
| gamuts | flags | `0` | Additional gamut triangles to overlay (bitfield: 1=ntsc, 2=470m, …). |
| size / s | image_size | `512x512` | Output size of the scope image. |
| intensity / i | float | `0.001` | Intensity of each plotted pixel dot. |
| fill | bool | `1` | Fill the chromaticity diagram with the visible spectrum colors. |

## Examples

### Basic CIE scope overlay on video

```sh
ffplay -i input.mp4 -vf ciescope
```

### Show BT.2020 gamut triangle with sRGB reference

```sh
ffplay -i input.mp4 -vf "ciescope=system=hdtv:gamuts=0x40"
```

### Save first 10 seconds of CIE scope video

```sh
ffmpeg -i input.mp4 -vf ciescope -t 10 cie_scope.mp4
```

### Increase dot intensity for sparse colors

```sh
ffplay -i input.mp4 -vf "ciescope=intensity=0.01:size=800x800"
```

## Notes

- Colors outside the displayed gamut triangle are outside that color space — useful for checking HDR/wide-gamut content.
- Low `intensity` values prevent overexposure with bright or saturated content; increase for low-saturation material.
- The filter shows all frame pixels simultaneously — use a representative frame or clip for meaningful results.
- See also `vectorscope` for a vectorscope-style display that is more common in broadcast grading workflows.

---

### showcqt

> Render an audio stream as an animated Constant-Q Transform (CQT) spectrogram video, showing frequency content on a musical scale.

**Source:** [libavfilter/avf_showcqt.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_showcqt.c)

The `showcqt` filter converts audio to a real-time spectrogram video using the Constant-Q Transform — a frequency analysis that spaces bins logarithmically, aligning with musical octaves and note intervals. The display can combine a scrolling sonogram (time-frequency heatmap) with a bar graph of instantaneous spectrum. Unlike FFT visualizers, `showcqt` maps frequency linearly to pitch, making it ideal for music analysis and visualization.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showcqt"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `1920x1080` | Output video size. |
| fps / rate / r | video_rate | `25` | Output frame rate. |
| bar_h | int | `-1` | Bar graph height (auto if −1). |
| axis_h | int | `-1` | Axis label height (auto if −1). |
| sono_h | int | `-1` | Sonogram height (auto if −1). |
| volume / sono_v | string | `16` | Sonogram volume (brightness) expression. |
| bar_v / volume2 | string | `sono_v` | Bar graph volume expression. |
| gamma / sono_g | float | `3.0` | Sonogram gamma correction. |
| basefreq | double | `20.01523...` | Lowest displayed frequency (Hz). |
| endfreq | double | `20495.6...` | Highest displayed frequency (Hz). |
| tlength | string | `384*tc/(384+tc*f)` | Per-frequency transform length expression. |
| count | int | `6` | Number of transform passes per frame. |
| fontcolor | string | `st(0,…)` | Axis label color expression. |
| cscheme | string | `1|0.5|0|0|0.5|1` | Color scheme (`R|G|B|R|G|B` for low/high). |

## Examples

### Basic visualization with ffplay

```sh
ffplay -f lavfi "amovie=music.flac,showcqt=size=1920x1080:count=4"
```

### Save spectrogram video

```sh
ffmpeg -i music.mp3 \
  -filter_complex "[0:a]showcqt=size=1280x720:fps=25[v]" \
  -map "[v]" -c:v libx264 cqt.mp4
```

### Only show bar graph (no sonogram)

```sh
ffplay -f lavfi "amovie=music.mp3,showcqt=sono_h=0:bar_h=400:axis_h=50"
```

### Custom color scheme (green tones)

```sh
ffplay -f lavfi "amovie=music.mp3,showcqt=cscheme=0|1|0|0|0.5|0"
```

## Notes

- `showcqt` is computationally expensive; reduce `count` or `size` for real-time use on slower machines.
- The frequency axis spans piano key range by default (A0 to C8 approximately).
- Combine with `[0:a]showcqt[v];[0:a][0:v]…` to get synchronized audio/video in one output.
- `tlength` controls the time-frequency trade-off: longer = better frequency resolution, shorter = better time resolution.

---

### showfreqs

> Render a real-time FFT frequency spectrum of an audio stream as a video, with configurable modes, scales, and windowing.

**Source:** [libavfilter/avf_showfreqs.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_showfreqs.c)

The `showfreqs` filter renders an FFT-based frequency spectrum display as a video stream. Unlike `showcqt` (which uses a constant-Q transform), `showfreqs` uses a standard FFT with configurable window size, making it suitable for general-purpose spectrum analysis. It supports both bar and line display modes, linear/log frequency and amplitude scales, and per-channel coloring.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showfreqs=size=800x400:mode=bar"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `1080x430` | Output video size. |
| rate / r | video_rate | `25` | Output frame rate. |
| mode | int | `bar` | Display mode: `bar`, `dot`, `line`, `filledline`. |
| ascale | int | `log` | Amplitude scale: `lin`, `log`, `bark`, `mel`. |
| fscale | int | `lin` | Frequency scale: `lin`, `log`, `rlog`. |
| win_size | int | `2048` | FFT window size (power of 2: 32–65536). |
| overlap | float | `1.0` | Window overlap (0–1). |
| averaging | int | `1` | Number of frames to time-average. |
| colors | string | `red\|green\|…` | Per-channel colors. |
| cmode | int | `combined` | Channel mode: `combined` or `separate`. |
| minamp | float | `1e-6` | Minimum amplitude for log scale. |
| data | int | `magnitude` | Display: `magnitude` or `phase`. |
| channels | string | `all` | Which channels to display. |

## Examples

### Bar spectrum with log frequency scale

```sh
ffplay -f lavfi "amovie=music.mp3,showfreqs=size=1280x480:mode=bar:fscale=log"
```

### Separate channels

```sh
ffplay -f lavfi "amovie=stereo.flac,showfreqs=cmode=separate:mode=line"
```

### Save spectrum video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]showfreqs=size=1280x720:mode=bar:ascale=log[v]" \
  -map "[v]" spectrum.mp4
```

### Phase spectrum display

```sh
ffplay -f lavfi "amovie=music.mp3,showfreqs=data=phase:mode=line"
```

## Notes

- Larger `win_size` gives better frequency resolution but less time resolution.
- `fscale=log` is easier to read for music (equal octave widths); `fscale=lin` is better for engineering analysis.
- `averaging` smooths the display over multiple frames — useful for noisy signals.
- For musical note-aligned display, prefer `showcqt`.

---

### showvolume

> Render a real-time per-channel volume meter as a video stream, useful for monitoring audio levels during recording or playback.

**Source:** [libavfilter/avf_showvolume.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_showvolume.c)

The `showvolume` filter produces a real-time volume level meter as a video stream, showing per-channel level bars. It is similar to a hardware VU meter — useful for monitoring recording levels, checking for clipping, or adding a visual level display to a video output. Colors can change based on level (green/yellow/red gradient).

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showvolume"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate / r | video_rate | `25` | Output frame rate. |
| b | int | `1` | Border width in pixels around each channel's meter. |
| w | int | `400` | Meter width in pixels. |
| h | int | `20` | Channel meter height in pixels. |
| f | double | `0.95` | Fade factor per frame (0 = instant decay, 1 = no decay). |
| c | string | `PEAK*255+floor(…)` | Meter bar color expression. |
| t | bool | `1` | Show volume value text on the meter bar. |
| v | bool | `1` | Show volume value numerically. |
| dm | double | `0` | Duration of max level display in seconds (peak hold). |
| dmc | color | `orange` | Color of the max level marker. |
| o | int | `h` | Channel display orientation: `h` (horizontal) or `v` (vertical). |
| s | int | `0` | Step in dB between background divisions. |
| p | float | `0` | Background opacity (0 = transparent). |
| m | int | `p` | Averaging mode: `p` (peak), `r` (rms). |
| ds | int | `lin` | Display scale: `lin` or `log`. |

## Examples

### Simple volume meter

```sh
ffplay -f lavfi "amovie=input.wav,showvolume=w=600:h=30"
```

### Peak hold meter (2-second hold)

```sh
ffplay -f lavfi "amovie=music.mp3,showvolume=dm=2:dmc=red"
```

### Embed in a video alongside the waveform

```sh
ffmpeg -i input.mp4 \
  -filter_complex \
    "[0:a]showvolume=w=200:h=720:o=v,format=yuva420p[vol];
     [0:v][vol]overlay=W-w:0" \
  output.mp4
```

### RMS mode with logarithmic display

```sh
ffplay -f lavfi "amovie=music.mp3,showvolume=m=r:ds=log"
```

## Notes

- Default color expression maps level to green→yellow→red via the `PEAK` variable.
- Use `f` (fade factor) to control peak decay speed — `f=1` holds bars statically.
- Combine with `overlay` to add the meter HUD to a video stream.
- For broadcast loudness compliance, use `ebur128`; `showvolume` shows instantaneous amplitude, not integrated loudness.

---

### showwaves

> Render an audio waveform as a real-time video stream, with configurable display modes, colors, and scaling.

**Source:** [libavfilter/avf_showwaves.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_showwaves.c)

The `showwaves` filter converts an audio stream into an animated waveform video. It supports several rendering modes — point, line, p2p (peak-to-peak), and cline (centered line) — and can display all channels merged or split into separate rows. It is commonly used for YouTube music visualizations, podcast videos, and audio quality inspection.

## Quick Start

```sh
ffplay -f lavfi "amovie=input.mp3,showwaves=size=800x300:mode=line"
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `600x240` | Output video size. |
| mode | int | `point` | Display mode: `point`, `line`, `p2p`, `cline`. |
| n | int64 | auto | Number of audio samples per output pixel (auto-computed from rate). |
| rate / r | video_rate | `25` | Output frame rate. |
| split_channels | bool | `0` | Display each channel in a separate row. |
| colors | string | `red|green|blue|yellow|…` | Per-channel colors separated by `\|`. |
| scale | int | `lin` | Amplitude scale: `lin`, `log`, `sqrt`, `cbrt`. |
| draw | int | `scale` | Drawing mode: `scale` or `full`. |
| filter | int | `off` | IIR filter to smooth: `off`, `average`. |

## Examples

### Scrolling waveform with ffplay

```sh
ffplay -f lavfi "amovie=music.mp3,showwaves=size=1280x360:mode=line:colors=white"
```

### Split channels in stereo

```sh
ffplay -f lavfi "amovie=stereo.flac,showwaves=size=800x400:split_channels=1:mode=cline"
```

### Save waveform video

```sh
ffmpeg -i input.mp3 \
  -filter_complex "[0:a]showwaves=size=1280x720:mode=line:colors=0x00aaff[v]" \
  -map "[v]" -c:v libx264 waveform.mp4
```

### Logarithmic scale for dynamic range

```sh
ffplay -f lavfi "amovie=music.mp3,showwaves=scale=log:mode=p2p"
```

## Notes

- `mode=line` draws a filled waveform (solid area); `mode=p2p` shows instantaneous peak-to-peak range; `mode=cline` draws lines from the center.
- `n` controls time resolution — lower values = more detail per pixel; auto-calculated from rate and size.
- For a static image of the full waveform, use `showwavespic` instead.
- Colors accept hex (`0xRRGGBB`), named colors, or `RRGGBB@alpha` with transparency.

---

### showwavespic

> Render the full waveform of an audio file as a single static image.

**Source:** [libavfilter/avf_showwaves.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/avf_showwaves.c)

The `showwavespic` filter renders the entire waveform of an audio stream into a single static image — the visual equivalent of the waveform view in a DAW or audio editor. Unlike `showwaves` (which produces a scrolling video), `showwavespic` buffers the complete audio and outputs one frame covering the full duration. It is ideal for thumbnail generation, album art waveforms, or batch waveform previews.

## Quick Start

```sh
ffmpeg -i input.mp3 -filter_complex "showwavespic=size=800x200" waveform.png
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | image_size | `600x240` | Output image size. |
| mode | int | `point` | Rendering mode: `point`, `line`, `p2p`, `cline`. |
| split_channels | bool | `0` | Display each channel in a separate row. |
| colors | string | `red\|green\|…` | Per-channel colors separated by `\|`. |
| scale | int | `lin` | Amplitude scale: `lin`, `log`, `sqrt`, `cbrt`. |
| draw | int | `scale` | Drawing mode: `scale` or `full`. |
| filter | int | `off` | IIR smoothing filter: `off` or `average`. |

## Examples

### Generate a waveform PNG

```sh
ffmpeg -i podcast.mp3 -filter_complex "showwavespic=size=1200x300:mode=line:colors=steelblue" waveform.png
```

### Split stereo channels

```sh
ffmpeg -i stereo.flac \
  -filter_complex "showwavespic=size=1000x400:split_channels=1" \
  stereo_waveform.png
```

### Waveform for a trimmed section

```sh
ffmpeg -i input.mp3 -ss 30 -t 60 \
  -filter_complex "showwavespic=size=800x200" section.png
```

### Logarithmic scale (shows quiet parts better)

```sh
ffmpeg -i input.wav -filter_complex "showwavespic=scale=log:mode=p2p" waveform_log.png
```

## Notes

- The filter buffers the entire audio before producing output — memory usage scales with audio duration at the sample rate.
- Trim long files with `-t` or `atrim` before feeding to `showwavespic` to keep memory usage manageable.
- For a scrolling real-time waveform video, use `showwaves` instead.
- `mode=p2p` (peak-to-peak) is the most common choice for DAW-style waveform thumbnails.

---

### thistogram

> Render a temporal histogram of pixel value distribution over time as a scrolling video, showing how the luma or color histogram evolves frame by frame.

**Source:** [libavfilter/vf_histogram.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_histogram.c)

The `thistogram` filter produces a temporal histogram — each column represents the pixel-value histogram of one video frame, and new columns scroll in from the right as the video plays. This creates a time-vs-level display that shows how the exposure and color distribution change over time. It is useful for spotting flicker, brightness ramps, color shifts, or inconsistent grading across a timeline.

## Quick Start

```sh
ffplay -i input.mp4 -vf thistogram
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| display_mode / d | int | `stack` | Overlay mode: `overlay` (histogram over video) or `stack` (side by side) or `parade`. |
| levels_mode / m | int | `linear` | Scale mode: `linear` or `logarithmic`. |
| components / c | int | `7` | Which color components to display (bitmask: 1=Y/R, 2=Cb/G, 4=Cr/B, 8=A). |
| level_height | int | `200` | Height of the histogram area in pixels. |
| scale_height | int | `12` | Height of the scale markers. |
| fgopacity / f | float | `0.7` | Foreground opacity. |
| bgopacity / b | float | `0.5` | Background opacity. |
| colors_mode / l | int | `colorful` | Color mode: `gray`, `color`, `colorful`, `levels`, `mono`, `acolor`, `xray`. |
| width / w | int | `0` | Width of display (0 = auto). |
| envelope / e | bool | `0` | Draw envelope around histogram. |
| slide | int | `replace` | Scroll mode: `replace`, `scroll`, `rscroll`, `frame`. |

## Examples

### Basic temporal histogram

```sh
ffplay -i input.mp4 -vf thistogram
```

### Logarithmic scale to see shadows better

```sh
ffplay -i input.mp4 -vf "thistogram=levels_mode=logarithmic"
```

### Luma only (component Y)

```sh
ffplay -i input.mp4 -vf "thistogram=components=1"
```

### Save temporal histogram video

```sh
ffmpeg -i input.mp4 -vf "thistogram=display_mode=stack:level_height=300" hist.mp4
```

## Notes

- `display_mode=overlay` draws the histogram over the video itself; `stack` adds it below.
- `components` bitmask: `1`=Y/R, `2`=Cb/G, `4`=Cr/B — combine by adding (e.g., `7` = all RGB).
- `slide=scroll` creates a waterfall/spectrogram style display where time scrolls left.
- For a per-frame static histogram display, use the `histogram` filter instead.

---

## Analysis & QC

### blackframe

> Detect video frames that are almost entirely black, logging frame number, percentage of black pixels, and timestamp.

**Source:** [libavfilter/vf_blackframe.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_blackframe.c)

The `blackframe` filter scans each video frame and reports frames where the majority of pixels fall below a configurable luminance threshold. It is commonly used to detect chapter boundaries, bumpers, or commercial breaks — transitions that are often signaled by a black frame. The filter passes video through unchanged and logs detections to stderr.

## Quick Start

```sh
# Detect black frames in a video file
ffmpeg -i input.mp4 -vf blackframe -f null - 2>&1 | grep blackframe
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| amount | int | `98` | Percentage of pixels that must be below the threshold to flag the frame (0–100). |
| threshold / thresh | int | `32` | Pixel luma value (0–255) below which a pixel is considered black. |

## Examples

### Default black frame detection

```sh
ffmpeg -i movie.mkv -vf blackframe -f null - 2>&1 | grep blackframe
```

### Stricter detection (100% of pixels must be black)

```sh
ffmpeg -i input.mp4 -vf "blackframe=amount=100:threshold=16" -f null -
```

### Log to file for post-processing

```sh
ffmpeg -i input.mp4 -vf blackframe -f null - 2>&1 | grep blackframe > black_frames.txt
```

### Find chapter transitions (relaxed threshold)

```sh
ffmpeg -i movie.mkv -vf "blackframe=amount=90:thresh=40" -f null - 2>&1 | grep blackframe
```

## Notes

- Output format: `blackframe:pblack:N pblack:PCT pos:FILEPOS pts:PTS t:TIME_SECONDS`
- The filter also exports `lavfi.blackframe.pblack` frame metadata with the percentage.
- Lower `threshold` (e.g., 16) reduces false positives from slightly-off-black frames.
- For detecting scene cuts rather than pure black frames, see `scdet`.

---

### blockdetect

> Detect DCT-based blocking artifacts in compressed video frames and attach a blockiness score as frame metadata.

**Source:** [libavfilter/vf_blockdetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_blockdetect.c)

The `blockdetect` filter measures the severity of DCT blocking artifacts in compressed video without modifying the stream. It is based on the Muijs–Kirenko no-reference blocking artifact measure: it looks for periodic pixel grid patterns at the block boundaries typical of heavy MPEG/H.264 quantization. The score is attached as `lavfi.block` frame metadata and can drive automated quality reports or `select` filter decisions.

## Quick Start

```sh
# Print per-frame blockiness scores
ffmpeg -i input.mp4 -vf blockdetect -f null - 2>&1 | grep block
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_min | int | `3` | Minimum pixel grid period to search for. |
| period_max | int | `24` | Maximum pixel grid period to search for. |
| planes | int | `1` | Bitmask of planes to analyze (default: first plane only). |

## Examples

### Default blockiness detection

```sh
ffmpeg -i compressed.mp4 -vf blockdetect -f null -
```

### Search for H.264 typical 8×8 and 16×16 block periods

```sh
ffmpeg -i input.mp4 -vf "blockdetect=period_min=8:period_max=16" -f null -
```

### Save per-frame scores to a file

```sh
ffmpeg -i input.mp4 \
  -vf "blockdetect,metadata=print:key=lavfi.block:file=block_scores.txt" \
  -f null -
```

### Combine with blurdetect for full quality report

```sh
ffmpeg -i input.mp4 -vf "blockdetect,blurdetect" -f null - 2>&1 | grep "lavfi\."
```

## Notes

- `lavfi.block` metadata value increases with artifact severity; perfectly clean frames score near 0.
- The default period range [3, 24] covers common block sizes (4×4 up to 24×24); adjust for the codec under test.
- Use after decoding compressed video; does not apply meaningfully to lossless or raw sources.
- Pair with `deblock` to both detect and reduce blocking in a single pipeline.

---

### blurdetect

> Compute a no-reference blur metric for each video frame using Canny edge detection, attaching the result as frame metadata.

**Source:** [libavfilter/vf_blurdetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_blurdetect.c)

The `blurdetect` filter computes a perceptual blur score for each frame without modifying the video. It is based on the Marziliano no-reference blur metric: it detects edges using Canny thresholding, then measures the spread of local maxima around each edge — wider spread indicates more blur. The score is attached as `lavfi.blur` frame metadata and can be used for automated quality control.

## Quick Start

```sh
# Print blur scores to stderr
ffmpeg -i input.mp4 -vf "blurdetect" -f null - 2>&1 | grep blur
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| low | float | `20/255 ≈ 0.078` | Low threshold for Canny edge detection (0–1). |
| high | float | `50/255 ≈ 0.196` | High threshold for Canny edge detection (0–1). `high` ≥ `low`. |
| radius | int | `50` | Search radius (pixels) around edge pixel for local maxima. |
| block_pct | int | `80` | Percentage of most significant blocks to include in blur score. |
| block_width | int | `-1` | Block width for block-based analysis; ≤0 disables block mode. |
| block_height | int | `-1` | Block height for block-based analysis; ≤0 disables block mode. |
| planes | int | `1` | Bitmask of planes to analyze (default: first plane only). |

## Examples

### Basic blur detection

```sh
ffmpeg -i input.mp4 -vf blurdetect -f null -
```

### Block-based analysis (32×32 blocks, top 80%)

```sh
ffmpeg -i input.mp4 -vf "blurdetect=block_width=32:block_height=32:block_pct=80" -f null -
```

### Inject metadata for select filter

```sh
ffmpeg -i input.mp4 \
  -vf "blurdetect,metadata=print:key=lavfi.blur:file=blur_scores.txt" \
  -f null -
```

### Adjust Canny thresholds for higher sensitivity

```sh
ffmpeg -i input.mp4 -vf "blurdetect=low=0.05:high=0.15" -f null -
```

## Notes

- `lavfi.blur` metadata value is the mean blur width — higher = more blurry.
- Use `metadata=print` after `blurdetect` to write per-frame scores to a file.
- Block-based mode (`block_width`/`block_height`) is faster and focuses on the sharpest regions.
- See `blockdetect` for detecting compression blocking artifacts (a different artifact type).

---

### drmeter

> Measure the Dynamic Range (DR) of an audio file using the crest factor method, reporting DR values per segment.

**Source:** [libavfilter/af_drmeter.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_drmeter.c)

The `drmeter` filter computes the Dynamic Range score popularized by the DR Loudness War database. It splits the audio into segments, computes the crest factor (peak-to-RMS ratio) for each, and derives a DR value. Higher DR indicates more dynamic, less compressed audio (DR14+ = very dynamic; DR8–13 = typical modern mastering; DR<8 = heavily limited). The audio passes through unchanged.

## Quick Start

```sh
# Measure dynamic range of a music file
ffmpeg -i music.flac -af drmeter -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| length | double | `3.0` | Window length in seconds for segment splitting. |

## Examples

### Basic DR measurement

```sh
ffmpeg -i album_track.flac -af drmeter -f null - 2>&1 | grep -i dr
```

### Shorter segments for more detail

```sh
ffmpeg -i music.wav -af "drmeter=length=1" -f null -
```

### Compare two masters

```sh
for f in original.wav loudness_war.wav; do
  echo "=== $f ===" && ffmpeg -i "$f" -af drmeter -f null - 2>&1 | grep DR
done
```

## Notes

- DR14+ is found in acoustic, jazz, and classical recordings with natural dynamics.
- DR8–13 is typical of modern pop/rock mastering.
- DR<8 indicates heavy brick-wall limiting or compression — associated with "loudness war" releases.
- The segment length (`length`) affects measurement granularity; 3 seconds is the conventional default matching the DR database tool.

---

### ebur128

> Measure loudness according to the EBU R128 / ITU-R BS.1770 standard, logging momentary, short-term, and integrated loudness with optional real-time video output.

**Source:** [libavfilter/f_ebur128.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_ebur128.c)

The `ebur128` filter implements the EBU R128 / ITU-R BS.1770 loudness scanner. It measures Momentary loudness (M, 400 ms window), Short-term loudness (S, 3 s window), Integrated loudness (I, gated over the whole programme), and Loudness Range (LRA). The audio passes through unchanged; statistics are logged to stderr and optionally injected into frame metadata. With `video=1`, a real-time graphing display is produced as a video output stream.

## Quick Start

```sh
# Measure loudness of a file and print summary to stderr
ffmpeg -i input.wav -af ebur128 -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| video | bool | `0` | Output a real-time loudness graph as a video stream. |
| size | image_size | `640x480` | Size of the video output (only used when `video=1`). |
| meter | int | `9` | EBU scale meter: `9` (±9 LU) or `18` (±18 LU). |
| metadata | bool | `0` | Inject per-100ms loudness values as frame metadata (`lavfi.r128.*`). |
| framelog | int | `info` | Logging level: `quiet`, `info`, `verbose`. |
| peak | flags | `none` | Enable `sample` and/or `true` peak measurement. |
| dualmono | bool | `0` | Treat mono input as dual-mono (adds 3 LU to account for equal-loudness of dual mono). |
| panlaw | double | `-3.0103` | Pan law for dual-mono (dB). |
| target | int | `-23` | Target loudness in LUFS; shifts the green ±1 LU zone in the video display. |
| gauge | int | `momentary` | Gauge type: `momentary` or `shortterm`. |
| scale | int | `absolute` | Scale display: `absolute` (LUFS) or `relative` (LU). |

## Examples

### Measure integrated loudness (broadcast compliance check)

```sh
ffmpeg -i input.mp4 -af ebur128=peak=true -f null -
```

### Real-time loudness graph alongside video

```sh
ffmpeg -i input.mp4 \
  -filter_complex "[0:a]ebur128=video=1:size=640x480[vid][aud]" \
  -map "[vid]" -map "[aud]" -map 0:v \
  -c:v libx264 output.mp4
```

### Inject metadata for downstream processing

```sh
ffmpeg -i input.wav -af ebur128=metadata=1 -f null -
```

### Check true peak and sample peak

```sh
ffmpeg -i input.wav -af ebur128=peak=sample+true -f null - 2>&1 | grep -E "I:|TPK:|SPK:"
```

## Notes

- The EBU R128 broadcast target is **−23 LUFS** (integrated) with a max true peak of −1 dBTP.
- `true` peak mode requires an over-sampled analysis and a build with `libswresample` — it is more accurate than sample peak.
- The filter outputs `lavfi.r128.I`, `lavfi.r128.M`, `lavfi.r128.S`, `lavfi.r128.LRA` as frame metadata when `metadata=1`.
- Use `loudnorm` (also EBU R128) to actually normalize loudness; `ebur128` only measures.

---

### freezedetect

> Detect frozen (static) video segments by comparing consecutive frames, logging start time, duration, and end time as metadata.

**Source:** [libavfilter/vf_freezedetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_freezedetect.c)

The `freezedetect` filter identifies frozen video — segments where consecutive frames show no significant change — and logs the start, duration, and end of each freeze event. It is used in broadcast playout monitoring to catch encoder stalls, dropped feeds, or slate/bug errors. The video stream passes through unchanged; detections are logged to stderr and attached as frame metadata.

## Quick Start

```sh
# Detect freeze events (default: 2 seconds, -60dB noise tolerance)
ffmpeg -i input.mp4 -vf freezedetect -f null - 2>&1 | grep freeze
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise / n | double | `-60dB` | Noise tolerance — max mean absolute difference between frames considered frozen. Can be in dB (e.g., `-50dB`) or ratio (e.g., `0.001`). |
| duration / d | duration | `2s` | Minimum duration of a static segment before it is reported as a freeze. |

## Examples

### Default freeze detection

```sh
ffmpeg -i broadcast.ts -vf freezedetect -f null - 2>&1 | grep freeze
```

### Detect short freezes (500ms) with relaxed noise tolerance

```sh
ffmpeg -i input.mp4 -vf "freezedetect=n=-50dB:d=0.5" -f null -
```

### Log freeze events to file

```sh
ffmpeg -i input.mp4 -vf freezedetect -f null - 2>&1 | grep freezedetect > freezes.txt
```

### Monitor a live stream in real time

```sh
ffmpeg -i rtsp://camera/stream -vf "freezedetect=d=3" -f null -
```

## Notes

- Metadata keys set: `lavfi.freezedetect.freeze_start` (on first frozen frame at or after `d`), `lavfi.freezedetect.freeze_duration` and `lavfi.freezedetect.freeze_end` (on first frame after the freeze).
- The noise threshold accounts for encoder quantization noise — a perfectly frozen H.264 stream may still produce small inter-frame differences due to bitstream artifacts.
- Combine with `silencedetect` for full A/V dropout detection in broadcast QC pipelines.

---

### replaygain

> Scan audio and compute ReplayGain track gain and peak values for loudness normalization tagging.

**Source:** [libavfilter/af_replaygain.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_replaygain.c)

The `replaygain` filter scans an audio stream and computes the ReplayGain track gain (in dB) and track peak values according to the ReplayGain 2.0 specification. The audio passes through unmodified; the results are printed at the end of the stream and exported as filter options. The computed values can then be written as tags to audio files so players can apply consistent loudness normalization without re-encoding.

## Quick Start

```sh
# Compute ReplayGain for a track
ffmpeg -i music.flac -af replaygain -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| track_gain | float | *(read-only)* | Exported track gain in dB after stream end. |
| track_peak | float | *(read-only)* | Exported track peak amplitude after stream end. |

## Examples

### Measure ReplayGain and print to stderr

```sh
ffmpeg -i music.mp3 -af replaygain -f null - 2>&1 | grep -E "track_gain|track_peak"
```

### Batch scan a folder

```sh
for f in *.flac; do
  echo "$f:" && ffmpeg -i "$f" -af replaygain -f null - 2>&1 | grep track_gain
done
```

### Combined with ebur128 for comparison

```sh
ffmpeg -i music.flac -af "replaygain,ebur128" -f null -
```

## Notes

- ReplayGain targets **89 dB SPL** (equivalent to −14 LUFS approximately), while EBU R128 targets −23 LUFS. They produce different normalization values for the same file.
- The filter only measures; use a tagging tool (e.g., `metaflac`, `mp3gain`) or `ffmpeg -metadata` to write the computed values into the file.
- `track_gain` is a negative value for loud content (e.g., `-3.2 dB`) and positive for quiet content.
- For streaming and broadcast use, `ebur128` + `loudnorm` following the −23 LUFS EBU R128 target is generally preferred over ReplayGain.

---

### signature

> Compute the MPEG-7 video signature fingerprint for duplicate detection, and optionally match two input streams to find time offsets.

**Source:** [libavfilter/vf_signature.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_signature.c)

The `signature` filter computes the MPEG-7 Video Signature for near-duplicate detection and content identification. The fingerprint is robust to re-encoding, resizing, and mild color grading. With two inputs, it can compare streams and find matching segments with their time offsets. Signatures can be written as binary or XML files for offline comparison.

## Quick Start

```sh
# Write MPEG-7 signature of a video to a binary file
ffmpeg -i input.mp4 -vf "signature=filename=sig.bin" -map 0:v -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| detectmode | int | `off` | Matching mode: `off`, `full` (whole-video match), `fast` (stop at first match). |
| nb_inputs | int | `1` | Number of input streams to compare. |
| filename | string | — | Output path for signature file. Use `%d` when `nb_inputs > 1`. |
| format | int | `binary` | Output format: `binary` or `xml`. |
| th_d | int | `9000` | Threshold for single-word similarity. |
| th_dc | int | `60000` | Threshold for all-word similarity. |
| th_xh | int | `116` | Threshold for frame-level similarity. |
| th_di | int | `0` | Minimum matching sequence length (frames). |
| th_it | double | `0.5` | Minimum ratio of matching frames to all frames (0–1). |

## Examples

### Generate a binary signature

```sh
ffmpeg -i input.mkv -vf "signature=filename=signature.bin" -map 0:v -f null -
```

### Generate XML signature for readability

```sh
ffmpeg -i input.mp4 -vf "signature=filename=sig.xml:format=xml" -map 0:v -f null -
```

### Compare two videos for duplicate detection

```sh
ffmpeg -i video1.mp4 -i video2.mp4 \
  -filter_complex "[0:v][1:v]signature=nb_inputs=2:detectmode=full:format=xml:filename=sig%d.xml" \
  -map 0:v -f null -
```

### Fast match (stop at first matching segment)

```sh
ffmpeg -i ref.mp4 -i query.mp4 \
  -filter_complex "[0:v][1:v]signature=nb_inputs=2:detectmode=fast" \
  -map 0:v -f null -
```

## Notes

- The MPEG-7 signature is robust to re-encoding and moderate visual changes but not heavy editing.
- With `nb_inputs=2` and `detectmode=full`, the filter logs `matching` or `no matching` plus the time offset if found.
- For batch comparison, generate signatures once and compare the binary/XML files offline — avoids re-processing video.
- Use `th_di` to set a minimum match length; a value of `0` (default) means any single matching segment counts.

---

### silencedetect

> Detect silent segments in audio by reporting start time, duration, and end time whenever audio falls below a noise threshold for a minimum duration.

**Source:** [libavfilter/af_silencedetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_silencedetect.c)

The `silencedetect` filter monitors audio level and logs an event when the signal stays below a configurable noise floor for at least a minimum duration. It sets `lavfi.silence_start`, `lavfi.silence_duration`, and `lavfi.silence_end` frame metadata, and prints to stderr. It is used to find gaps in recordings, split audio at silence, or quality-check broadcast playout. The audio passes through unchanged.

## Quick Start

```sh
# Detect silences longer than 1 second
ffmpeg -i input.wav -af "silencedetect=d=1" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| noise / n | double | `-60dB` | Noise floor. Can be dB (e.g., `-50dB`) or amplitude ratio (e.g., `0.001`). |
| duration / d | duration | `2s` | Minimum silence duration before reporting. |
| mono / m | bool | `0` | When enabled, analyze each channel independently (adds `.X` suffix to metadata keys). |

## Examples

### Detect 2-second silences (default)

```sh
ffmpeg -i podcast.mp3 -af silencedetect -f null - 2>&1 | grep silence
```

### Detect short pauses (500ms, relaxed noise floor)

```sh
ffmpeg -i interview.wav -af "silencedetect=n=-50dB:d=0.5" -f null -
```

### Per-channel silence detection (stereo)

```sh
ffmpeg -i stereo.wav -af "silencedetect=mono=1" -f null - 2>&1 | grep silence
```

### Extract silence timestamps for use as chapter markers

```sh
ffmpeg -i long_recording.wav -af silencedetect -f null - 2>&1 | \
  grep silence_end | awk '{print $5}' > chapter_times.txt
```

## Notes

- Metadata keys: `lavfi.silence_start` is set on the first frame at or after the minimum duration; `lavfi.silence_end` and `lavfi.silence_duration` are set on the first non-silent frame after.
- With `mono=1`, keys are suffixed `.0`, `.1`, etc. per channel — useful for detecting dropout on one channel only.
- To actually remove silence rather than just detect it, use the `silenceremove` filter.
- The noise floor default of −60 dB is quite tight; for recordings with floor noise or hum, use −50 dB or higher.

---

### siti

> Calculate Spatial Information (SI) and Temporal Information (TI) complexity scores per frame as defined in ITU-T Rec. P.910.

**Source:** [libavfilter/vf_siti.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_siti.c)

The `siti` filter computes SI and TI metrics from ITU-T Rec. P.910, which are standard measures of visual complexity used in video codec benchmarking and adaptive bitrate research. SI measures spatial detail (via a Sobel edge filter on each frame), while TI measures temporal motion (via frame differencing). Per-frame values are emitted as metadata; an optional summary prints the maximum SI, maximum TI, and mean values at the end of the stream.

## Quick Start

```sh
# Compute SI/TI and print summary
ffmpeg -i input.mp4 -vf "siti=print_summary=1" -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| print_summary | bool | `0` | Print average and max SI/TI to the console at the end of the stream. |

## Examples

### Print SI/TI summary for a file

```sh
ffmpeg -i input.mp4 -vf "siti=print_summary=1" -f null -
```

### Export per-frame SI/TI values to a CSV

```sh
ffmpeg -i input.mp4 -vf "siti,metadata=print:file=siti.txt" -f null -
```

### Compare SI/TI of two encodes

```sh
for f in original.mp4 compressed.mp4; do
  echo "=== $f ===" && ffmpeg -i "$f" -vf "siti=print_summary=1" -f null - 2>&1 | grep -E "SI|TI"
done
```

## Notes

- **SI** (Spatial Information): Standard deviation of a Sobel-filtered frame. High SI = lots of edges/texture. Typical range: 10–120.
- **TI** (Temporal Information): Standard deviation of the frame difference. High TI = lots of motion. Typical range: 5–100.
- Content in the upper-right quadrant (high SI, high TI) is the hardest to compress efficiently.
- Note: this implementation follows the legacy P.910 (11/21) specification; the current standard is P.910 (07/22).

---

### vmafmotion

> Compute the VMAF motion score per frame — a per-frame motion metric that is one component of the VMAF video quality model.

**Source:** [libavfilter/vf_vmafmotion.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_vmafmotion.c)

The `vmafmotion` filter computes the VMAF motion score — a per-frame temporal motion metric that is one of the sub-features used in Netflix's VMAF (Video Multi-method Assessment Fusion) model. It measures the mean absolute difference between consecutive frames after a low-pass filter. The filter passes video through unchanged and logs the mean motion score at the end. Per-frame scores can be written to a file.

## Quick Start

```sh
# Print average VMAF motion score
ffmpeg -i input.mp4 -vf vmafmotion -f null -
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stats_file | string | — | Path to write per-frame motion scores. Use `-` to write to stdout. |

## Examples

### Print average motion score to log

```sh
ffmpeg -i input.mp4 -vf vmafmotion -f null - 2>&1 | grep motion
```

### Save per-frame scores to a file

```sh
ffmpeg -i input.mp4 -vf "vmafmotion=stats_file=motion.txt" -f null -
```

### Print to stdout (pipe to awk for averaging)

```sh
ffmpeg -i input.mp4 -vf "vmafmotion=stats_file=-" -f null - 2>/dev/null | \
  awk '{sum+=$NF; n++} END {print "mean:", sum/n}'
```

## Notes

- The VMAF motion score is correlated with perceived motion blur and temporal complexity — high scores indicate fast-moving content.
- This is a **single-stream** filter (no reference video needed), unlike full VMAF which requires a reference/distorted pair.
- For full VMAF quality measurement, use the `libvmaf` filter with a reference stream.
- Scores are typically in the range 0–20; action scenes often score 5–15, static content near 0.

---

### volumedetect

> Analyze audio and report mean volume, maximum volume, and a histogram of sample levels at the end of the stream.

**Source:** [libavfilter/af_volumedetect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/af_volumedetect.c)

The `volumedetect` filter scans an audio stream and prints the mean volume (RMS), maximum sample volume, and a histogram of level distribution at the end of the stream. It is the simplest way to determine how much headroom a file has before clipping — essential before normalizing with the `volume` filter. The audio passes through unchanged; there are no parameters to configure.

## Quick Start

```sh
# Detect volume stats for a file
ffmpeg -i input.wav -af volumedetect -f null -
```

## Parameters

None. `volumedetect` has no configurable options.

## Examples

### Print volume stats for a file

```sh
ffmpeg -i input.mp3 -af volumedetect -f null - 2>&1 | grep volume
```

### Determine safe normalization gain

```sh
# max_volume will show the headroom; use it as input to -af volume
ffmpeg -i input.wav -af volumedetect -f null - 2>&1 | grep max_volume
# Then normalize:
ffmpeg -i input.wav -af "volume=6dB" normalized.wav
```

### Batch volume scan

```sh
for f in *.mp3; do
  echo "$f:" && ffmpeg -i "$f" -af volumedetect -f null - 2>&1 | grep -E "mean_volume|max_volume"
done
```

### Check whether audio will clip at a given gain

```sh
# If max_volume is -4dB, adding more than +4dB will clip
ffmpeg -i loud.wav -af volumedetect -f null - 2>&1 | grep max_volume
```

## Notes

- Output includes `mean_volume` (RMS in dBFS), `max_volume` (peak sample in dBFS), and a histogram like `histogram_4db: 6` (6 samples within −4 to −5 dBFS).
- If `max_volume` is, say, −4 dB, you can safely apply up to +4 dB gain without clipping.
- For broadcast loudness compliance, use `ebur128` instead — it measures integrated loudness (LUFS), not peak.
- Only supports 16-bit signed integer samples natively; the filter adds an implicit format conversion if needed.

---

## Interlace & Telecine

### detelecine

> Apply inverse telecine using a known pulldown pattern to reconstruct the original progressive frames from telecined video.

**Source:** [libavfilter/vf_detelecine.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_detelecine.c)

The `detelecine` filter performs pattern-based inverse telecine — the exact reverse of the `telecine` filter. It requires knowing the pulldown pattern and phase (start frame) of the telecined stream. When the pattern is known (e.g., content was encoded by the same FFmpeg pipeline using `telecine`), `detelecine` provides a perfect lossless inversion. For content of unknown pattern, use `fieldmatch` + `decimate` instead.

## Quick Start

```sh
# Reverse 3:2 pulldown with known pattern
ffmpeg -i ntsc_telecined.ts -vf "detelecine" -r 24000/1001 progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| first_field | int | `top` | First field: `top` or `bottom`. Must match the `telecine` setting. |
| pattern | string | `23` | Pulldown pattern. Must exactly match the pattern used during `telecine`. |
| start_frame | int | `0` | Position of the first frame relative to the pattern, if the stream is cut. |

## Examples

### Reverse classic 3:2 pulldown

```sh
ffmpeg -i ntsc.ts -vf detelecine -r 24000/1001 film.mp4
```

### Reverse PAL Euro pulldown

```sh
ffmpeg -i pal.ts -vf "detelecine=pattern=222222222223" -r 24 film.mp4
```

### Handle cut stream with known phase offset

```sh
# If the clip was cut 3 frames into the pattern cycle:
ffmpeg -i cut_clip.ts -vf "detelecine=start_frame=3" -r 24000/1001 film.mp4
```

## Notes

- `detelecine` only works reliably when the pattern and phase are known; for broadcast captures of unknown origin, use `fieldmatch` + `decimate` or `pullup` instead.
- The `start_frame` parameter is essential when processing a mid-stream cut — incorrect values produce combed output.
- The output framerate will be variable unless you specify `-r` explicitly; set it to match the original pre-telecine rate.

---

### fieldmatch

> Match fields for inverse telecine, reconstructing progressive frames from telecined video while leaving genuinely interlaced frames flagged for downstream deinterlacing.

**Source:** [libavfilter/vf_fieldmatch.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_fieldmatch.c)

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

---

### interlace

> Interleave fields from consecutive progressive frames to produce interlaced video, halving the frame rate while preserving spatial resolution.

**Source:** [libavfilter/vf_tinterlace.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_tinterlace.c)

The `interlace` filter converts progressive video to interlaced output by interleaving alternating lines from two consecutive input frames. This halves the output frame rate while keeping the full spatial resolution. It is used for broadcast delivery when a progressive source needs to be encoded as interlaced (e.g., 50p → 25i, 60p → 30i). A vertical low-pass filter is available to prevent interlace twitter artifacts.

## Quick Start

```sh
# Convert 50fps progressive to 25i interlaced
ffmpeg -i input_50fps.mp4 -vf interlace output_25i.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scan | int | `tff` | Field order: `tff` (top field first) or `bff` (bottom field first). |
| lowpass | int | `linear` | Vertical low-pass filter: `off`, `linear`, `complex`. |

## Examples

### 50fps progressive to 25i TFF (PAL broadcast)

```sh
ffmpeg -i source_50fps.mp4 -vf interlace -r 25 broadcast.ts
```

### 60fps progressive to 30i BFF

```sh
ffmpeg -i source_60fps.mp4 -vf "interlace=scan=bff" -r 30 broadcast.ts
```

### With complex low-pass to reduce moiré

```sh
ffmpeg -i input_50fps.mp4 -vf "interlace=lowpass=complex" -r 25 output.ts
```

## Notes

- `scan=tff` (top-field-first) is standard for most broadcast formats; use `bff` for formats that specify bottom-field-first (e.g., some DV/DVCPro).
- `lowpass=complex` is better at retaining detail with less twitter than `linear`, but is slightly more expensive.
- This filter interleaves fields from frames j and j+1 — the output frame contains lines 0,2,4… from frame j and lines 1,3,5… from frame j+1.
- For a more feature-rich version with additional modes, see `tinterlace`.

---

### kerndeint

> Deinterlace video using Donald Graft's adaptive kernel deinterlacer, which applies processing only to detected interlaced regions.

**Source:** [libavfilter/vf_kerndeint.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_kerndeint.c)

The `kerndeint` filter deinterlaces video using Donald Graft's adaptive kernel algorithm. Unlike simple field-drop deinterlacers, `kerndeint` detects which pixel rows are actually interlaced (show combing) and applies processing only there, preserving quality in non-interlaced areas. It can optionally apply sharpening to recovered regions. For most use cases, `yadif` or `bwdif` are preferred, but `kerndeint` can work well for specific content types.

## Quick Start

```sh
ffmpeg -i interlaced.ts -vf kerndeint output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| thresh | int | `10` | Threshold (0–255) for detecting interlaced pixels. `0` = process every pixel. |
| map | bool | `0` | Paint detected interlaced pixels white (useful for tuning thresh). |
| order | bool | `0` | Field order: `0` = normal, `1` = swap fields. |
| sharp | bool | `0` | Enable additional sharpening on processed pixels. |
| twoway | bool | `0` | Enable two-way sharpening (sharper result). |

## Examples

### Default deinterlacing

```sh
ffmpeg -i interlaced.ts -vf kerndeint output.mp4
```

### Visualize which pixels are processed (tuning thresh)

```sh
ffplay -i interlaced.ts -vf "kerndeint=map=1:thresh=15"
```

### With sharpening

```sh
ffmpeg -i interlaced.ts -vf "kerndeint=sharp=1" sharpened.mp4
```

### Process every pixel (thresh=0) with two-way sharpening

```sh
ffmpeg -i interlaced.ts -vf "kerndeint=thresh=0:twoway=1" output.mp4
```

## Notes

- Set `thresh` to balance between processing too few pixels (residual combing) and too many (unnecessary blurring).
- Use `map=1` to visualize the detection mask — white pixels will be processed; tune `thresh` until combing areas are fully covered.
- For broadcast-quality deinterlacing, `yadif` with `mode=1` (send_field) is generally preferred.
- `sharp=1` and `twoway=1` can recover some sharpness lost during deinterlacing but may introduce ringing on hard edges.

---

### pullup

> Reverse 3:2 pulldown (inverse telecine) to reconstruct progressive frames from NTSC-telecined video using look-ahead field matching.

**Source:** [libavfilter/vf_pullup.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_pullup.c)

The `pullup` filter performs inverse telecine (IVTC) — it reconstructs the original 24fps or 25fps progressive frames from 29.97fps 3:2 pulldown telecined video. Unlike pattern-based approaches, `pullup` uses look-ahead field matching, making it robust to mixed content (24p telecined + 30i interlaced). The output has variable framerate; use `fps=24000/1001` after `pullup` for NTSC, or `fps=25` for PAL.

## Quick Start

```sh
# Inverse telecine NTSC (29.97i → 23.976p)
ffmpeg -i telecined.ts -vf "pullup,fps=24000/1001" progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| jl | int | `8` | Junk pixels to ignore on the left (units: 8 pixels). |
| jr | int | `8` | Junk pixels to ignore on the right (units: 8 pixels). |
| jt | int | `4` | Junk lines to ignore at top (units: 2 lines). |
| jb | int | `4` | Junk lines to ignore at bottom (units: 2 lines). |
| sb | int | `0` | Strict breaks: `1` = fewer false matches but may drop frames; `-1` = more permissive. |
| mp | int | `l` | Metric plane: `l` (luma), `u` (Cb), `v` (Cr). |

## Examples

### Inverse telecine NTSC film

```sh
ffmpeg -i film_telecined.ts -vf "pullup,fps=24000/1001" -c:v libx264 film.mp4
```

### Inverse telecine PAL

```sh
ffmpeg -i pal_pulldown.mxf -vf "pullup,fps=25" progressive.mp4
```

### With strict breaks for cleaner output

```sh
ffmpeg -i input.ts -vf "pullup=sb=1,fps=24000/1001" clean.mp4
```

## Notes

- `pullup` produces variable-framerate output — always follow with `fps` to regularize the frame rate.
- For content that is a mix of telecined and interlaced video, `fieldmatch` + `yadif` + `decimate` is a more flexible alternative.
- The "junk" parameters (`jl`, `jr`, `jt`, `jb`) help ignore logo bugs or letterbox areas that might confuse field matching.
- `mp=l` (luma, the default) is best for most content; use chroma plane only to save CPU on clean sources.

---

### telecine

> Apply telecine (3:2 pulldown) to progressive video, converting 24fps film content to 29.97fps interlaced video for NTSC broadcast.

**Source:** [libavfilter/vf_telecine.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_telecine.c)

The `telecine` filter applies a pulldown pattern to progressive video, creating the 3:2 field sequence used when converting 24fps film to 29.97fps NTSC broadcast. Each progressive frame is repeated across fields according to the pattern: the classic `23` pattern repeats two frames as 2 fields and one as 3 fields. The filter can also apply non-standard pulldown patterns for other conversion ratios (25→30, 18→30, etc.).

## Quick Start

```sh
# Apply 3:2 pulldown: 24fps progressive → 29.97fps telecined
ffmpeg -i film_24fps.mp4 -vf telecine -r 30000/1001 ntsc_telecined.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| first_field | int | `top` | First output field: `top` (tff) or `bottom` (bff). |
| pattern | string | `23` | Pulldown pattern — string of digits indicating field repeat counts per frame. |

## Pulldown Patterns

| Pattern | Usage |
|---------|-------|
| `23` | 24fps → NTSC 30i (classic 3:2 pulldown) |
| `2332` | 24fps → NTSC 30i (preferred, smoother) |
| `33` | 20fps → NTSC 30i |
| `334` | 18fps → NTSC 30i |
| `222222222223` | 24fps → PAL 25i (Euro pulldown) |

## Examples

### Classic 3:2 pulldown (24fps to 29.97fps)

```sh
ffmpeg -i film.mp4 -vf telecine -r 30000/1001 ntsc.ts
```

### Preferred 2332 pattern for 24p

```sh
ffmpeg -i film.mp4 -vf "telecine=pattern=2332" -r 30000/1001 ntsc.ts
```

### PAL Euro pulldown (24fps to 25fps interlaced)

```sh
ffmpeg -i film.mp4 -vf "telecine=pattern=222222222223" -r 25 pal.ts
```

### Bottom field first (for certain tape formats)

```sh
ffmpeg -i film.mp4 -vf "telecine=first_field=bottom" -r 30000/1001 ntsc_bff.ts
```

## Notes

- The pattern digits indicate how many fields each input frame contributes; total divided by 2 gives output frames per input frame.
- The `23` pattern produces judder on 24fps content when displayed on 60Hz displays — `2332` distributes the cadence more evenly.
- To reverse telecine on the output later, use `detelecine` with the same pattern.

---

### tinterlace

> Perform temporal field interlacing with multiple modes — merge progressive frames into interlaced output, drop fields, or pad with blank lines.

**Source:** [libavfilter/vf_tinterlace.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_tinterlace.c)

The `tinterlace` filter provides fine-grained temporal field interlacing with multiple operational modes. It can weave fields from consecutive frames into interlaced output (`merge`), drop alternate frames, pad frames with blank lines, or interleave in various patterns. It is the multi-mode predecessor to the simpler `interlace` filter and offers more flexibility for broadcast encoding workflows.

## Quick Start

```sh
# Merge progressive 50fps frames into 25i interlaced
ffmpeg -i progressive_50fps.mp4 -vf tinterlace -r 25 interlaced.ts
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | int | `merge` | Interlacing mode (see table below). |
| flags | flags | — | Additional flags: `vlpf` (vertical low-pass filter). |
| scan | int | `tff` | Field order for modes that need it: `tff` or `bff`. |
| lowpass | int | `linear` | Vertical low-pass filter: `off`, `linear`, `complex`. |

## Modes

| Mode | Value | Description |
|------|-------|-------------|
| `merge` | 0 | Weave odd frames (upper field) + even frames (lower field); halves framerate, doubles height. |
| `drop_even` | 1 | Output only odd frames, drop even; halves framerate. |
| `drop_odd` | 2 | Output only even frames, drop odd; halves framerate. |
| `pad` | 3 | Expand each frame to full height with alternate blank lines; same framerate. |
| `interleave_top` | 4 | Interleave top field from odd, bottom from even. |
| `interleave_bottom` | 5 | Interleave bottom field from odd, top from even. |
| `interlacex2` | 6 | Move fields to separate frames; doubles framerate. |
| `mergex2` | 7 | Same as `merge` but keep framerate by doubling. |

## Examples

### Merge progressive frames into interlaced

```sh
ffmpeg -i 50fps_progressive.mp4 -vf "tinterlace=mode=merge" -r 25 output.ts
```

### Apply vertical low-pass to reduce twitter

```sh
ffmpeg -i input.mp4 -vf "tinterlace=mode=merge:lowpass=complex" output.ts
```

### Drop even frames for simple frame rate conversion

```sh
ffmpeg -i 60fps.mp4 -vf "tinterlace=mode=drop_even" 30fps.mp4
```

## Notes

- `lowpass=complex` reduces interlace twitter and moiré better than `linear` but at a slight sharpness cost.
- For simple progressive-to-interlaced encoding, the simpler `interlace` filter is often sufficient.
- `mode=merge` is the classic interlacing operation used for broadcast delivery.

---

## Utility & Timing

### aloop

> Loop a segment of audio samples a specified number of times or infinitely.

**Source:** [libavfilter/f_loop.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_loop.c)

The `aloop` filter repeats a segment of audio samples N times, buffering a configurable number of samples and replaying them in sequence. It is the audio counterpart to the `loop` video filter and uses the same parameter semantics with samples instead of frames. Common uses include creating seamless music loops, extending short clips, and generating ambient sound loops.

## Quick Start

```sh
# Loop 44100 samples (1 second at 44.1kHz) 5 times
ffmpeg -i input.wav -af "aloop=loop=5:size=44100" looped.wav
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| loop | int | `0` | Number of loop iterations. `0` = no looping; `-1` = infinite. |
| size | int64 | `0` | Maximum number of samples to buffer for the loop segment. |
| start | int64 | `0` | Sample number where the loop segment starts. |
| time | duration | — | Loop start time (used instead of `start` when `start=-1`). |

## Examples

### Loop 2 seconds of audio 4 times (at 44.1kHz)

```sh
ffmpeg -i music.wav -af "aloop=loop=4:size=88200" extended.wav
```

### Infinite loop for ambient sound

```sh
ffmpeg -i ambient.flac -af "aloop=loop=-1:size=220500" -t 3600 hour_loop.wav
```

### Loop from 10 seconds in

```sh
ffmpeg -i music.mp3 -af "aloop=loop=3:size=48000:start=-1:time=10" output.wav
```

## Notes

- `size` in samples = seconds × sample_rate (e.g., 2 seconds at 48kHz = 96000).
- Unlike perfect audio loops that require sample-accurate trimming, `aloop` will create a glitch at the loop point unless the audio was already prepared for seamless looping.
- For infinite looping livestreams, combine with `-stream_loop -1` at the input level instead of `aloop` for more efficient memory use.

---

### areverse

> Reverse an audio clip in time by buffering all samples and outputting them in reverse order.

**Source:** [libavfilter/f_reverse.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_reverse.c)

The `areverse` filter plays audio backwards by buffering all samples in memory and emitting them in reverse order. It is the audio counterpart to the `reverse` video filter, and they are typically used together to create a fully reversed audio/video clip. Reverse audio is commonly used in music production (for reverse reverb effects), film sound design, and creative edits.

## Quick Start

```sh
# Reverse first 5 seconds of audio
ffmpeg -i input.wav -af "atrim=end=5,areverse" reversed.wav
```

## Parameters

None. `areverse` takes no options.

## Examples

### Reverse first 5 seconds of audio

```sh
ffmpeg -i input.mp3 -af "atrim=end=5,asetpts=PTS-STARTPTS,areverse" reversed.mp3
```

### Reverse an entire short clip

```sh
ffmpeg -i short.wav -af areverse reversed.wav
```

### Reverse audio and video together

```sh
ffmpeg -i clip.mp4 -vf reverse -af areverse reversed.mp4
```

### Reverse reverb effect (apply reverb then reverse for pre-reverb)

```sh
ffmpeg -i dry.wav -af "areverse,aecho=0.8:0.5:1000:0.5,areverse" reverse_reverb.wav
```

## Notes

- **Warning:** `areverse` buffers the entire audio in memory. For long files, trim first with `atrim=end=N`.
- Add `asetpts=PTS-STARTPTS` after `atrim` to reset audio timestamps before `areverse`.
- The reverse reverb technique: reverse the audio, apply reverb, reverse again — the reverb swells before each transient.
- Output duration matches input duration exactly.

---

### asetpts

> Recompute the presentation timestamps of audio frames using a configurable expression, mirroring the setpts filter for audio streams.

**Source:** [libavfilter/setpts.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/setpts.c)

The `asetpts` filter recomputes PTS values for audio frames using a mathematical expression — the audio equivalent of the `setpts` video filter. It is used to generate synthetic timestamps, fix desync, or adjust audio timing. For speed changes, `atempo` is usually better (it resamples to preserve pitch), but `asetpts` gives direct PTS control for cases where timing surgery is needed.

## Quick Start

```sh
# Reset audio PTS to start from zero (after atrim)
ffmpeg -i input.mp4 -af "atrim=start=10,asetpts=PTS-STARTPTS" trimmed.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string | `PTS` | Expression evaluated per frame to compute output PTS. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | Current input PTS. |
| `N` | Cumulative number of consumed samples (not including current frame). |
| `NB_SAMPLES` / `S` | Number of samples in the current frame. |
| `SAMPLE_RATE` / `SR` | Audio sample rate. |
| `TB` | Timebase of input. |
| `STARTPTS` | PTS of the first frame. |
| `T` | Time in seconds of current frame. |

## Examples

### Reset timestamps after trim

```sh
ffmpeg -i input.wav -af "atrim=start=5,asetpts=PTS-STARTPTS" trimmed.wav
```

### Generate timestamps from sample count (most accurate)

```sh
ffmpeg -i input.wav -af "asetpts=N/SR/TB" resampled.wav
```

### Fix broken audio timestamps

```sh
ffmpeg -i broken.mp4 -af "asetpts=N/SR/TB" fixed.mp4
```

### Add a 2-second audio delay

```sh
ffmpeg -i input.wav -af "asetpts=PTS+2/TB" delayed.wav
```

## Notes

- `asetpts=PTS-STARTPTS` is the standard fix after `atrim` to reset audio to start at time 0.
- `N/SR/TB` generates PTS purely from sample counting — the most robust approach when input timestamps are unreliable.
- For actual playback speed change, use `atempo` (pitch-corrected) instead of `asetpts`.
- `asetpts` and `setpts` can be used together to keep audio/video in sync after timeline manipulation.

---

### decimate

> Drop duplicate frames from video to achieve the target frame rate, used as the second stage of inverse telecine after fieldmatch.

**Source:** [libavfilter/vf_decimate.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_decimate.c)

The `decimate` filter removes duplicate frames at regular intervals to reduce frame rate — the second stage of a `fieldmatch` + `decimate` IVTC pipeline. For every N frames (cycle), it identifies the most similar consecutive frame pair and drops one, effectively converting 29.97fps telecined video back to 23.976fps progressive. It can also be used independently to reduce frame rate by dropping duplicate frames in any content.

## Quick Start

```sh
# IVTC: match fields then drop duplicates (30i → 24p)
ffmpeg -i telecined.ts -vf "fieldmatch,decimate" progressive.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cycle | int | `5` | Number of frames per group; one frame per group is dropped. Default 5 converts 30fps to 24fps. |
| dupthresh | double | `1.1` | Threshold below which a frame is considered a duplicate. |
| scthresh | double | `15.0` | Scene change detection threshold; prevents dropping across cuts. |
| blockx | int | `32` | Block width for difference metric calculations. |
| blocky | int | `32` | Block height for difference metric calculations. |
| ppsrc | bool | `0` | Use second stream as pre-processed reference for duplicate detection. |
| chroma | bool | `1` | Include chroma in duplicate detection. |
| mixed | bool | `false` | Handle input with mixed decimated and non-decimated content. |

## Examples

### Full IVTC pipeline

```sh
ffmpeg -i telecined_ntsc.ts -vf "fieldmatch,decimate" -r 24000/1001 progressive.mp4
```

### With yadif fallback for mixed content

```sh
ffmpeg -i mixed.ts -vf "fieldmatch,yadif=deint=interlaced,decimate" output.mp4
```

### Pre-processed source for better detection

```sh
ffmpeg -i input.ts \
  -filter_complex "[0:v]yadif=1[pp];[0:v][pp]fieldmatch=ppsrc=1,decimate=ppsrc=1[out]" \
  -map "[out]" output.mp4
```

### Drop every 5th duplicate frame independently

```sh
ffmpeg -i 30fps_video.mp4 -vf "decimate=cycle=5" 24fps_video.mp4
```

## Notes

- `cycle=5` = drop 1 in 5 frames: 30fps → 24fps, or 29.97fps → 23.976fps.
- A high `dupthresh` (e.g., 3.0) is more permissive about calling frames duplicates; lower values are stricter.
- Scene change detection (`scthresh`) prevents incorrectly dropping the first frame of a new scene.
- Currently requires constant frame rate input — for VFR input, prepend `fps=30000/1001` first.

---

### deflicker

> Reduce temporal luminance flickering in video by smoothing per-frame brightness variations over a moving window.

**Source:** [libavfilter/vf_deflicker.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_deflicker.c)

The `deflicker` filter reduces temporal luminance flickering — rapid frame-to-frame brightness variation caused by fluorescent lighting, high-speed cameras shooting at certain shutter speeds, or digitized analog sources. It computes a moving-window average of frame brightness (using one of several averaging modes) and normalizes each frame toward that average. The video content is otherwise unmodified.

## Quick Start

```sh
ffmpeg -i flickery.mp4 -vf deflicker output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| size / s | int | `5` | Window size in frames (2–129). Larger = smoother but more blur across brightness changes. |
| mode / m | int | `am` | Averaging mode: `am` (arithmetic), `gm` (geometric), `hm` (harmonic), `qm` (quadratic), `cm` (cubic), `pm` (power), `median`. |
| bypass | bool | `0` | Don't modify frames, only attach metadata (useful for analysis). |

## Examples

### Default deflicker

```sh
ffmpeg -i flickery_timelapse.mp4 -vf deflicker stabilized.mp4
```

### Larger window for slower, steadier correction

```sh
ffmpeg -i flickery.mp4 -vf "deflicker=size=15" output.mp4
```

### Median mode (robust to outlier bright/dark frames)

```sh
ffmpeg -i input.mp4 -vf "deflicker=mode=median:size=9" output.mp4
```

### Analysis only (metadata without modification)

```sh
ffmpeg -i input.mp4 -vf "deflicker=bypass=1" -f null -
```

## Notes

- Arithmetic mean (`am`) is a good default for most content.
- `median` mode is more robust against frames that are extreme outliers (e.g., a single very bright flash), which could skew a mean-based correction.
- For timelapse footage, a larger window (10–30) and `gm` (geometric mean) typically produces the smoothest results.
- `bypass=1` attaches `lavfi.deflicker.scale` metadata without changing the video — useful to inspect the correction magnitude.

---

### dejudder

> Remove judder from video with uneven frame durations, typically introduced by inverse telecine or mixed-cadence sources.

**Source:** [libavfilter/vf_dejudder.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_dejudder.c)

The `dejudder` filter removes judder from video that has uneven frame durations due to telecine conversion or mixed-cadence sources. Judder is the irregular motion stutter that appears when 24fps film is converted to 29.97fps (NTSC) without proper 3:2 cadence handling — frames alternate between 2-field and 3-field durations. `dejudder` detects the repeating cadence pattern and smooths the output timing. It may change the container's recorded frame rate.

## Quick Start

```sh
# Remove NTSC telecine judder
ffmpeg -i juddering.ts -vf "pullup,dejudder" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cycle | int | `4` | Length of the judder cycle in frames. `4` = 24→30fps NTSC; `5` = 25→30fps PAL; `20` = mixed. |

## Examples

### Remove NTSC 3:2 pulldown judder

```sh
ffmpeg -i ntsc_judder.ts -vf "pullup,dejudder" clean.mp4
```

### Remove PAL 25→30 pulldown judder

```sh
ffmpeg -i pal_judder.ts -vf "dejudder=cycle=5" clean.mp4
```

### Full IVTC pipeline with dejudder

```sh
ffmpeg -i telecined.ts -vf "fieldmatch,dejudder,fps=30000/1001,decimate" progressive.mp4
```

## Notes

- `dejudder` on its own does not remove duplicate frames — it only corrects the timing. Pair with `decimate` or `fps` to also remove duplicates.
- `cycle=4` is for the classic 24fps NTSC conversion (2 frames at 2 fields, 1 frame at 3 fields repeating over 4 frames).
- Aside from frame rate changes in metadata, `dejudder` has no effect on constant-frame-rate video.
- This filter is safe to apply as part of a post-`pullup` pipeline to clean up any residual timing irregularities.

---

### loop

> Loop a segment of video frames a specified number of times or infinitely.

**Source:** [libavfilter/f_loop.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_loop.c)

The `loop` filter repeats a segment of video frames N times. By buffering a specified number of frames and replaying them, it can create a seamless loop from any segment of a video. This is useful for creating looping backgrounds, extending short clips, or generating infinite loops for displays.

## Quick Start

```sh
# Loop the first 30 frames 5 times
ffmpeg -i input.mp4 -vf "loop=loop=5:size=30:start=0" looped.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| loop | int | `0` | Number of loop iterations. `0` = no looping; `-1` = infinite. |
| size | int64 | `0` | Maximum number of frames to buffer for the loop segment. |
| start | int64 | `0` | Frame number where the loop segment starts. |
| time | duration | — | Loop start time in seconds (used instead of `start` when `start=-1`). |

## Examples

### Loop first 30 frames 5 times

```sh
ffmpeg -i short_clip.mp4 -vf "loop=loop=5:size=30:start=0" extended.mp4
```

### Infinite loop of first frame (static image from video)

```sh
ffmpeg -i input.mp4 -vf "loop=loop=-1:size=1:start=0" -t 30 static.mp4
```

### Loop a specific 60-frame segment starting at frame 100

```sh
ffmpeg -i input.mp4 -vf "loop=loop=3:size=60:start=100" looped.mp4
```

### Loop from a time offset

```sh
ffmpeg -i input.mp4 -vf "loop=loop=10:size=25:start=-1:time=5.0" output.mp4
```

## Notes

- `size` sets the buffer size — it must be at least as large as the segment you want to loop.
- Memory usage scales with `size` × frame dimensions × pixel format.
- For audio looping, use `aloop` with the same `loop`/`size`/`start` logic applied to samples.
- Combine with `trim` to extract exactly the segment you want to loop first.

---

### reverse

> Reverse a video clip in time by buffering all frames and outputting them in reverse order.

**Source:** [libavfilter/f_reverse.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/f_reverse.c)

The `reverse` filter plays a video clip backwards by buffering all frames in memory and then emitting them in reverse order. It requires the complete clip to be buffered before any output is produced. This is commonly used for creative reverse effects, slow-motion reversal, or generating mirror/palindrome edits. Always trim the input first to limit memory usage.

## Quick Start

```sh
# Reverse the first 5 seconds of a video
ffmpeg -i input.mp4 -vf "trim=end=5,reverse" reversed.mp4
```

## Parameters

None. `reverse` takes no options.

## Examples

### Reverse the first 5 seconds

```sh
ffmpeg -i input.mp4 -vf "trim=end=5,setpts=PTS-STARTPTS,reverse" reversed.mp4
```

### Reverse an entire short clip

```sh
ffmpeg -i short_clip.mp4 -vf reverse reversed.mp4
```

### Create a boomerang effect (forward + reverse)

```sh
ffmpeg -i clip.mp4 \
  -filter_complex "[0:v]split[a][b];[b]reverse[rev];[a][rev]concat=n=2:v=1:a=0" \
  boomerang.mp4
```

### Reverse with audio

```sh
ffmpeg -i clip.mp4 -vf reverse -af areverse reversed_av.mp4
```

## Notes

- **Warning:** `reverse` buffers the entire clip in memory. For long videos, trim first with `trim=end=N`.
- Always add `setpts=PTS-STARTPTS` after `trim` to reset timestamps before passing to `reverse`.
- Use both `reverse` and `areverse` together to reverse audio and video simultaneously.
- This is a single-pass operation — the output duration matches the input duration exactly.

---

### setdar

> Set the display aspect ratio (DAR) of a video stream by adjusting the sample aspect ratio (SAR), without scaling pixels.

**Source:** [libavfilter/vf_aspect.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/vf_aspect.c)

The `setdar` filter sets the Display Aspect Ratio (DAR) of a video stream by changing the Sample Aspect Ratio (SAR) metadata — it does **not** rescale the pixels. This is used to correct mislabeled anamorphic content (e.g., 720×576 material that should display as 16:9 but is incorrectly tagged as 4:3), or to override the aspect ratio for a specific output format.

## Quick Start

```sh
# Tag a 720x576 frame as 16:9 display aspect
ffmpeg -i input.mp4 -vf "setdar=dar=16/9" output.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dar / ratio / r | string | `0` | Display aspect ratio as a fraction (`16/9`), decimal (`1.7778`), or expression. `0` = keep input DAR. |
| max | int | `100` | Maximum numerator/denominator when reducing the ratio to a fraction. |

## Expression Variables (for `dar`)

| Variable | Description |
|----------|-------------|
| `w`, `h` | Input frame width and height. |
| `a` | `w / h` (pixel aspect). |
| `sar` | Input sample aspect ratio. |
| `dar` | Input display aspect ratio. |

## Examples

### Set to 16:9

```sh
ffmpeg -i anamorphic.mp4 -vf "setdar=dar=16/9" corrected.mp4
```

### Set to 4:3

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=4/3" output.mp4
```

### Set using decimal value

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=1.7778" widescreen.mp4
```

### Compute DAR based on pixel dimensions (no-op, keeps correct DAR)

```sh
ffmpeg -i input.mp4 -vf "setdar=dar=w/h" output.mp4
```

## Notes

- `setdar` changes the SAR in the bitstream headers — the pixel data is unchanged. Players that respect SAR will display correctly; players that ignore SAR will show the raw pixel dimensions.
- DAR = `(width / height) × SAR`. If you have 720×576 pixels at SAR 64:45, DAR = `(720/576) × (64/45) = 16/9`.
- To actually resize pixels to match the aspect ratio, use `scale=1280:720` or `scale=iw*sar:ih`.
- Use `ffprobe` to check the current DAR/SAR values before applying this filter.

---

### setpts

> Recompute the presentation timestamps (PTS) of video frames using a configurable expression, enabling speed changes, timestamp fixes, and creative timing effects.

**Source:** [libavfilter/setpts.c](https://github.com/FFmpeg/FFmpeg/blob/master/libavfilter/setpts.c)

The `setpts` filter recomputes the PTS (Presentation Timestamp) of each video frame using a mathematical expression. This is the primary way to change video speed, fix broken timestamps, generate synthetic timestamps, or apply custom timing curves. The expression has access to the current PTS, frame number, timebase, and other variables.

## Quick Start

```sh
# Double the playback speed (2×)
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" fast.mp4
```

## Parameters

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expr | string | `PTS` | Expression evaluated per frame to set the output PTS. |

## Expression Variables

| Variable | Description |
|----------|-------------|
| `PTS` | Current input PTS. |
| `N` | Frame number (starts at 0). |
| `T` | Time in seconds of current frame. |
| `TB` | Timebase of input. |
| `STARTPTS` | PTS of the first frame. |
| `STARTT` | Time in seconds of the first frame. |
| `FRAME_RATE` / `FR` | Framerate (only for CFR video). |
| `PREV_INPTS` / `PREV_OUTT` | Previous input/output PTS. |
| `INTERLACED` | Whether current frame is interlaced. |

## Examples

### 2× speed (half duration)

```sh
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" fast.mp4
```

### 0.5× speed (double duration, slow motion)

```sh
ffmpeg -i input.mp4 -vf "setpts=2.0*PTS" slow.mp4
```

### Reset timestamps to start from zero

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS-STARTPTS" fixed.mp4
```

### Force constant 25fps timestamps (fix VFR input)

```sh
ffmpeg -i vfr_input.mp4 -vf "setpts=N/(25*TB)" cfr_25fps.mp4
```

### Add 10-second offset to timestamps

```sh
ffmpeg -i input.mp4 -vf "setpts=PTS+10/TB" offset.mp4
```

## Notes

- When changing speed with `setpts`, the audio is not affected — use `atempo` or `asetpts` to sync audio.
- `setpts=PTS-STARTPTS` is the standard fix for clips that start at a non-zero PTS (e.g., after `trim`).
- Combine `setpts=0.5*PTS` with `-r 60` to create smooth slow motion from high-fps source.
- The expression is evaluated per frame using FFmpeg's `av_expr_eval` — you can use any math function.

---
