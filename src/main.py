from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
import time
from pynput import keyboard

finished = False

def on_press(key):
    global finished
    if key == keyboard.Key.space:
        print("Pressed space, stopping recording")
        finished = True

def main():
    start = time.perf_counter()

    print("Starting main module")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    recorder = Recorder()
    recorder.start()

    while not finished:
        pass

    recording = recorder.stop_and_save()

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