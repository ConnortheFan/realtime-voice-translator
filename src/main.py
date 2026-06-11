"""
Main module to run entire program. Run:

python src/main.py

to start.
"""
from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
from log_utils import setup_logging, log_calls, get_logger
from core import AppState, KeyboardHandler, Modules

@log_calls
def main():
    """
    Main function to run entire program. Run:

    python src/main.py

    to start.
    """
    setup_logging(debug = True)

    logger = get_logger(__name__)

    state = AppState()
    KeyboardHandler(state).start()
    modules = Modules()

    logger.debug("All modules initialized, program running")
    print("Press ENTER to transcribe Italian to English")
    print("Hold SPACE to talk")
    print("Press ESC to quit")

    recorder = modules.get_module("recorder")
    recorder.start()

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

            translator = modules.get_module("translator")
            translation = translator.translate_ba(transcription)

            print(translation)
            print("Speaking started")

            tts_it = modules.get_module("tts_it")
            tts_it.speak(translation)

            print("Speaking stopped")
            recorder.clear_audio()

        # Someone else speaking Italian
        elif state.transcribe_to_en and not state.transcribe_to_en_processing:
            print("Transcribing to English")
            state.transcribe_to_en_processing = True
            recording_audio_en = recorder.get_audio()

            transcriber = modules.get_module("transcriber")
            transcription_en = transcriber.transcribe_to_en(recording_audio_en, "it")
            print(transcription_en)

            print("Speaking started")

            tts_en = modules.get_module("tts_en")
            tts_en.speak(transcription_en)
            print("Speaking stopped")
        elif state.transcribe_to_en_processing and not state.transcribe_to_en:
            state.transcribe_to_en_processing = False
            print("Done transcribing")
            recorder.clear_audio()

    recorder.stop()

if __name__ == "__main__":
    main()
