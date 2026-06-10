"""
Main module to run entire program. Run:

python src/main.py

to start.
"""

from concurrent.futures import ThreadPoolExecutor

from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
from log_utils import setup_logging, log_calls, get_logger
from core import AppState, KeyboardHandler

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
    recorder = Recorder()

    with ThreadPoolExecutor(max_workers=4) as ex:
        futures = {
            "transcriber": ex.submit(Transcriber),
            "translator": ex.submit(Translator, "it", "en"),
            "tts_it": ex.submit(TextToSpeech, "it"),
            "tts_en": ex.submit(TextToSpeech, "en"),
        }

        transcriber = futures['transcriber'].result()
        translator = futures['translator'].result()
        tts_it = futures['tts_it'].result()
        tts_en = futures['tts_en'].result()

    logger.debug("All modules initialized, program running")
    print("Press ENTER to transcribe Italian to English")
    print("Hold SPACE to talk")
    print("Press ESC to quit")

    started = False
    transcribing = False

    recorder.start()

    while state.running:
        # You speaking via push-to-talk SPACE bar
        if state.recording and not started:
            started = True
            print("\nRecording started")
            recorder.clear_audio()
        elif not state.recording and started:
            started = False
            print("Recording stopped")

            recording_audio = recorder.get_audio()
            transcription = transcriber.transcribe(recording_audio)
            translation = translator.translate_ba(transcription)
            print(translation)
            print("Speaking started")
            tts_it.speak(translation)
            print("Speaking stopped")
            recorder.clear_audio()
        # Someone else speaking Italian
        elif state.transcribe_to_en and not transcribing:
            print("Transcribing to English")
            transcribing = True
            recording_audio_en = recorder.get_audio()
            transcription_en = transcriber.transcribe_to_en(recording_audio_en, "it")
            print(transcription_en)
            print("Speaking started")
            tts_en.speak(transcription_en)
            print("Speaking stopped")
        elif transcribing and not state.transcribe_to_en:
            transcribing = False
            print("Done transcribing")
            recorder.clear_audio()

    recorder.stop()

if __name__ == "__main__":
    main()
