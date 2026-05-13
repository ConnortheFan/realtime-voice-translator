"""
Transcription module using the faster-whisper library.
"""

from faster_whisper import WhisperModel
import numpy as np
import time

class Transcriber:
    """
    Transcribe audio using the Whisper model.

    This class provides an interface to use the Whisper model from the faster-whisper library to transcribe a NumPy audio array in 16 kHz mono float32 format and returns the transcribed text.

    Also provides optional saving of transcribed text.

    For intended use with the Recorder module.
    """

    def __init__(
        self,
        model_size: str = "base",
        cuda: bool = False,
        language: str | None = None
    ) -> None:
        """
        Initialize the Whisper model.

        Args:
            model_size (str): Which Whisper model to use - "tiny", "base", "small", "medium", or "large-v3". Larger models are more accurate, but slower.
                Defaults to "base" model.
            cuda (bool): If CUDA GPU is available. Otherwise, will use CPU.
                Defaults to False.
            language (str | None): Language code (ex. "en" or "it"). Choose None to let Whisper auto-detect.
                Defaults to None.
        """
        start = time.perf_counter()

        self.language = language
        device = "cpu"
        compute_type = "int8" # int8 is fastest on CPU
        if cuda:
            device = "cuda"
            compute_type = "float16" # float16 is best on GPU

        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

        end = time.perf_counter()
        print(f"\nInitializing Whisper model took {end - start:.3f} seconds")

    def transcribe(self, audio: np.ndarray) -> str:
        """
        Transcribe a NumPy audio array to text.

        Args:
            audio (np.ndarray): NumPy array of shape (N,) or (N, 1) sampled at 16 kHz mono.

        Returns:
            str: Transcribed string.
        """
        start = time.perf_counter()

        audio = self._prepare(audio)

        segments, _ = self.model.transcribe(
            audio,
            language=self.language,
            vad_filter=True, # skip silent regions automatically
        )

        transcript = " ".join(segment.text.strip() for segment in segments)

        end = time.perf_counter()
        print(f"Transcribing took {end - start:.3f} seconds")

        return transcript
    
    def transcribe_and_save(self, audio: np.ndarray, filename: str = "outputs/transcript.txt") -> str:
        """
        Transcribe a NumPy audio array to text. Also, save transcribed text to filename.

        Args:
            audio (np.ndarray): float32 array of shape (N,) or (N, 1) sampled at 16 kHz mono.
            filename (str): Destination to save transcribed text.
                Defaults to "outputs/transcript.txt".

        Returns:
            str: Transcribed string.
        """
        transcript = self.transcribe(audio)

        start = time.perf_counter()

        with open(filename, "w") as f:
            f.write(transcript)
        
        print(f"Transcript saved to {filename}")

        end = time.perf_counter()
        print(f"Saving took {end - start:.3f} seconds")

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