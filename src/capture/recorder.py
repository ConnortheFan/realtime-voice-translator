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
        start = time.perf_counter()

        self.sample_rate = sample_rate # 16 kHz standard
        self.channels = channels # mono microphone input
        self.dtype = np.float32 
        self.audio = []
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback
        )
        self.recording = False

        end = time.perf_counter()
        print(f"\nInitializing Recorder took {end - start:.3f} seconds")

    def record(self, duration: float, save: bool = True, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Record audio from the microphone for a set duration and return it as a NumPy array. Also, optionally save it to a WAV file.

        Args:
            duration (float): Recording duration in seconds.
            save (bool): Whether to save recording to files.
                Defaults to True.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav".

        Returns:
            np.ndarray: Recorded audio samples as a NumPy array.
        """
        start = time.perf_counter()

        num_samples = int(duration * self.sample_rate)

        print(f"Recording for {duration} seconds")

        audio = sd.rec(
            num_samples,
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype
        )
        sd.wait()

        print("Done recording")
        print(f"Recording took {time.perf_counter() - start:.3f} seconds")

        if save:
            start = time.perf_counter()

            write(filename, self.sample_rate, audio)
            print(f"Audio saved to {filename}")

            print(f"Saving took {time.perf_counter() - start:.3f} seconds")

        return audio

    def _callback(self, indata, frames, time, status): # _ at start means is internal method, don't use publicly
        """
        Call at the sample_rate of the audio stream to append indata array to the actual stream. For use in audio stream.
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

        self.start_time = time.perf_counter()

        print("Recording...")

    def stop(self, save: bool = True, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Stop recording and return recording as a NumPy array. Also, optionally save it to a WAV file.

        Intended to be used wtih start().

        Args:
            save (bool): Whether to save recording to files.
                Defaults to True.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav"
        """
        self.stream.stop()
        self.recording = False

        print(f"Recording took {time.perf_counter() - self.start_time:.3f} seconds")

        audio = np.concatenate(self.audio)
        if save:
            write(filename, self.sample_rate, audio)
        return audio
    
    def get_audio(self, save: bool = True, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Get and return current audio array. Will clear audio buffer when called. Also, optionally save it to a WAV file. 

        Audio stream must be started with the start() function before using this function.

        Args:
            save (bool): Whether to save recording to files.
                Defaults to True.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav".
        """
        audio = np.concatenate(self.audio)
        self.audio = []

        print(f"Recording took {time.perf_counter() - self.start_time:.3f} seconds")
        self.start_time = time.perf_counter()

        if save:
            write(filename, self.sample_rate, audio)
        return audio
    
    
    def clear_audio(self) -> None:
        """Clears the audio buffer."""
        self.audio = []
        self.start_time = time.perf_counter()