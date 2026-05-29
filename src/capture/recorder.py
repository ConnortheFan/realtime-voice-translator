"""
Audio recording module using the sounddevice library.
"""

from time import perf_counter
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from log_utils import log_calls, get_logger

class Recorder:
    """
    Record audio from the system microphone.

    This class provides an interface to capture audio input from the
    microphone using the sounddevice library and returns the audio as 
    a NumPy audio array in 16 kHz mono float32 format.

    Also provides optional saving of audio in WAV format.

    For intended use in conjunction with the Transcriber module.
    """

    logger = get_logger(__name__)

    @log_calls
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        dtype=np.float32,
    ):
        """
        Initialize a Recorder for audio (microphone) input. 
        For intended use with transcriber, leave default parameters.

        Args:
            sample_rate (int): The frequency of sampling for recording.
                Defaults to 16 kHz (16,000).
            channels (int): Number of channels of audio to expect.
            Currently does not support multiple channels.
                Defaults to 1 (mono).
            dtype : Data type to store in audio array.
                Defaults to float32.
        """
        self.sample_rate = sample_rate # 16 kHz standard
        self.channels = channels # mono microphone input
        self.dtype = dtype # np.float32
        self.audio = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback
        )
        self.recording = False
        self.start_time = perf_counter()

    @log_calls
    def record(
        self,
        duration: float,
        save: bool = True,
        filename: str = "outputs/audio.wav",
    ) -> np.ndarray:
        """
        Record audio from the microphone for a set duration and return
        it as a NumPy array. Also, optionally save it to a WAV file.

        Args:
            duration (float): Recording duration in seconds.
            save (bool): Whether to save recording to files.
                Defaults to True.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav".

        Returns:
            np.ndarray: Recorded audio samples as a NumPy array.
        """
        num_samples = int(duration * self.sample_rate)

        print(f"Recording for {duration} seconds")

        audio = sd.rec(
            num_samples,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype
        )
        sd.wait()

        if save:
            write(filename, self.sample_rate, audio)
            self.logger.debug("Audio saved to %s", filename)

        return audio

    def _callback(self, indata, _frames, _time, _status):
        """
        Call at the sample_rate of the audio stream to append indata 
        array to the actual stream. For use in audio stream.
        """
        self.audio.append(indata.copy())

    def start(self) -> None:
        """
        Start recording from microphone to audio stream. For use in live processing.
        
        Intended to be used with stop(), get_audio(), or clear_audio().
        """
        self.audio = []
        self.stream.start()
        self.recording = True

        self.start_time = perf_counter()

        print("Recording...")

    def stop(self) -> None:
        """
        Stop recording.

        Intended to be used wtih start().
        """
        self.stream.stop()
        self.recording = False

    def get_audio(
        self,
        save: bool = True,
        filename: str = "outputs/audio.wav",
    ) -> np.ndarray:
        """
        Get and return current audio array. 
        Will clear audio buffer when called. 
        Also, optionally save it to a WAV file. 

        Audio stream must be started with the start() function before using this function.

        Args:
            save (bool): Whether to save recording to files.
                Defaults to True.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav".
        """
        audio = np.concatenate(self.audio)
        self.audio = []

        self.logger.debug("Recording took %.3f seconds", perf_counter() - self.start_time)
        self.start_time = perf_counter()

        if save:
            write(filename, self.sample_rate, audio)
        return audio


    def clear_audio(self) -> None:
        """Clears the audio buffer."""
        self.audio = []
        self.start_time = perf_counter()
