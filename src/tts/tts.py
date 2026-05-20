"""
Text-to-Speech module using piper-tts for multilingual, offline tts.
"""

from piper import PiperVoice
from .download_voice import download_voice_tts
from pathlib import Path
import sounddevice as sd
import wave
import numpy as np
import time

DEFAULT_VOICE_DIR = Path("./voices")

def _find_voice_path(lang: str) -> Path | None:
    """
    Find the path of the first .onnx model in DEFAULT_VOICE_DIR whose name starts with the given language code.

    Args:
        lang (str): ISO 639 language code
    
    Returns:
        Path | None: Path to the .onnx model file. If no .onnx model file is found, will return None.
    """
    voice_path = next(DEFAULT_VOICE_DIR.glob(f"{lang}*.onnx"), None)

    return voice_path


class TextToSpeech:
    """
    Turn text into a sound file (WAV) offline.

    This class provides an interface to use PiperVoice for 2 languages. Voices must be downloaded and kept in voices/, which will happen automatically or by calling scripts/install_languages.py
    """

    def __init__(self, lang: str, auto_download: bool = True):
        """
        Initialize the TTS engine.

        Args:
            lang (str): The language to speak. Use ISO 639 codes to determine the language (e.g. en, it, es, fr).
            auto_download (bool): Whether to automatically download the voice files for languages.
                Defaults to True.
        """
        start = time.perf_counter()

        self.lang = lang
        voice_path = _find_voice_path(lang)

        if auto_download and voice_path is None:
            download_voice_tts(lang)
            voice_path = _find_voice_path(lang)
    
        if voice_path is None:
            raise ValueError("Voice Path not found")
        self.voice = PiperVoice.load(voice_path)

        end = time.perf_counter()
        print(f"\nInitializing TTS took {end - start:.3f} seconds")

    def speak_and_save(self, text: str, filename: str = "outputs/tts_output.wav"):
        """
        Synthesize the given text into audio and play it through the system's audio output.
        """
        start = time.perf_counter()

        wav_path = filename

        wav_file = wave.Wave_write(wav_path)
        self.voice.synthesize_wav(text, wav_file)

        wav_file = wave.Wave_read(wav_path)
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        channels = wav_file.getnchannels()

        audio = np.frombuffer(frames, dtype=np.int16)

        end = time.perf_counter()
        print(f"Doing Text-to-Speech took {end - start:.3f} seconds")

        start = time.perf_counter()

        print("Playing audio")
        sd.play(audio, sample_rate)
        sd.wait()
        print("Finished playing")

        end = time.perf_counter()
        print(f"Playing audio took {end - start:.3f} seconds")

        

if __name__ == "__main__":
    tts_en = TextToSpeech("en")
    tts_en.speak_and_save("Hello, this is a test to see if your audio is working.")

    tts_it = TextToSpeech("it")
    tts_it.speak_and_save("Ciao bello. Io sono stanco e voglio dormire.")