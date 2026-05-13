from capture.recorder import Recorder
from transcription.transcriber import Transcriber

def main():
    print("main module")

    recorder = Recorder()
    recording = recorder.record_and_save(10)

    transcriber = Transcriber()
    transcription = transcriber.transcribe_and_save(recording)

if __name__ == "__main__":
    main()