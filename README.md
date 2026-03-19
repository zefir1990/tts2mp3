# tts2mp3

`tts2mp3` is a Python script that converts text to high-quality speech and saves it as an MP3 file using the **Coqui-TTS** engine. It supports multiple languages (including Russian and English) and voice cloning via XTTS-v2.

## Features

- **High-Quality TTS**: Uses Coqui-TTS's advanced models.
- **Multilingual**: Supports Russian, English, and 15+ other languages.
- **Voice Cloning**: Clone any voice using a 6-second reference audio clip with XTTS-v2.
- **MP3 Output**: Automatically converts synthesized audio to MP3 format.

## Prerequisites

Before running the script, you'll need:

1.  **Python >= 3.9, < 3.12** (Important: `coqui-tts` has compatibility issues with Python 3.12+)
2.  **FFmpeg**: Required by `pydub` for MP3 conversion.
    - [Download FFmpeg](https://ffmpeg.org/download.html)
    - Ensure `ffmpeg` is in your system PATH.

## Installation

1.  Clone the repository or download the script.
2.  Create and activate a virtual environment (recommended):
    ```powershell
    python -m venv tts-env
    .\tts-env\Scripts\activate
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### 🚀 Basic Usage (English)
```bash
python tts2mp3.py --text "Hello world" --output hello.mp3
```

### 🇷🇺 Russian (Standard Voice)
Uses the VITS model which does **not** require a reference voice.
```bash
python tts2mp3.py --text "Привет, это тест." --model "tts_models/ru/multi-dataset/vits" --language "ru" --output privet.mp3
```

### 👤 High-Quality Voice Cloning (XTTS-v2)
Requires a 6-second reference WAV file of the target voice.
```bash
python tts2mp3.py --text "Привет, я говорю вашим голосом." --model "tts_models/multilingual/multi-dataset/xtts_v2" --language "ru" --speaker_wav "reference.wav" --output clone.mp3
```

## All Arguments

- `--text`: Direct text to convert.
- `--file`: Path to a text file to convert.
- `--output`: Output MP3 path (default: `output.mp3`).
- `--model`: Coqui-TTS model name (default: `tts_models/en/ljspeech/glow-tts`).
- `--language`: Language code (e.g., `en`, `ru`) for multilingual models.
- `--speaker_wav`: Reference WAV for cloning (XTTS).
- `--speaker`: Speaker name for multi-speaker models.
- `--gpu`: Use GPU for faster synthesis if available.

## Troubleshooting

### 1. `ImportError: cannot import name 'BeamSearchScorer'`
This is caused by incompatible `transformers` versions. Ensure you are using `transformers==4.33.0` as specified in `requirements.txt`.

### 2. `WeightsUnpickler` Error (PyTorch 2.6+)
The script includes a monkey-patch to fix this security-related conflict in newer PyTorch versions. If it persists, try re-running the script.

### 3. "Kernel size can't be greater than actual input size"
- Ensure you are using the correct model for the language (e.g., don't use the English model for Russian text).
- Avoid very short text strings; adding a period or extra word can help.

---
*Created as part of an agentic coding task.*
