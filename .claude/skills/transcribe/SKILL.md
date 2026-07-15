---
name: transcribe
description: Transcribe a video or reel into a text script, fully locally and free. Use when the user gives a video link (Instagram Reel, TikTok, YouTube, X/Twitter, ...) or a local media file and wants the spoken words / script / captions extracted — phrasings like "transcribe this", "get the script", "תמלל לי", "תעתיק את התסריט". Wraps the transcribe/ CLI (yt-dlp + faster-whisper). No API key.
---

# Transcribe a video into a script

This skill turns a video link or local media file into a text script, running
**entirely locally** with `yt-dlp` + `faster-whisper` — no API key, nothing sent
to the cloud except the video download itself. It wraps the CLI in
[`transcribe/transcribe.py`](../../../transcribe/transcribe.py).

## When to use

Trigger when the user provides a video link (Instagram/TikTok/YouTube/X/…) or a
local media file and wants the spoken content extracted — e.g. "transcribe this
reel", "get me the script", "תמלל לי את הסרטון", "תעתיק את התסריט".

## Steps

1. **Get the target.** Take the URL or file path from the user's message. If they
   referred to a video without giving a link (e.g. "the reel I sent"), ask for the
   URL or file path.

2. **Check prerequisites once.** The tool needs `ffmpeg` on PATH plus the Python
   deps. If you're unsure they're installed, run:
   ```bash
   cd transcribe && pip install -r requirements.txt
   ```
   `ffmpeg` is a system package, not pip — if it's missing the script prints the
   exact install command (`brew install ffmpeg` / `sudo apt install ffmpeg` /
   `winget install Gyan.FFmpeg`). Relay that to the user; don't try to work around it.

3. **Pick the model and language.**
   - **Language:** if the user tells you the language (or it's obvious from their
     request, e.g. a Hebrew request), pass `--language` with the ISO code
     (`he`, `en`, …). Otherwise omit it and let Whisper auto-detect.
   - **Model:** default to `--model small`. For **Hebrew** or when accuracy matters,
     use `--model medium` (or `large-v3` for critical work). Warn the user that
     bigger models are slower on CPU.

4. **Run the tool** from the repo's `transcribe/` directory:
   ```bash
   cd transcribe
   python transcribe.py "<URL_OR_PATH>" --language <code> --model <size>
   ```
   Add `--srt` if the user wants timestamped subtitles, `-o <path>` to control where
   the transcript is saved (default `transcript.txt`), and `--keep-audio` to retain
   the downloaded audio.

5. **Return the script.** The tool prints the transcript to stdout and saves it to a
   file. Show the transcript to the user and tell them the file path. If they want
   it cleaned up (punctuation, paragraphs, speaker labels) or translated, offer to
   do that as a follow-up.

## Failure handling

- **Download fails** → the post is likely private/age-restricted, or `yt-dlp` is out
  of date. Suggest `pip install -U yt-dlp`, or ask the user to download the file
  manually and pass its local path instead.
- **No speech detected** → the clip may have no spoken audio (music only) or be too
  quiet. Confirm with the user.
- **Slow on CPU** → suggest a smaller model, or a GPU with `--compute-type float16`.

## Notes

- Only **public** posts can be downloaded — private/restricted content can't be fetched.
- Full option reference lives in [`transcribe/README.md`](../../../transcribe/README.md).
