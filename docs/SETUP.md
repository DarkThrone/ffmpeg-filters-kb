# Setup Guide

## GitHub Secrets Required

In your GitHub repository Settings → Secrets and variables → Actions, add:

| Secret | Description |
|--------|-------------|
| `ALGOLIA_APP_ID` | Your Algolia Application ID |
| `ALGOLIA_ADMIN_KEY` | Algolia Admin API Key (write access, never expose publicly) |

## Algolia Public Key

The search-only (public) key goes in `config.toml` under `extra.algolia_search_key`.
This is safe to commit — it has read-only access.

## GitHub Pages

Enable GitHub Pages in repository Settings → Pages:
- Source: GitHub Actions
- The workflow will deploy automatically on every push to `main`.
