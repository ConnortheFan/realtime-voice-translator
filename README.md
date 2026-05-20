# Real-Time Voice Translator

A desktop application that captures live speech, translates it in real time, and plays translated audio output using AI-powered speech recognition and translation tools.

This project is being developed as both:
- a personal-use communication tool
- a portfolio project focused on real-time audio processing and AI integration

---

## Features

### Current
- [x] Microphone audio capture 
- [x] WAV export
- [x] Speech-to-text transcription
- [x] Real-time translation
- [x] Text-to-speech playback

### Planned
- [ ] Continuous streaming translation
- [ ] Reduced latency pipeline
- [ ] Multiple language support
- [ ] Voice activity detection
- [ ] Simple desktop GUI
- [ ] Bidirectional conversation mode

---

## Tech Stack

- Python
- sounddevice
- NumPy
- SciPy
- Faster-Whisper
- Argos Translate / LibreTranslate
- piper-tts

---

## Project Structure

```text
realtime-voice-translator/
│
├── scripts/
|   └── install_languages.py
|
├── src/
│   ├── capture/
|   |   └── recorder.py
│   ├── transcription/
|   |   └── transcriber.py
│   ├── translation/
|   |   └── translator.py
│   ├── tts/
|   |   ├── download_voice.py
|   |   └── tts.py
│   └── main.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Architecture

```text
Microphone Input
        ↓
Speech-to-Text
        ↓
Translation
        ↓
Text-to-Speech
        ↓
Speaker Output
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/ConnortheFan/realtime-voice-translator
cd realtime-voice-translator
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the virtual environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

#### Windows CMD

```cmd
.\.venv\Scripts\activate.bat
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

```bash
python src/main.py
```

### Note

When running this program for the first time, it will need to download the Whisper Model. After the model is downloaded, the program should then be able to be run offline.

The program will also have to download language translation pairs as well as voices for each language. This will happen at first run, but you can speed it up by running 

```bash
python scripts/install_languages.py <lang_code> <lang_code> ...
```

---

## Goals

This project is intended to help develop experience with:
- real-time systems
- audio processing
- AI model integration
- asynchronous programming
- software architecture
- low-latency pipelines

---

## Known Challenges

- Reducing translation latency
- Handling continuous speech smoothly
- Managing audio buffering
- Improving translation quality
- Avoiding overlapping speech playback

---

## Roadmap

### Phase 1
- [x] Capture microphone input
- [x] Transcribe speech locally

### Phase 2
- [x] Add translation pipeline
- [x] Add speech playback

### Phase 3
- [ ] Improve responsiveness
- [ ] Add streaming support

### Phase 4
- [ ] Build polished UI
- [ ] Optimize performance

---

## License

This project is for educational and personal-use purposes.