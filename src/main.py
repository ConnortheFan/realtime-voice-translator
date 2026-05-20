from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
import time

def main():
    start = time.perf_counter()

    print("Starting main module")

    recorder = Recorder()
    recording = recorder.record_and_save(10)

    transcriber = Transcriber()
    transcription = transcriber.transcribe_and_save(recording)

    translator = Translator("it")
    translation = translator.translate_ba_and_save(transcription)

    tts_it = TextToSpeech("it")
    tts_it.speak_and_save(translation)

    end = time.perf_counter()
    print(f"\nProgram took {end - start:.3f} seconds")

if __name__ == "__main__":
    main()