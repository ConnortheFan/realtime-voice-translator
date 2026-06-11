"""Consolidate module into package."""

from .tts import TextToSpeech
from .download_voice import download_voice_tts

__all__ = ["TextToSpeech", "download_voice_tts"]
