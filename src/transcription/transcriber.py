"""
Transcription module using the faster-whisper library.
"""

from faster_whisper import WhisperModel
import numpy as np
import torch
from log_utils import get_logger, log_calls

class Transcriber:
    """
    Transcribe audio using the Whisper model.

    This class provides an interface to use the Whisper model from the 
    faster-whisper library to transcribe a NumPy audio array in 16 kHz 
    mono float32 format and returns the transcribed text.

    Also provides optional saving of transcribed text.

    For intended use with the Recorder module.
    """

    logger = get_logger(__name__)

    @log_calls
    def __init__(
        self,
        model_size: str = "base",
    ) -> None:
        """
        Initialize the Whisper model.

        Args:
            model_size (str): Which Whisper model to use - 
            "tiny", "base", "small", "medium", or "large-v3". 
            Larger models are more accurate, but slower.
                Defaults to "base" model.
        """
        if torch.cuda.is_available():
            self.model = WhisperModel(model_size, device="cuda", compute_type="float16")
            self.logger.info("Using CUDA")
        else:
            self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
            self.logger.info("Using CPU")

    @log_calls
    def transcribe(
        self,
        audio: np.ndarray,
        lang: str | None = None,
        save: bool = True,
        filename: str = "outputs/transcript.txt",
    ) -> str:
        """
        Transcribe and return a NumPy audio array to text. Also, optionally save transcribed text.

        Args:
            audio (np.ndarray): float32 array of shape (N,) or (N, 1) sampled at 16 kHz mono.
            lang (str | None): Language code (ex. "en" or "it") for transcribing. 
            Choose None to let Whisper auto-detect.
                Defaults to None.
            save (bool): Whether to save transcription to files.
                Defaults to True.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/transcript.txt".

        Returns:
            str: Transcribed string.
        """
        audio = self._prepare(audio)

        segments, _ = self.model.transcribe(
            audio,
            language=lang,
            vad_filter=True, # skip silent regions automatically
        )

        transcript = " ".join(segment.text.strip() for segment in segments)

        if save:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript)

            self.logger.debug("Transcript saved to %s", filename)

        return transcript

    @log_calls
    def transcribe_to_en(
        self,
        audio: np.ndarray,
        lang: str | None = None,
        save: bool = True,
        filename: str = "outputs/transcript_en.txt",
    ) -> str:
        """
        Transcribe and translate a NumPy audio array to English.
        Returns translated text. Also, optionally save text.

        Args:
            audio (np.ndarray): NumPy array of shape (N,) or (N, 1) sampled at 16 kHz mono.
            lang (str | None): Language code (ex. "en" or "it") for transcribing.
            Choose None to let Whisper auto-detect.
                Defaults to None.
            save (bool): Whether to save transcription to files.
                Defaults to True.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/transcript.txt".

        Returns:
            str: Transcribed string.
        """
        audio = self._prepare(audio)

        segments, _ = self.model.transcribe(
            audio,
            language=lang,
            task="translate", # automatically translate to English
            vad_filter=True, # skip silent regions automatically
        )

        transcript = " ".join(segment.text.strip() for segment in segments)

        if save:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript)
            self.logger.debug("Transcript saved to %s", filename)

        return transcript

    def _prepare(self, audio: np.ndarray) -> np.ndarray:
        """Normalize shape and dtype for Whisper model."""
        audio = np.squeeze(audio) # (N, 1) -> (N,)
        if audio.ndim != 1:
            raise ValueError(f"Expected a 1D audio array, got shape {audio.shape}")
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32)
        # Clip values to [-1, 1] in case of floating point error
        return np.clip(audio, -1.0, 1.0)
