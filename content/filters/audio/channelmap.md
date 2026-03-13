+++
title = "channelmap"
description = "Remap audio channels — reorder, duplicate, or select specific channels from the input to produce a different output channel layout."
date = 2024-01-01

[taxonomies]
category = ["audio"]
tags = ["channel", "routing", "utility"]

[extra]
filter_type = "audio"
since = ""
see_also = ["channelsplit", "pan", "amerge"]
parameters = ["map", "channel_layout"]
cohort = 2
+++

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
