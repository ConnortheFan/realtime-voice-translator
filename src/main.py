from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
import time
from pynput import keyboard

recording = False
running = True

def on_press(key):
    global recording, running
    if key == keyboard.Key.space:
        recording = True
    elif key == keyboard.Key.esc:
        print("\nESC pressed, program exiting")
        running = False

def on_release(key):
    global recording
    if key == keyboard.Key.space:
        recording = False

def main():
    start = time.perf_counter()

    global recording, running

    print("Starting main module")

    recorder = Recorder()
    transcriber = Transcriber()
    translator = Translator("it")
    tts_it = TextToSpeech("it")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("All modules initialized, program running")
    print("Hold SPACE to talk")
    print("Press ESC to quit")

    started = False

    while running:
        
        if recording and not started:
            started = True
            print("\nRecording started")
            recorder.start()
            
        elif not recording and started:
            started = False
            print("Recording stopped")

            recording_audio = recorder.stop_and_save()
            transcription = transcriber.transcribe_and_save(recording_audio)
            translation = translator.translate_ba_and_save(transcription)
            tts_it.speak_and_save(translation)

    end = time.perf_counter()
    print(f"\nProgram took {end - start:.3f} seconds")

if __name__ == "__main__":
    main()