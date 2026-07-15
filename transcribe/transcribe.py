#!/usr/bin/env python3
"""
transcribe.py — Video/Reel → Script transcriber (100% local, free).

Give it a link (Instagram Reel, TikTok, YouTube, X, ...) or a local media file.
It downloads the audio with yt-dlp, transcribes it locally with faster-whisper,
and writes the script to a .txt file (and optionally a timestamped .srt).

No API keys. Nothing leaves your machine except the video download itself.

Usage:
    python transcribe.py "https://www.instagram.com/reel/XXXX/"
    python transcribe.py video.mp4 --language he --model small --srt
    python transcribe.py "https://youtu.be/XXXX" -o my_script.txt

See README.md for install instructions.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# ----------------------------------------------------------------------------- helpers

def _err(msg: str) -> None:
    print(f"\033[31m✗ {msg}\033[0m", file=sys.stderr)


def _info(msg: str) -> None:
    print(f"\033[36m→ {msg}\033[0m")


def _ok(msg: str) -> None:
    print(f"\033[32m✓ {msg}\033[0m")


def check_prerequisites() -> None:
    """Fail early with a friendly message if ffmpeg / deps are missing."""
    if shutil.which("ffmpeg") is None:
        _err("ffmpeg is not installed — it's required to process audio.")
        print(
            "\n  Install it:\n"
            "    macOS:   brew install ffmpeg\n"
            "    Ubuntu:  sudo apt install ffmpeg\n"
            "    Windows: winget install Gyan.FFmpeg\n",
            file=sys.stderr,
        )
        sys.exit(1)

    missing = []
    try:
        import yt_dlp  # noqa: F401
    except ImportError:
        missing.append("yt-dlp")
    try:
        import faster_whisper  # noqa: F401
    except ImportError:
        missing.append("faster-whisper")

    if missing:
        _err(f"Missing Python packages: {', '.join(missing)}")
        print(
            "\n  Install them:\n"
            "    pip install -r requirements.txt\n"
            "  (or)\n"
            f"    pip install {' '.join(missing)}\n",
            file=sys.stderr,
        )
        sys.exit(1)


def is_url(target: str) -> bool:
    return target.startswith(("http://", "https://"))


def download_audio(url: str, workdir: Path) -> Path:
    """Download the best audio track from a URL and return the file path."""
    import yt_dlp

    out_template = str(workdir / "audio.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        # Extract to a plain wav so faster-whisper reads it consistently.
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

    _info(f"Downloading audio from: {url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as exc:  # yt-dlp raises many types; surface a clean message
        _err(f"Could not download the video: {exc}")
        print(
            "\n  Tips:\n"
            "    • Private/age-restricted posts can't be fetched.\n"
            "    • Try updating yt-dlp:  pip install -U yt-dlp\n"
            "    • Or download the file manually and pass its path instead.\n",
            file=sys.stderr,
        )
        sys.exit(1)

    wavs = list(workdir.glob("audio.wav")) or list(workdir.glob("audio.*"))
    if not wavs:
        _err("Download finished but no audio file was produced.")
        sys.exit(1)
    _ok("Audio downloaded.")
    return wavs[0]


def transcribe_audio(
    audio_path: Path,
    model_size: str,
    language: str | None,
    compute_type: str,
):
    """Run faster-whisper and return (segments_list, detected_language)."""
    from faster_whisper import WhisperModel

    _info(f"Loading Whisper model '{model_size}' (first run downloads it once)...")
    # CPU + int8 is the sweet spot for local machines without a GPU.
    model = WhisperModel(model_size, device="cpu", compute_type=compute_type)

    _info("Transcribing... (this can take a while on CPU)")
    segments_gen, info = model.transcribe(
        str(audio_path),
        language=language,          # None → auto-detect
        vad_filter=True,            # skip long silences → faster + cleaner
        beam_size=5,
    )

    # segments_gen is lazy; materialize it so we can reuse it for txt + srt.
    segments = list(segments_gen)
    return segments, info.language


def write_txt(segments, out_path: Path) -> None:
    text = "\n".join(seg.text.strip() for seg in segments if seg.text.strip())
    out_path.write_text(text + "\n", encoding="utf-8")


def _fmt_ts(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, out_path: Path) -> None:
    lines = []
    for i, seg in enumerate(segments, start=1):
        lines.append(str(i))
        lines.append(f"{_fmt_ts(seg.start)} --> {_fmt_ts(seg.end)}")
        lines.append(seg.text.strip())
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe a video/reel link (or local file) into a script — fully local, free.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "target",
        help="Video URL (Instagram/TikTok/YouTube/X/...) or a path to a local media file.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output .txt path. Default: transcript next to where you ran it.",
    )
    parser.add_argument(
        "-l", "--language",
        default=None,
        help="Language code (e.g. 'he' for Hebrew, 'en'). Default: auto-detect.",
    )
    parser.add_argument(
        "-m", "--model",
        default="small",
        choices=["tiny", "base", "small", "medium", "large-v3"],
        help="Whisper model size. Bigger = more accurate but slower. Default: small. "
             "For Hebrew, 'medium' or 'large-v3' are noticeably better.",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        choices=["int8", "int8_float16", "float16", "float32"],
        help="Compute precision. Default: int8 (fastest on CPU).",
    )
    parser.add_argument(
        "--srt",
        action="store_true",
        help="Also write a timestamped .srt subtitle file.",
    )
    parser.add_argument(
        "--keep-audio",
        action="store_true",
        help="Keep the downloaded audio file instead of deleting it.",
    )
    args = parser.parse_args()

    check_prerequisites()

    # Resolve output path.
    if args.output:
        out_txt = Path(args.output).expanduser().resolve()
    else:
        out_txt = Path.cwd() / "transcript.txt"
    out_txt.parent.mkdir(parents=True, exist_ok=True)

    workdir = Path(tempfile.mkdtemp(prefix="transcribe_"))
    audio_kept_path: Path | None = None
    try:
        # 1. Get the audio.
        if is_url(args.target):
            audio_path = download_audio(args.target, workdir)
        else:
            src = Path(args.target).expanduser()
            if not src.exists():
                _err(f"File not found: {src}")
                sys.exit(1)
            audio_path = src
            _ok(f"Using local file: {src}")

        # 2. Transcribe.
        segments, detected = transcribe_audio(
            audio_path, args.model, args.language, args.compute_type
        )

        if not segments:
            _err("No speech was detected in the audio.")
            sys.exit(1)

        # 3. Write outputs.
        write_txt(segments, out_txt)
        _ok(f"Script saved to: {out_txt}   (language: {detected})")

        if args.srt:
            out_srt = out_txt.with_suffix(".srt")
            write_srt(segments, out_srt)
            _ok(f"Subtitles saved to: {out_srt}")

        if args.keep_audio and is_url(args.target):
            audio_kept_path = out_txt.with_suffix(audio_path.suffix)
            shutil.copy2(audio_path, audio_kept_path)
            _ok(f"Audio saved to: {audio_kept_path}")

        # 4. Print the script to the terminal too.
        print("\n" + "─" * 60)
        print(out_txt.read_text(encoding="utf-8").rstrip())
        print("─" * 60)

    finally:
        # Clean up temp working dir (but never a user's own local file).
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    main()
