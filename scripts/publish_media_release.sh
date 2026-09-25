#!/usr/bin/env bash
# Upload the full-quality media originals to a GitHub Release, so that the
# "Download original" buttons on the /media/ page work.
#
# The files are the ones listed in content/media/manifest.json ("release" entries),
# taken from media_originals/release/ (git-ignored). Release assets do NOT go into
# the git history and do NOT count toward the GitHub Pages size limit.
#
# Requires the GitHub CLI:   brew install gh && gh auth login
#
# Usage:
#   scripts/publish_media_release.sh             # create the release (or add/replace files)
#   scripts/publish_media_release.sh --dry-run   # only show what would be uploaded
set -euo pipefail
cd "$(dirname "$0")/.."

REPO=${REPO:-garico92/website}
MANIFEST=content/media/manifest.json
DIR=media_originals/release
DRY=${1:-}

TAG=$(python3 -c "import json; print(json.load(open('$MANIFEST'))['release_tag'])")
FILES=()
while IFS= read -r f; do FILES+=("$DIR/$f"); done < <(python3 - "$MANIFEST" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
for item in m["items"].values():
    if "release" in item:
        print(item["release"]["file"])
PY
)

echo "Release $TAG on $REPO:"
for f in "${FILES[@]}"; do
    [ -f "$f" ] || { echo "  missing: $f  (run scripts/make_web_media.py)"; exit 1; }
    printf "  %-45s %6s MB\n" "$(basename "$f")" "$(( $(wc -c < "$f") / 1000000 ))"
done
[ "$DRY" = "--dry-run" ] && exit 0

command -v gh >/dev/null || { echo "GitHub CLI not found: brew install gh && gh auth login"; exit 1; }

if gh release view "$TAG" -R "$REPO" >/dev/null 2>&1; then
    gh release upload "$TAG" "${FILES[@]}" -R "$REPO" --clobber
else
    gh release create "$TAG" "${FILES[@]}" -R "$REPO" --target main --latest=false \
        --title "Website media — full-quality originals" \
        --notes "Full-resolution originals of the pictures, videos and animations shown on https://garico92.github.io/website/media/. Released under CC BY 4.0 — credit: Giovanni Aricò."
fi

echo "Checking download links..."
BASE="https://github.com/$REPO/releases/download/$TAG"
for f in "${FILES[@]}"; do
    code=$(curl -s -o /dev/null -w '%{http_code}' -I "$BASE/$(basename "$f")")
    echo "  $code  $BASE/$(basename "$f")"
done
