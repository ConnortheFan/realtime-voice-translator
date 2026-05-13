"""
Audio recording module.
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

class Recorder:
    """
    Record audio from the system microphone.

    This class provides an interface to capture audio input using the sounddevice library.
    """

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        """Create a Recorder with default values"""
        self.sample_rate = sample_rate # 16kHz standard
        self.channels = channels # Microphone input
        self.audio = []
        self.stream = None
        self.recording = False

    def record(self, duration: float) -> np.ndarray:
        """
        Record audio from the microphone and return it as an NumPy array.

        Args:
            duration (float): Recording duration in seconds.

        Returns:
            np.ndarray: Recorded audio samples as a NumPy array.
        """
        num_samples = int(duration * self.sample_rate)

        start = time.perf_counter()

        print(f"Recording for {duration} seconds")

        self.audio = sd.rec(
            num_samples,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.float32
        )
        sd.wait()

        end = time.perf_counter()

        print("Done recording")
        print(f"Took {end - start} seconds")
        print(f"Audio length: {len(self.audio) / self.sample_rate} seconds")
        return self.audio

    def record_and_save(self, duration: float, filename: str = "audio.wav") -> np.ndarray:
        """
        Record audio from the microphone and save it to a WAV file. Also, return it as a NumPy array.

        Args:
            duration (float): Recording duration in seconds.
            filename (str): Filename to save audio file. 
                Defaults to "audio.wav"

        Returns:
            np.ndarray: Recorded audio samples as a NumPy array.
        """

        audio = self.record(duration)
        write(filename, self.sample_rate, self.audio)
        print(f"Audio saved to {filename}")
        return audio

    def _callback(self, indata, frames, time, status): # _ at start means is internal method, don't use publicly
        """
        Call at the sample_rate of the audio stream to append indata array to the actual stream. For use in audio stream in later implementation.
        """
        pass

    def start(self) -> None:
        """
        Start recording from microphone to audio stream.
        
        Intended to be used with stop() or stop_and_save().
        """
        pass

    def stop(self) -> np.ndarray:
        """
        Stop recording and return ndarray of audio.
        
        Intended to be used with start().
        """
        return np.ndarray(0)

    def stop_and_save(self, filename: str = "audio.wav") -> np.ndarray:
        """
        Stop recording and save it to a WAV file. Also return ndarray of audio.

        Intended to be used wtih start()

        Args:
            filename (str): Filename to save audio file. 
                Defaults to "audio.wav"
        """

        audio = self.stop()
        write(filename, self.sample_rate, audio)
        return audio
    