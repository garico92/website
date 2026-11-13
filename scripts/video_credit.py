#!/usr/bin/env python3
"""
video_credit.py - burn a small "Credits: Giovanni Aricò" into the last second of a video.

Only the end of the video is re-encoded: everything before the last keyframe that precedes
the credit is stream-copied, so the rest of the film stays bit-identical (no quality loss,
same size). The tail is re-encoded with the same x264 preset / rate control as the source,
so that the two parts share the same H.264 headers and can be joined without a re-encode.
If the headers do not match, the whole video is re-encoded instead (and this is reported).

Used by scripts/make_web_media.py; can also be run by hand:

    python scripts/video_credit.py in.mp4 out.mp4 [--text "..."] [--seconds 1]
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

CREDIT = "Credits: Giovanni Aricò"
SECONDS = 1.0                      # how long the credit is shown, at the very end
FONT_CANDIDATES = [                # first one that exists is used
    "/Library/Fonts/Inter-Medium.otf",
    "~/Library/Fonts/Inter-Medium.otf",
    "/usr/share/fonts/opentype/inter/Inter-Medium.otf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _run(cmd, capture=False):
    res = subprocess.run([str(c) for c in cmd], check=True, text=True,
                         stdout=subprocess.PIPE if capture else None,
                         stderr=subprocess.PIPE if capture else None)
    return res.stdout if capture else ""


def font_file() -> str:
    for f in FONT_CANDIDATES:
        p = Path(f).expanduser()
        if p.exists():
            return str(p)
    raise FileNotFoundError("no font found for the credit; add one to FONT_CANDIDATES")


def credit_start(path: Path, seconds: float = SECONDS) -> tuple[float, float]:
    """(start time, fade-in) for a credit shown during the last `seconds` of the file.
    With a variable frame rate (e.g. a converted GIF) the last frame can stay on screen for
    longer than `seconds`: the credit then starts on that frame, without fade."""
    d = json.loads(_run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                         "packet=pts_time:format=duration", "-of", "json", path], capture=True))
    D = float(d["format"]["duration"])
    last = max(float(p["pts_time"]) for p in d["packets"] if "pts_time" in p)
    start = D - seconds
    if last <= start + 0.25:
        return last, 0.0
    return start, 0.25


def drawtext(height: int, start: float, text: str = CREDIT, fade: float = 0.25) -> str:
    """ffmpeg drawtext filter: small white text with a soft dark box, bottom-right corner,
    visible (with a short fade-in) from `start` seconds to the end of the stream."""
    size = max(14, round(height * 0.026))
    margin = round(height * 0.03)
    pad = max(4, round(size * 0.35))
    esc = text.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’")
    alpha = (f"min(1\\,(t-{start:.4f})/{fade})" if fade > 0 else "1")
    return (f"drawtext=fontfile='{font_file()}':text='{esc}':fontsize={size}:fontcolor=white"
            f":box=1:boxcolor=black@0.45:boxborderw={pad}"
            f":x=w-tw-{margin + pad}:y=h-th-{margin + pad}"
            f":alpha='{alpha}':enable='gte(t\\,{start - 1e-3:.4f})'")


def probe(path: Path) -> dict:
    d = json.loads(_run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                         "stream=width,height,r_frame_rate,nb_frames,pix_fmt,level:format=duration",
                         "-of", "json", path], capture=True))
    s = d["streams"][0]
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    return {"width": s["width"], "height": s["height"], "fps": num / den, "level": s.get("level"),
            "nb_frames": int(s.get("nb_frames") or 0), "duration": float(d["format"]["duration"])}


def keyframes(path: Path) -> list[float]:
    out = _run(["ffprobe", "-v", "error", "-skip_frame", "nokey", "-select_streams", "v:0",
                "-show_entries", "frame=pts_time", "-of", "csv=p=0", path], capture=True)
    return [float(x.strip().rstrip(",")) for x in out.split() if x.strip().rstrip(",")]


def x264_options(path: Path) -> dict:
    """The x264 settings stored by the encoder in the stream (SEI user data)."""
    m = re.search(rb"options: ([^\x00]*)", path.read_bytes()[:4_000_000])
    if not m:
        return {}
    return dict(kv.split("=", 1) for kv in m.group(1).decode(errors="ignore").split() if "=" in kv)


def x264_args(opt: dict, level) -> list[str]:
    """Encoder arguments that reproduce the source settings (and therefore its SPS/PPS)."""
    # presets as written by x264 into its options string
    subme, ref, bf = int(opt.get("subme", 7)), int(opt.get("ref", 3)), int(opt.get("bframes", 3))
    if subme >= 10:
        preset = "veryslow"
    elif subme >= 9:
        preset = "slower"
    elif subme == 8:
        preset = "slow"
    elif subme == 7:
        preset = "medium"
    elif subme == 6:
        preset = "fast"
    elif subme == 4:
        preset = "faster"
    elif subme == 2:
        preset = "veryfast"
    elif subme == 1:
        preset = "superfast"
    else:
        preset = "medium"
    args = ["-c:v", "libx264", "-preset", preset]
    if opt.get("psy_rd", "").startswith("0.40") and opt.get("deblock") == "1:1:1":
        args += ["-tune", "animation"]
    params = [f"ref={ref}", f"bframes={bf}", f"keyint={opt.get('keyint', 250)}",
              f"min-keyint={opt.get('keyint_min', 25)}"]
    if opt.get("rc") == "crf":
        args += ["-crf", opt.get("crf", "20")]
    else:  # 2pass / abr: single-pass ABR with the same bitrate and VBV on the short tail
        args += ["-b:v", f"{opt.get('bitrate', '4000')}k"]
        if "vbv_maxrate" in opt:
            args += ["-maxrate", f"{opt['vbv_maxrate']}k", "-bufsize", f"{opt['vbv_bufsize']}k"]
    if level:
        args += ["-level:v", f"{int(level) / 10:.1f}"]
    return args + ["-x264-params", ":".join(params), "-pix_fmt", "yuv420p", "-profile:v", "high",
                   "-tag:v", "avc1"]


def avcc(path: Path) -> bytes:
    """The H.264 decoder configuration (SPS/PPS) of an MP4 file."""
    data = path.read_bytes()
    i = data.find(b"avcC")
    if i < 0:
        return b""
    size = int.from_bytes(data[i - 4:i], "big")
    return data[i + 4:i - 4 + size]


def frames_before(path: Path, t: float) -> int:
    """Number of frames shown before time t (works for variable frame rate too)."""
    out = _run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                "packet=pts_time", "-of", "csv=p=0", path], capture=True)
    return sum(1 for x in out.split() if x.strip(",") and float(x.strip(",")) < t - 1e-4)


def frame_count(path: Path) -> int:
    out = _run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0",
                "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path], capture=True)
    return int(out.strip().rstrip(","))


TAIL_QP = 16   # quality of a re-encoded two-pass tail (lower = better; it is only a few seconds)


def tail_args(enc: list, crf: int) -> list:
    """Same encoder arguments, but CRF `crf` (for the headers) and constant QP TAIL_QP (zone)."""
    out, i = [], 0
    while i < len(enc):
        if enc[i] in ("-b:v", "-maxrate", "-bufsize", "-crf"):
            i += 2
            continue
        out.append(enc[i])
        i += 1
    j = out.index("-x264-params") + 1
    out[j] += f":zones=0,1000000,q={TAIL_QP}"
    return out + ["-crf", str(crf)]


def matching_crf(src: Path, K: float, enc: list, head: Path, tmp: Path) -> int | None:
    want = avcc(head)
    for crf in range(51, -1, -1):
        probe_out = tmp / "pps.mp4"
        _run(["ffmpeg", "-y", "-v", "error", "-ss", f"{K:.6f}", "-i", src, "-map", "0:v:0",
              "-frames:v", "1", *tail_args(enc, crf), "-an", probe_out])
        if avcc(probe_out) == want:
            return crf
    return None


def encode(inp: list, vf: str, enc: list, two_pass: bool, out: Path, tmp: Path) -> None:
    common = ["ffmpeg", "-y", "-v", "error", *inp, "-map", "0:v:0", "-vf", vf, *enc, "-an",
              "-fps_mode", "passthrough"]   # keep the source timestamps (also for variable frame rate)
    if two_pass:  # as the source: also gives the same picture parameter set
        log = tmp / "pass"
        _run([*common, "-pass", "1", "-passlogfile", log, "-f", "mp4", "/dev/null"])
        _run([*common, "-pass", "2", "-passlogfile", log, "-movflags", "+faststart", out])
    else:
        _run([*common, "-movflags", "+faststart", out])


def add_credit(src: Path, dst: Path, text: str = CREDIT, seconds: float = SECONDS,
               verbose: bool = True) -> str:
    """Write `src` with the credit burnt into its last `seconds` to `dst`.
    Returns "tail" (only the end re-encoded) or "full" (whole video re-encoded)."""
    src, dst = Path(src), Path(dst)
    info = probe(src)
    D, fps, H = info["duration"], info["fps"], info["height"]
    start, fade = credit_start(src, seconds)
    opt = x264_options(src)
    enc = x264_args(opt, info["level"])
    log = print if verbose else (lambda *a, **k: None)

    tmp = Path(tempfile.mkdtemp(prefix="credit_"))
    try:
        keys = [k for k in keyframes(src) if k <= start + 1e-6]
        K = max(keys) if keys else 0.0
        if K > 0:
            n_head = frames_before(src, K)
            head, tail = tmp / "head.mp4", tmp / "tail.mp4"
            _run(["ffmpeg", "-y", "-v", "error", "-i", src, "-map", "0:v:0", "-c", "copy",
                  "-frames:v", n_head, head])
            encode(["-ss", f"{K:.6f}", "-i", src], drawtext(H, start - K, text, fade), enc,
                   opt.get("rc") == "2pass", tail, tmp)
            if avcc(head) != avcc(tail) and opt.get("rc") != "crf":
                # Two-pass sources store a picture-parameter set that a new short encode does
                # not reproduce. A CRF encode writes its CRF value there instead: find the CRF
                # that gives the same headers, and set the real quality with a zone (q=TAIL_QP).
                crf = matching_crf(src, K, enc, head, tmp)
                if crf is not None:
                    enc2 = tail_args(enc, crf)
                    encode(["-ss", f"{K:.6f}", "-i", src], drawtext(H, start - K, text, fade), enc2,
                           False, tail, tmp)
            if avcc(head) == avcc(tail) and frame_count(head) == n_head:
                lst = tmp / "list.txt"
                lst.write_text(f"file '{head}'\nfile '{tail}'\n")
                _run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                      "-c", "copy", "-movflags", "+faststart", dst])
                if frame_count(dst) == info["nb_frames"] or not info["nb_frames"]:
                    log(f"  credit: re-encoded only the last {D - K:.2f} s of {D:.2f} s")
                    return "tail"
            log("  credit: H.264 headers differ, re-encoding the whole video")
        encode(["-i", src], drawtext(H, start, text, fade), enc, opt.get("rc") == "2pass", dst, tmp)
        return "full"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("dst", type=Path)
    ap.add_argument("--text", default=CREDIT)
    ap.add_argument("--seconds", type=float, default=SECONDS)
    a = ap.parse_args()
    print(add_credit(a.src, a.dst, a.text, a.seconds))
