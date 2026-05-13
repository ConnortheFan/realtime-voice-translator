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

### Planned
- [ ] Real-time translation
- [ ] Text-to-speech playback
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
- pyttsx3

---

## Project Structure

```text
realtime-voice-translator/
│
├── src/
│   ├── capture/
|   |   └── recorder.py
│   ├── transcription/
|   |   └── transcriber.py
│   ├── translation/
│   ├── tts/
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
- [ ] Add translation pipeline
- [ ] Add speech playback

### Phase 3
- [ ] Improve responsiveness
- [ ] Add streaming support

### Phase 4
- [ ] Build polished UI
- [ ] Optimize performance

---

## License

This project is for educational and personal-use purposes.