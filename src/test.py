from capture.recorder import Recorder
from transcription.transcriber import Transcriber

if __name__ == "__main__":
    transcriber = Transcriber()
    recorder = Recorder()

    r = recorder.record(10)
    transcriber.transcribe_to_en_and_save(r, "es")