"""
Text-to-Speech module using piper-tts for multilingual, offline tts.
"""

from time import perf_counter
from pathlib import Path
import wave

import sounddevice as sd
from piper import PiperVoice
import numpy as np

from log_utils import get_logger, log_calls
from .download_voice import download_voice_tts


DEFAULT_VOICE_DIR = Path("./voices")

def _find_voice_path(lang: str) -> Path | None:
    """
    Find the path of the first .onnx model in DEFAULT_VOICE_DIR
    whose name starts with the given language code.

    Args:
        lang (str): ISO 639 language code
    
    Returns:
        Path | None: Path to the .onnx model file.
        If no .onnx model file is found, will return None.
    """
    voice_path = next(DEFAULT_VOICE_DIR.glob(f"{lang}*.onnx"), None)

    return voice_path

# pylint: disable=too-few-public-methods
class TextToSpeech:
    """
    Turn text into a sound file (WAV) offline.

    This class provides an interface to use PiperVoice for 2 languages.
    Voices must be downloaded and kept in voices/, which will happen
    automatically or by calling scripts/install_languages.py
    """

    logger = get_logger(__name__)

    @log_calls
    def __init__(self, lang: str, auto_download: bool = True):
        """
        Initialize the TTS engine.

        Args:
            lang (str): The language to speak. 
            Use ISO 639 codes to determine the language (e.g. en, it, es, fr).
            auto_download (bool): Whether to automatically download the voice files for languages.
                Defaults to True.
        """
        self.lang = lang
        voice_path = _find_voice_path(lang)

        if auto_download and voice_path is None:
            download_voice_tts(lang)
            voice_path = _find_voice_path(lang)

        if voice_path is None:
            raise ValueError("Voice Path not found")
        self.voice = PiperVoice.load(voice_path)

    def speak(self, text: str, filename: str = "outputs/tts_output.wav") -> None:
        """
        Synthesize the given text into audio and play it through the system's audio output. 
        Also, will save audio output to files as a WAV file. 
        
        Will hold program until speaking is done.

        Args:
            text (str): Text to speak.
            filename (str): Destination to save output audio.
                Defaults to "outputs/tts_output.wav".
        """
        start = perf_counter()

        wav_path = filename

        wav_file = wave.Wave_write(wav_path)
        self.voice.synthesize_wav(text, wav_file)

        wav_file = wave.Wave_read(wav_path)
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

        self.logger.debug("Transforming Text-to-Speech took %.3f seconds", perf_counter() - start)

        start = perf_counter()

        sd.play(audio, sample_rate)
        sd.wait()

        self.logger.debug("Playing audio took %.3f seconds", perf_counter() - start)


if __name__ == "__main__":
    tts_en = TextToSpeech("en")
    tts_en.speak("Hello, this is a test to see if your audio is working.")

    tts_it = TextToSpeech("it")
    tts_it.speak("Ciao bello. Io sono stanco e voglio dormire.")
