Code to generate my website. Based on https://github.com/HugoBlox/theme-academic-cv.

## Media page (`/media/`)

Heavy pictures and videos are **never committed**. The workflow is:

1. Put the originals in `media_originals/` (git-ignored).
2. Describe them in `ITEMS` at the top of `scripts/make_web_media.py`, then run
   `python scripts/make_web_media.py` (needs `ffmpeg` and `Pillow`). It writes
   - light web versions + `manifest.json` into `content/media/` (committed),
   - full-quality files for download into `media_originals/release/`.
3. Add a `{{< media-item id="..." >}}` block with the description to `content/media/index.md`.
4. Upload the originals to the GitHub Release with `scripts/publish_media_release.sh`
   (the "Download original" buttons point there).

The pre-commit hook (`hooks/`, enabled with `git config core.hooksPath hooks`) refuses files above 50 MB.
