"""
Text-to-Speech module using piper-tts for multilingual, offline tts.
"""

from piper import PiperVoice
from download_voice import download_voice_tts
from pathlib import Path

DEFAULT_VOICE_DIR = Path("./voices")

class TextToSpeech:
    """
    Turn text into a sound file (WAV) offline.

    This class provides an interface to use PiperVoice for multiple languages. Voices must be downloaded and kept in piper-voices/, which will happen automatically or by calling scripts/install_languages.py
    """

    def __init__(self, voice_dir: str | None = None):
        """
        Initialize the TTS engine.

        Args:
            voice_dir (str): Root directory containing Piper voice model files.
                Defaults to ~/piper-voices.
        """


if __name__ == "__main__":
    download_voice_tts("en")