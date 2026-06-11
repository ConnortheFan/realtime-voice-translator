"""
Module for controlling shared modules throughout entire pipeline.
"""

from concurrent.futures import ThreadPoolExecutor

from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
from log_utils import log_calls, get_logger

class Modules:
    """
    Container to initialize and store modules for instantaneous startup.
    """
    logger = get_logger(__name__)

    def __init__(self):
        self.cache = {}
        self.cache["recorder"] = Recorder()

        self.ex = ThreadPoolExecutor(max_workers=4)
        self.futures = {
            "transcriber": self.ex.submit(Transcriber),
            "translator": self.ex.submit(Translator, "it", "en"),
            "tts_it": self.ex.submit(TextToSpeech, "it"),
            "tts_en": self.ex.submit(TextToSpeech, "en"),
        }

    @log_calls
    def get_module(self, module: str):
        """
        Retrieves a module from initialization. If the module has 
        already been retrieved before, stores it in cache for instantaneous retrieval.

        Args:
            module (str): Name of module.
                Will raise a ValueError if module not found.
        """
        if module not in self.futures and module not in self.cache:
            raise ValueError(f"Module {module} not found")

        if module not in self.cache:
            self.cache[module] = self.futures.pop(module).result()

        return self.cache[module]

    def status(self) -> dict[str, str]:
        """
        Returns initialization state of all modules.
        """
        return {
            name: (
                "ready" if name in self.cache
                else "initialized" if self.futures[name].done()
                else "pending" if name in self.futures
                else "unknown"
            )
            for name in self.futures.keys() | self.cache.keys()
        }
