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

    def record(self, duration: float) -> np.ndarray:
        """
        Record audio from the microphone for a set duration and return it as an NumPy array.

        Args:
            duration (float): Recording duration in seconds.

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
        # print(f"Audio length: {len(audio) / self.sample_rate} seconds")

        end = time.perf_counter()
        print(f"Recording took {end - start:.3f} seconds")

        return audio

    def record_and_save(self, duration: float, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Record audio from the microphone for a set duration and save it to a WAV file. Also, return it as a NumPy array.

        Args:
            duration (float): Recording duration in seconds.
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav".

        Returns:
            np.ndarray: Recorded audio samples as a NumPy array.
        """
        audio = self.record(duration)

        start = time.perf_counter()

        write(filename, self.sample_rate, self.audio)
        print(f"Audio saved to {filename}")

        end = time.perf_counter()
        print(f"Saving took {end - start:.3f} seconds")

        return audio

    def _callback(self, indata, frames, time, status): # _ at start means is internal method, don't use publicly
        """
        Call at the sample_rate of the audio stream to append indata array to the actual stream. For use in audio stream.
        """
        self.audio.append(indata.copy())
        

    def start(self) -> None:
        """
        Start recording from microphone to audio stream. For use in live processing.
        
        Intended to be used with stop() or stop_and_save().
        """
        self.audio = []
        self.stream.start()
        self.recording = True

        self.start_time = time.perf_counter()

        print("Recording...")


    def stop(self) -> np.ndarray:
        """
        Stop recording and return ndarray of audio.
        
        Intended to be used with start().
        """
        self.stream.stop()
        self.recording = False

        self.end_time = time.perf_counter()
        print(f"Recording took {self.end_time - self.start_time:.3f} seconds")

        return np.concatenate(self.audio)

    def stop_and_save(self, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Stop recording and save it to a WAV file. Also return ndarray of audio.

        Intended to be used wtih start()

        Args:
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav"
        """
        audio = self.stop()
        write(filename, self.sample_rate, audio)
        return audio
    
    def get_audio_and_save(self, filename: str = "outputs/audio.wav") -> np.ndarray:
        """
        Get current audio array since last call to get_audio or start and save it to a WAV file. Will clear audio buffer when called.

        Audio stream must be started with the start() function.

        Args:
            filename (str): Destination to save audio file. 
                Defaults to "outputs/audio.wav"
        """
        audio = np.concatenate(self.audio)
        self.audio = []
        write(filename, self.sample_rate, audio)
        return audio
    
    
    def clear_audio(self):
        """Clears the audio buffer."""
        self.audio = []