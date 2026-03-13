# FFmpeg Filters Reference

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/U7U31VWKOY)

A modern, searchable reference for FFmpeg audio and video filters — detailed parameters, practical examples, and source-informed documentation. Built with [Zola](https://www.getzola.org/) and deployed to GitHub Pages.

**Live site:** https://darkthrone.github.io/ffmpeg-filters-kb

---

## Setup

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| [Zola](https://www.getzola.org/documentation/getting-started/installation/) | 0.22.1 | `brew install zola` |
| Python | 3.11+ | `brew install python` |
| FFmpeg source (optional, for extraction) | latest | `git clone https://github.com/FFmpeg/FFmpeg` |

### Local development

```sh
git clone https://github.com/DarkThrone/ffmpeg-filters-kb
cd ffmpeg-filters-kb
zola serve
```

Open http://127.0.0.1:1111 in your browser. Zola watches for changes and hot-reloads automatically.

### Build for production

```sh
zola build
# Output is in ./public/
```

---

## Adding new filter documentation

### 1. Extract filter metadata from FFmpeg source

```sh
python3 scripts/extract_filters.py \
  --ffmpeg-src /path/to/FFmpeg \
  --filters filtername1 filtername2
```

This writes `filter_data/{name}.json` for each filter (gitignored — regenerate locally).

### 2. Write the Markdown page

Create `content/filters/{category}/{filtername}.md` with TOML front matter:

```toml
+++
title = "filtername"
description = "One-line description."
date = 2024-01-01

[taxonomies]
category = ["video"]  # or "audio", "sources", etc.
tags = ["tag1", "tag2"]

[extra]
filter_type = "video"
since = ""
see_also = ["other_filter"]
parameters = ["param1", "param2"]
source_file = "libavfilter/vf_filtername.c"
cohort = 1
+++
```

Follow with the page body:

```
## Quick Start
## Parameters (table)
## Examples
## Notes
```

### 3. Rebuild the site

```sh
zola build
```

---

## Search (Algolia)

Search is powered by Algolia. To index locally:

```sh
pip install "algoliasearch>=3.0,<4.0" python-frontmatter toml
export ALGOLIA_APP_ID=your_app_id
export ALGOLIA_ADMIN_KEY=your_admin_key
export ALGOLIA_INDEX=ffmpeg_filters
python3 scripts/index_algolia.py
```

Add `algolia_app_id`, `algolia_search_key`, and `algolia_index` to `config.toml` under `[extra]` to enable search in the UI.

---

## Deployment

The site deploys automatically via GitHub Actions on every push to `main`. See `.github/workflows/deploy.yml`.

To enable it on a fork:
1. Go to **Settings → Pages → Source** and select **GitHub Actions**
2. Add `ALGOLIA_APP_ID` and `ALGOLIA_ADMIN_KEY` to **Settings → Secrets → Actions** (optional, only needed for search indexing)

---

## Project structure

```
content/filters/
  video/        ← video filter pages
  audio/        ← audio filter pages
  sources/      ← test source filter pages
  visualization/
  analysis/
  interlace/
  utility/
scripts/
  extract_filters.py   ← pulls metadata from FFmpeg source
  index_algolia.py     ← pushes records to Algolia
templates/             ← Zola/Tera HTML templates
sass/                  ← SCSS design system
static/
  js/app.js            ← search, sidebar, keyboard shortcuts
  LLM.md               ← full content dump for LLM ingestion
```

---

## License

[MIT](LICENSE) — fork freely, contributions welcome.
