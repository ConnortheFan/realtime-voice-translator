from capture.recorder import Recorder
from transcription.transcriber import Transcriber
import time

def main():
    start = time.perf_counter()

    print("Starting main module")

    recorder = Recorder()
    recording = recorder.record_and_save(10)

    transcriber = Transcriber()
    transcription = transcriber.transcribe_and_save(recording)

    end = time.perf_counter()
    print(f"\nProgram took {end - start} seconds")

if __name__ == "__main__":
    main()