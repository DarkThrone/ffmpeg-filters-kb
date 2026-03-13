+++
title = "signature"
description = "Compute the MPEG-7 video signature fingerprint for duplicate detection, and optionally match two input streams to find time offsets."
date = 2024-01-01

[taxonomies]
category = ["analysis"]
tags = ["analysis", "video", "fingerprint", "duplicate"]

[extra]
filter_type = "analysis"
since = ""
see_also = ["psnr", "ssim"]
parameters = ["detectmode", "nb_inputs", "filename", "format", "th_d", "th_dc", "th_xh", "th_di", "th_it"]
cohort = 3
source_file = "libavfilter/vf_signature.c"
+++

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
