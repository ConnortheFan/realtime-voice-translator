from audio.recorder import Recorder


def main():
    print("main module")

    recorder = Recorder()
    recorder.record_and_save(5)

if __name__ == "__main__":
    main()