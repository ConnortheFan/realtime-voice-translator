from capture.recorder import Recorder
from transcription.transcriber import Transcriber
from translation.translator import Translator
from tts.tts import TextToSpeech
import time
from pynput import keyboard
from log_utils import setup_logging, log_calls

recording = False
running = True
transcribe_to_en = False

def on_press(key):
    global recording, running, transcribe_to_en
    if key == keyboard.Key.space:
        recording = True
    elif key == keyboard.Key.enter:
        transcribe_to_en = True
    elif key == keyboard.Key.esc:
        print("\nESC pressed, program exiting")
        running = False

def on_release(key):
    global recording, transcribe_to_en
    if key == keyboard.Key.space:
        recording = False
    elif key == keyboard.Key.enter:
        transcribe_to_en = False

@log_calls
def main():
    setup_logging(debug = False)
    global recording, running, transcribe_to_en

    recorder = Recorder()
    transcriber = Transcriber()
    translator = Translator("it", "en")
    tts_it = TextToSpeech("it")
    tts_en = TextToSpeech("en")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print("All modules initialized, program running")
    print("Press ENTER to transcribe Italian to English")
    print("Hold SPACE to talk")
    print("Press ESC to quit")

    started = False
    transcribing = False

    recorder.start()

    while running:
        # You speaking via push-to-talk SPACE bar
        if recording and not started:
            started = True
            print("\nRecording started")
            recorder.clear_audio()
            
        elif not recording and started:
            started = False
            print("Recording stopped")

            recording_audio = recorder.get_audio()
            transcription = transcriber.transcribe(recording_audio)
            translation = translator.translate_ba(transcription)
            print("Speaking started")
            tts_it.speak(translation)
            print("Speaking stopped")
            recorder.clear_audio()
        
        # Someone else speaking Italian
        elif transcribe_to_en and not transcribing:
            print("Transcribing to English")
            transcribing = True
            recording_audio_en = recorder.get_audio()
            transcription_en = transcriber.transcribe_to_en(recording_audio_en, "it")
            print("Speaking started")
            tts_en.speak(transcription_en)
            print("Speaking stopped")
        elif transcribing and not transcribe_to_en:
            transcribing = False
            print("Done transcribing")
            recorder.clear_audio()

    recorder.stop()

if __name__ == "__main__":
    main()