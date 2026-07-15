# 🎙️ Transcribe — סרטון → סקריפט (מקומי, חינם)

כלי שורת פקודה שלוקח **לינק לסרטון** (Reel של אינסטגרם, טיקטוק, יוטיוב, X ועוד) —
מוריד את האודיו, מתמלל אותו **מקומית על המחשב שלך** עם Whisper, ומחזיר לך את הסקריפט
כקובץ טקסט (ואופציונלית גם כתוביות עם חותמות זמן).

✅ בלי מפתח API · ✅ בלי תשלום · ✅ שום דבר לא נשלח לענן (חוץ מהורדת הסרטון עצמו)

---

## התקנה (פעם אחת)

### 1. התקיני ffmpeg
זה הכלי שמעבד את האודיו:

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# Windows
winget install Gyan.FFmpeg
```

### 2. התקיני את חבילות ה-Python

```bash
cd transcribe
pip install -r requirements.txt
```

זהו. בפעם הראשונה שתריצי תמלול, המודל של Whisper יורד אוטומטית (פעם אחת).

---

## שימוש

### הכי בסיסי — לינק לרילס:
```bash
python transcribe.py "https://www.instagram.com/reel/XXXX/"
```

הסקריפט יודפס למסך ויישמר לקובץ `transcript.txt`.

### עברית + מודל מדויק יותר:
```bash
python transcribe.py "https://www.instagram.com/reel/XXXX/" --language he --model medium
```

### קובץ מקומי שכבר הורדת:
```bash
python transcribe.py video.mp4 --language he
```

### עם כתוביות מתוזמנות (.srt):
```bash
python transcribe.py "https://youtu.be/XXXX" --srt
```

### לשמור למקום ספציפי:
```bash
python transcribe.py "https://..." -o ~/Desktop/my_script.txt
```

---

## כל האפשרויות

| דגל | מה זה עושה | ברירת מחדל |
|------|-----------|------------|
| `target` | הלינק לסרטון או נתיב לקובץ מקומי (**חובה**) | — |
| `-o, --output` | לאן לשמור את קובץ הטקסט | `transcript.txt` |
| `-l, --language` | קוד שפה, למשל `he` לעברית או `en` לאנגלית | זיהוי אוטומטי |
| `-m, --model` | גודל המודל: `tiny` / `base` / `small` / `medium` / `large-v3` | `small` |
| `--compute-type` | דיוק חישוב: `int8` (הכי מהיר) עד `float32` | `int8` |
| `--srt` | לייצר גם קובץ כתוביות מתוזמן | כבוי |
| `--keep-audio` | לשמור את קובץ האודיו שהורד | כבוי |

---

## איזה מודל לבחור?

| מודל | דיוק | מהירות (CPU) | מתי להשתמש |
|------|------|--------------|------------|
| `tiny` | נמוך | הכי מהיר | בדיקה מהירה בלבד |
| `small` | טוב | מהיר | ברירת מחדל, טוב לרוב המקרים |
| `medium` | מצוין | בינוני | **מומלץ לעברית** — איזון טוב |
| `large-v3` | הכי טוב | איטי | תמלול קריטי, כשהדיוק חשוב מהכל |

> 💡 **לעברית** מומלץ `medium` ומעלה — המודלים הקטנים פחות מדייקים בעברית.
> אם יש לך GPU של Nvidia, אפשר להאיץ משמעותית עם `--compute-type float16`.

---

## פתרון תקלות

| בעיה | פתרון |
|------|-------|
| `ffmpeg is not installed` | התקיני ffmpeg (ראי סעיף ההתקנה למעלה) |
| `Could not download the video` | הסרטון פרטי/מוגבל, או ש-yt-dlp צריך עדכון: `pip install -U yt-dlp` |
| התמלול איטי מאוד | השתמשי במודל קטן יותר (`--model small`) או הוסיפי GPU |
| התמלול לא מדויק בעברית | עברי למודל `medium` או `large-v3`, והוסיפי `--language he` |
| `No speech was detected` | ייתכן שהסרטון בלי דיבור, או שהאודיו שקט מדי |

---

## איך זה עובד מאחורי הקלעים

```
לינק → yt-dlp מוריד אודיו → ffmpeg ממיר ל-WAV → faster-whisper מתמלל → קובץ טקסט
```

הכל רץ מקומית. `faster-whisper` היא גרסה מהירה ויעילה של מודל Whisper של OpenAI,
שרצה מצוין גם על מעבד רגיל בלי כרטיס מסך.
