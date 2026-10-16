#!/usr/bin/env python3
"""
make_web_media.py - build light, web-ready versions of heavy media for the /media/ page.

Layout
------
media_originals/            original files (git-ignored, never committed)
media_originals/release/    full-quality files to attach to the GitHub Release
content/media/              light versions shown on the website (committed)
content/media/manifest.json sizes/dimensions read by the `media-item` shortcode

Requirements
------------
ffmpeg + ffprobe on PATH (with libx264, libaom-av1), Python >= 3.9, Pillow (with WebP).

Usage
-----
python scripts/make_web_media.py                      # build whatever is missing
python scripts/make_web_media.py --only video         # video | loop | image | ready
python scripts/make_web_media.py --only video --step av1   # a single step (see --help)
python scripts/make_web_media.py --force              # rebuild even if outputs exist
python scripts/make_web_media.py --list               # print outputs and sizes

Adding a new item
-----------------
1. Put the original in media_originals/ (or, for a video that is already web-sized, kind "ready":
   put it directly in content/media/; it is then also the download, no release upload needed).
2. Add an entry to ITEMS below (copy one of the existing ones).
3. Run this script, then add a {{< media-item id="..." >}} block to content/media/index.md.
4. Upload media_originals/release/<release_name> to the GitHub Release (scripts/publish_media_release.sh).
"""
from __future__ import annotations

import argparse
import io
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # our composites are intentionally huge

ROOT = Path(__file__).resolve().parents[1]
ORIG = ROOT / "media_originals"
RELEASE = ORIG / "release"
OUT = ROOT / "content" / "media"
MANIFEST = OUT / "manifest.json"

RELEASE_TAG = "media-v1"
RELEASE_BASE = f"https://github.com/garico92/website/releases/download/{RELEASE_TAG}/"

# --------------------------------------------------------------------------------------
# What to build. `id` is used for output file names and by the shortcode.
# --------------------------------------------------------------------------------------
ITEMS = [
    {
        "id": "nenya-composite-zoom",
        "kind": "image",
        "source": "composite_zoom_nenya_cluster_dm_twilight_full_SQ_4K_v0.png",
        "release_name": "nenya_composite_zoom_4096px.png",
        "preview_width": 1600,   # inline image (Hugo derives smaller srcset sizes from it)
        "preview_quality": 82,
        "tile_size": 1024,       # deep-zoom tiles (OpenSeadragon / DZI)
        "tile_overlap": 1,
        "tile_quality": 85,
    },
    {
        "id": "nenya-orbit-dive",
        "kind": "video",
        "source": "orbit_dive_nenya_cluster_dm_twilight_full_FHD_30s_24fps.mp4",
        "release_name": "nenya_orbit_dive_1080p_25s.mp4",
        "trim_end_s": 5.0,       # drop the last 5 s (too much shot noise)
        "hold_end_s": 2.0,       # web versions: freeze the last frame for 2 s (no abrupt ending)
        "poster_time_s": 18.5,   # frame shown before playback
        "poster_width": 1280,
        "poster_quality": 75,
        # Order matters only for the manifest; the shortcode decides the <source> order.
        # H.264 two-pass at a fixed bitrate: CRF-based encodes of this particle-noise
        # content are huge (> 60 Mbit/s). AV1 was tested (SVT-AV1, libaom) and did not
        # beat H.264 at equal size here, so it is not used; add
        #   {"name": "1080p_av1", "height": 1080, "codec": "av1", "bitrate": "6M"}
        # for smoother content. The shortcode serves 720p to phones, 1080p otherwise.
        "renditions": [
            {"name": "1080p", "height": 1080, "codec": "h264", "bitrate": "10M"},
            {"name": "720p", "height": 720, "codec": "h264", "bitrate": "4M"},
        ],
    },
    {
        "id": "baryonification",
        "kind": "loop",          # GIF -> looping, muted, autoplaying MP4
        "source": "baryonification.gif",
        "release_name": None,    # no release copy: the web MP4 itself is the download
        "crf": 20,
    },
    {
        "id": "periodic-boundary-conditions",
        "kind": "ready",         # already web-sized: lives directly in content/media/, no re-encode
        "file": "periodic_boundary_conditions.mp4",
        "poster_time_s": 28.0,
        "poster_width": 1280,
        "poster_quality": 80,
    },
]


# --------------------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------------------
def run(cmd: list[str], capture: bool = False) -> str:
    print("  $", " ".join(str(c) for c in cmd), flush=True)
    res = subprocess.run([str(c) for c in cmd], check=True, text=True,
                         stdout=subprocess.PIPE if capture else None,
                         stderr=subprocess.PIPE if capture else None)
    return res.stdout if capture else ""


def ffmpeg_major() -> int:
    out = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout
    m = re.search(r"ffmpeg version n?(\d+)", out)
    return int(m.group(1)) if m else 4


def has_encoder(name: str) -> bool:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout
    return re.search(rf"\s{re.escape(name)}\s", out) is not None


def vfr_flag() -> list[str]:
    # -vsync was replaced by -fps_mode in ffmpeg 5.1
    return ["-fps_mode", "vfr"] if ffmpeg_major() >= 6 else ["-vsync", "vfr"]


def probe(path: Path) -> dict:
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=width,height,r_frame_rate,nb_frames,codec_name",
               "-show_entries", "format=duration", "-of", "json", path], capture=True)
    d = json.loads(out)
    s = d["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return {"width": s["width"], "height": s["height"], "fps": num / den,
            "codec": s.get("codec_name"), "nb_frames": int(s.get("nb_frames") or 0),
            "duration": float(d["format"]["duration"])}


def mb(n: int) -> str:
    return f"{n / 1e6:.1f} MB"


def needs(path: Path, force: bool) -> bool:
    if force or not path.exists() or path.stat().st_size == 0:
        return True
    print(f"  = {path.relative_to(ROOT)} exists, skipping (use --force to rebuild)")
    return False


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {}


def save_manifest(man: dict) -> None:
    man["release_tag"] = RELEASE_TAG
    man["release_base"] = RELEASE_BASE
    man.setdefault("items", {})
    MANIFEST.write_text(json.dumps(man, indent=2, sort_keys=True) + "\n")
    print(f"  -> {MANIFEST.relative_to(ROOT)}")


def webp_from_frame(src: Path, t: float, width: int, out: Path, quality: int = 80) -> None:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1",
                          "-f", "image2pipe", "-vcodec", "png", "-"],
                         check=True, capture_output=True).stdout
    im = Image.open(io.BytesIO(png)).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    im.save(out, "WEBP", quality=quality, method=6)


# --------------------------------------------------------------------------------------
# video
# --------------------------------------------------------------------------------------
def clean_cut_packets(src: Path, keep_frames: int) -> tuple[int, int]:
    """Smallest number of packets (decode order) that can be stream-copied without
    breaking B-frame references and that contains at least `keep_frames` frames.
    Returns (n_packets, n_frames_in_output)."""
    out = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts",
               "-of", "csv=p=0", src], capture=True)
    pts = [int(x) for x in out.split() if x.strip().lstrip("-").isdigit()]
    rank = {p: i for i, p in enumerate(sorted(pts))}
    disp = [rank[p] for p in pts]
    seen, maxd = 0, -1
    for i, d in enumerate(disp):
        # a new reference frame starts here and everything before it is complete
        if i > 0 and d > maxd and seen == maxd + 1 and maxd + 1 >= keep_frames:
            return i, maxd + 1
        seen += 1
        maxd = max(maxd, d)
    return len(disp), len(disp)


def build_video(item: dict, force: bool, step: str | None) -> dict:
    src = ORIG / item["source"]
    info = probe(src)
    fps = info["fps"]
    keep = int(round((info["duration"] - item.get("trim_end_s", 0)) * fps))
    print(f"  source {info['width']}x{info['height']} @ {fps:g} fps, {info['duration']:.2f} s "
          f"-> keeping {keep} frames ({keep / fps:.2f} s)")
    entry = {"kind": "video", "width": info["width"], "height": info["height"], "fps": fps,
             "duration_s": round(keep / fps, 2), "hold_end_s": item.get("hold_end_s", 0),
             "renditions": {}}

    # poster
    poster = OUT / f"{item['id']}_poster.webp"
    if step in (None, "poster") and needs(poster, force):
        webp_from_frame(src, item.get("poster_time_s", 0), item.get("poster_width", 1280), poster,
                        quality=item.get("poster_quality", 75))
    entry["poster"] = poster.name

    # web renditions
    tmpdir = Path(tempfile.mkdtemp(prefix="passlog_", dir=ORIG))
    try:
        for r in item["renditions"]:
            out = OUT / f"{item['id']}_{r['name']}.mp4"
            run_this = step in (None, r["codec"], r["name"])
            if run_this and needs(out, force):
                t0 = time.time()
                filters = [f"trim=end_frame={keep}", "setpts=PTS-STARTPTS"]
                if item.get("hold_end_s"):
                    filters.append(f"tpad=stop_mode=clone:stop_duration={item['hold_end_s']}")
                if r["height"] != info["height"]:
                    filters.append(f"scale=-2:{r['height']}:flags=lanczos")
                common = ["ffmpeg", "-y", "-v", "error", "-stats", "-i", src, "-map", "0:v:0",
                          "-vf", ",".join(filters), "-an"]
                if r["codec"] == "h264":
                    br = r["bitrate"]
                    peak = f"{2 * int(br.rstrip('M'))}M"
                    log = tmpdir / f"{r['name']}"
                    x264 = ["-c:v", "libx264", "-preset", "slow", "-b:v", br, "-passlogfile", log]
                    run([*common, *x264, "-pass", "1", "-f", "mp4", "/dev/null"])
                    run([*common, *x264, "-pass", "2", "-maxrate", peak, "-bufsize", peak,
                         "-pix_fmt", "yuv420p", "-profile:v", "high", "-level:v", "4.1",
                         "-tag:v", "avc1", "-movflags", "+faststart", out])
                elif r["codec"] == "av1":
                    if has_encoder("libsvtav1"):  # much faster than libaom, same quality
                        enc = ["-c:v", "libsvtav1", "-preset", "6", "-b:v", r["bitrate"]]
                    else:
                        enc = ["-c:v", "libaom-av1", "-b:v", r["bitrate"], "-cpu-used", "6",
                               "-row-mt", "1", "-tiles", "2x2"]
                    run([*common, *enc, "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
                else:
                    raise ValueError(r["codec"])
                print(f"  -> {out.name}: {mb(out.stat().st_size)} in {time.time() - t0:.0f} s")
            if out.exists():
                entry["renditions"][r["name"]] = {"file": out.name, "bytes": out.stat().st_size,
                                                  "codec": r["codec"], "height": r["height"]}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # trimmed original for the GitHub Release (lossless stream copy)
    rel = RELEASE / item["release_name"]
    if step in (None, "release") and needs(rel, force):
        n_pk, n_fr = clean_cut_packets(src, keep)
        print(f"  stream-copying {n_pk} packets -> {n_fr} frames ({n_fr / fps:.2f} s)")
        run(["ffmpeg", "-y", "-v", "error", "-i", src, "-map", "0:v:0", "-c", "copy",
             "-frames:v", str(n_pk), "-movflags", "+faststart", rel])
        err = subprocess.run(["ffmpeg", "-v", "error", "-i", str(rel), "-f", "null", "-"],
                             capture_output=True, text=True).stderr.strip()
        if err:
            print("  !! decode errors in trimmed original:\n" + err, file=sys.stderr)
    if rel.exists():
        ri = probe(rel)
        entry["release"] = {"file": rel.name, "bytes": rel.stat().st_size,
                            "duration_s": round(ri["duration"], 2)}
    return entry


# --------------------------------------------------------------------------------------
# looping animation (GIF -> MP4)
# --------------------------------------------------------------------------------------
def build_loop(item: dict, force: bool, step: str | None) -> dict:
    src = ORIG / item["source"]
    info = probe(src)
    out = OUT / f"{item['id']}.mp4"
    poster = OUT / f"{item['id']}_poster.webp"
    if step in (None, "mp4") and needs(out, force):
        run(["ffmpeg", "-y", "-v", "error", "-i", src, *vfr_flag(),
             "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2:flags=lanczos",
             "-c:v", "libx264", "-preset", "veryslow", "-tune", "animation", "-crf", str(item.get("crf", 20)),
             "-pix_fmt", "yuv420p", "-profile:v", "high", "-tag:v", "avc1",
             "-movflags", "+faststart", "-an", out])
        print(f"  -> {out.name}: {mb(out.stat().st_size)} (GIF was {mb(src.stat().st_size)})")
    if step in (None, "poster") and needs(poster, force):
        webp_from_frame(src, 0, info["width"], poster, quality=85)
    entry = {"kind": "loop", "width": info["width"], "height": info["height"],
             "duration_s": round(info["duration"], 2), "poster": poster.name}
    if out.exists():
        entry["file"] = out.name
        entry["bytes"] = out.stat().st_size
    if item.get("release_name"):
        rel = RELEASE / item["release_name"]
        if step in (None, "release") and needs(rel, force):
            shutil.copy2(src, rel)
        if rel.exists():
            entry["release"] = {"file": rel.name, "bytes": rel.stat().st_size}
    elif out.exists():
        # the light MP4 on the website is also what the download button serves
        entry["download"] = {"file": out.name, "bytes": out.stat().st_size}
    return entry


# --------------------------------------------------------------------------------------
# image (preview + deep-zoom tiles + losslessly optimised PNG)
# --------------------------------------------------------------------------------------
def write_dzi(im: Image.Image, out_dir: Path, name: str, tile: int, overlap: int, quality: int) -> int:
    """Deep Zoom Image pyramid (the format OpenSeadragon reads). Returns number of tiles."""
    W, H = im.size
    max_level = math.ceil(math.log2(max(W, H)))
    files = out_dir / f"{name}_files"
    if files.exists():
        shutil.rmtree(files)
    n = 0
    level_im = im
    for level in range(max_level, -1, -1):
        scale = 2 ** (max_level - level)
        w, h = max(1, math.ceil(W / scale)), max(1, math.ceil(H / scale))
        if level_im.size != (w, h):
            level_im = level_im.resize((w, h), Image.LANCZOS)
        d = files / str(level)
        d.mkdir(parents=True, exist_ok=True)
        for c in range(math.ceil(w / tile)):
            for r in range(math.ceil(h / tile)):
                x0 = c * tile - (overlap if c else 0)
                y0 = r * tile - (overlap if r else 0)
                x1 = min(c * tile + tile + overlap, w)
                y1 = min(r * tile + tile + overlap, h)
                level_im.crop((x0, y0, x1, y1)).save(d / f"{c}_{r}.webp", "WEBP", quality=quality, method=6)
                n += 1
    (out_dir / f"{name}.dzi").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<Image xmlns="http://schemas.microsoft.com/deepzoom/2008" Format="webp" '
        f'Overlap="{overlap}" TileSize="{tile}">\n  <Size Width="{W}" Height="{H}"/>\n</Image>\n')
    return n


def dir_bytes(p: Path) -> int:
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file())


def build_image(item: dict, force: bool, step: str | None) -> dict:
    src = ORIG / item["source"]
    im = None

    def load():
        nonlocal im
        if im is None:
            print(f"  loading {src.name} ...")
            im = Image.open(src).convert("RGB")
        return im

    with Image.open(src) as probe_im:
        W, H = probe_im.size
    preview = OUT / f"{item['id']}_{item['preview_width']}.webp"
    if step in (None, "preview") and needs(preview, force):
        pw = item["preview_width"]
        load().resize((pw, round(H * pw / W)), Image.LANCZOS).save(
            preview, "WEBP", quality=item["preview_quality"], method=6)
        print(f"  -> {preview.name}: {mb(preview.stat().st_size)}")

    dz_dir = OUT / "deepzoom"
    dzi = dz_dir / f"{item['id']}.dzi"
    if step in (None, "tiles") and needs(dzi, force):
        dz_dir.mkdir(exist_ok=True)
        n = write_dzi(load(), dz_dir, item["id"], item["tile_size"], item["tile_overlap"], item["tile_quality"])
        print(f"  -> {n} deep-zoom tiles, {mb(dir_bytes(dz_dir / (item['id'] + '_files')))}")

    rel = RELEASE / item["release_name"]
    if step in (None, "release") and needs(rel, force):
        load().save(rel, "PNG", optimize=True)  # lossless; drops the unused alpha channel
        print(f"  -> {rel.name}: {mb(rel.stat().st_size)} (source {mb(src.stat().st_size)})")

    entry = {"kind": "image", "width": W, "height": H, "preview": preview.name,
             "dzi": f"deepzoom/{dzi.name}"}
    if preview.exists():
        entry["preview_bytes"] = preview.stat().st_size
    tiles = dz_dir / f"{item['id']}_files"
    if tiles.exists():
        entry["tiles_bytes"] = dir_bytes(tiles)
    if rel.exists():
        entry["release"] = {"file": rel.name, "bytes": rel.stat().st_size}
    return entry


# --------------------------------------------------------------------------------------
# video that is already web-ready (no trim / re-encode, no release copy)
# --------------------------------------------------------------------------------------
def build_ready(item: dict, force: bool, step: str | None) -> dict:
    src = OUT / item["file"]
    if not src.exists():
        sys.exit(f"{src} not found: put the web-ready video in content/media/")
    info = probe(src)
    poster = OUT / f"{item['id']}_poster.webp"
    if step in (None, "poster") and needs(poster, force):
        webp_from_frame(src, item.get("poster_time_s", 0), item.get("poster_width", 1280), poster,
                        quality=item.get("poster_quality", 80))
    size = src.stat().st_size
    print(f"  {src.name}: {info['width']}x{info['height']} @ {info['fps']:g} fps, "
          f"{info['duration']:.1f} s, {mb(size)}")
    # the video is both the page version ("default" rendition: played on every screen)
    # and the download (no separate release copy)
    return {"kind": "video", "width": info["width"], "height": info["height"], "fps": info["fps"],
            "duration_s": round(info["duration"], 2), "hold_end_s": 0, "poster": poster.name,
            "renditions": {"default": {"file": src.name, "bytes": size, "codec": info["codec"],
                                       "height": info["height"]}},
            "download": {"file": src.name, "bytes": size}}


# --------------------------------------------------------------------------------------
BUILDERS = {"video": build_video, "loop": build_loop, "image": build_image, "ready": build_ready}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=sorted(BUILDERS), help="build only items of this kind")
    ap.add_argument("--id", help="build only the item with this id")
    ap.add_argument("--step", help="only one step: video: poster|h264|av1|<rendition>|release; "
                                   "loop: mp4|poster|release; image: preview|tiles|release; ready: poster")
    ap.add_argument("--force", action="store_true", help="rebuild outputs that already exist")
    ap.add_argument("--list", action="store_true", help="print the manifest and exit")
    args = ap.parse_args()

    if args.list:
        print(json.dumps(load_manifest(), indent=2))
        return
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} not found on PATH")
    OUT.mkdir(parents=True, exist_ok=True)
    RELEASE.mkdir(parents=True, exist_ok=True)

    man = load_manifest()
    man.setdefault("items", {})
    for item in ITEMS:
        if (args.only and item["kind"] != args.only) or (args.id and item["id"] != args.id):
            continue
        print(f"\n== {item['id']} ({item['kind']})")
        man["items"][item["id"]] = BUILDERS[item["kind"]](item, args.force, args.step)
        save_manifest(man)  # save after every item so partial runs are kept

    print("\nWeb files in content/media/:")
    total = 0
    for f in sorted(OUT.glob("*")):
        if f.is_file() and f.suffix in (".mp4", ".webp"):
            total += f.stat().st_size
            print(f"  {f.relative_to(OUT)}: {mb(f.stat().st_size)}")
    dz = OUT / "deepzoom"
    if dz.exists():
        total += dir_bytes(dz)
        print(f"  deepzoom/ (tiles): {mb(dir_bytes(dz))}")
    print(f"  total committed media: {mb(total)}")


if __name__ == "__main__":
    main()
