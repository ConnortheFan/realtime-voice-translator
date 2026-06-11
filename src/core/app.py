"""
Realtime Voice Translator App logic.
"""
# pylint: disable=too-few-public-methods
from capture import Recorder
from transcription import Transcriber
from translation import Translator
from tts import TextToSpeech
from log_utils import log_calls, get_logger
from .state import AppState
from .keyboard import KeyboardHandler
from .modules import Modules

class App:
    """
    Realtime Voice Translator Application using push-to-talk logic.

    Hold SPACE to talk in English. When you release the spacebar, 
    will transcribe, translate, and say the translation.

    Press ENTER to transcribe the foreign language to English. 
    Will record and consider everything said since the last input as foreign.
    """
    logger = get_logger(__name__)

    @log_calls
    def __init__(self):
        """Initialize the App states and modules"""
        self.state = AppState()
        KeyboardHandler(self.state).start()
        self.modules = Modules()
        self.logger.debug("All modules initializing, program running")

    @log_calls
    def run(self):
        """Run the App."""
        print("Press ENTER to transcribe Italian to English")
        print("Hold SPACE to talk")
        print("Press ESC to quit")

        modules = self.modules
        state = self.state

        recorder: Recorder = modules.get_module("recorder")
        recorder.start()

        print(modules.status())

        while state.running:
            # You speaking via push-to-talk SPACE bar
            if state.push_to_talk and not state.push_to_talk_processing:
                state.push_to_talk_processing = True
                print("\nRecording started")
                recorder.clear_audio()
            elif not state.push_to_talk and state.push_to_talk_processing:
                state.push_to_talk_processing = False
                print("Recording stopped")

                recording_audio = recorder.get_audio()

                transcriber: Transcriber = modules.get_module("transcriber")
                transcription = transcriber.transcribe(recording_audio, lang="en")
                print(transcription)

                translator: Translator = modules.get_module("translator")
                translation = translator.translate_ba(transcription)

                print(translation)
                print("Speaking started")

                tts_it: TextToSpeech = modules.get_module("tts_it")
                tts_it.speak(translation)

                print("Speaking stopped")
                recorder.clear_audio()

            # Someone else speaking Italian
            elif state.transcribe_to_en and not state.transcribe_to_en_processing:
                print("Transcribing to English")
                state.transcribe_to_en_processing = True
                recording_audio_en = recorder.get_audio()

                transcriber: Transcriber = modules.get_module("transcriber")
                transcription_en = transcriber.transcribe_to_en(recording_audio_en, "it")
                print(transcription_en)

                print("Speaking started")

                tts_en: TextToSpeech = modules.get_module("tts_en")
                tts_en.speak(transcription_en)
                print("Speaking stopped")
            elif state.transcribe_to_en_processing and not state.transcribe_to_en:
                state.transcribe_to_en_processing = False
                print("Done transcribing")
                recorder.clear_audio()

        recorder.stop()
        print(modules.status())
