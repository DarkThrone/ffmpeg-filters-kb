+++
title = "zoompan"
description = "Apply a Ken Burns-style zoom and pan effect, animating position and zoom level across still or video frames."
date = 2024-01-01

[taxonomies]
category = ["video"]
tags = ["transform", "zoom", "animation"]

[extra]
filter_type = "video"
since = ""
see_also = ["scale", "crop", "setpts"]
parameters = ["zoom", "x", "y", "d", "s", "fps"]
cohort = 1
source_file = "libavfilter/vf_zoompan.c"
+++

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
