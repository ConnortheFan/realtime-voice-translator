"""
Audio recording module using the sounddevice library.
"""

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import time

class Recorder:
    """
    Record audio from the system microphone.

    This class provides an interface to capture audio input from the microphone using the sounddevice library and returns the audio as a NumPy audio array in 16 kHz mono float32 format.

    Also provides optional saving of audio in WAV format.

    For intended use in conjunction with the Transcriber module.
    """

    def __init__(self, sample_rate: int = 16000, channels: int = 1, dtype=np.float32):
        """
        Initialize a Recorder for audio (microphone) input. For intended use with transcriber, leave default parameters.

        Args:
            sample_rate (int): The frequency of sampling for recording.
                Defaults to 16 kHz (16,000).
            channels (int): Number of channels of audio to expect. Currently does not support multiple channels.
                Defaults to 1 (mono).
            dtype : Data type to store in audio array.
                Defaults to float32.
        """
        self.sample_rate = sample_rate # 16 kHz standard
        self.channels = channels # mono microphone input
        self.dtype = np.float32 
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
            dtype=self.dtype
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
            filename (str): Destination to save audio file. 
                Defaults to "audio.wav".

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
            filename (str): Destination to save audio file. 
                Defaults to "audio.wav"
        """
        audio = self.stop()
        write(filename, self.sample_rate, audio)
        return audio
    