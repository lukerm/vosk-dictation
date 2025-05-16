# sudo apt install portaudio19-dev
# pip install vosk pyaudio pyperclip

import argparse
import json
import os
from genericpath import exists
from pathlib import Path

import wave
import pyaudio
import pyperclip
from vosk import Model, KaldiRecognizer

# Configure audio recording
FRAME_RATE = 16000
CHANNELS = 1

# Path to the model you downloaded
ROOT_DIR = os.path.expanduser("~/.vosk")
MODEL_PATH = Path(ROOT_DIR) / "vosk-model-small-en-us-0.15"
TRANS_PATH = Path(ROOT_DIR) / "transcriptions"
RECORD_PATH = Path(ROOT_DIR) / "recordings"
os.makedirs(TRANS_PATH, exist_ok=True)
os.makedirs(RECORD_PATH, exist_ok=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--record-seconds', '-s', type=int, default=10, help="number of seconds to record and transcribe")
    parser.add_argument('--model-path', '-m', type=str, default=MODEL_PATH, help="abs filepath where the transcription model is stored")
    args = parser.parse_args()

    # Load the model
    model = Model(str(args.model_path))

    # Setup recording
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=FRAME_RATE,
                    input=True,
                    frames_per_buffer=4096)

    # Create recognizer
    rec = KaldiRecognizer(model, FRAME_RATE)

    record_seconds = args.record_seconds
    print("Recording for", record_seconds, "seconds...")
    frames = []

    # Record audio
    text_parts = []
    for i in range(0, int(FRAME_RATE / 4096 * record_seconds)):
        data = stream.read(4096)
        frames.append(data)
        if rec.AcceptWaveform(data):
            text_part = json.loads(rec.Result())['text']
            print(text_part)
            text_parts.append(text_part)
            #print("Partial result:", result["text"])


    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Process final result
    final_part = json.loads(rec.FinalResult())['text']
    if final_part.strip():
        print(final_part)
        text_parts.append(final_part)


    transcribed_text = '\n'.join(text_parts) + '\n'

    print('\n')
    print("Recording finished")

    print('\n')
    print(transcribed_text)

    # Save text to file
    from datetime import datetime
    now_str = datetime.strftime(datetime.now(), '%Y%m%dT%H%M%S')
    transcribed_fname = Path(TRANS_PATH) / f"transcription_{now_str}.txt"
    with open(transcribed_fname, "w") as text_file:
        text_file.write(transcribed_text)
    print(f"Full transcription saved to {transcribed_fname}")

    pyperclip.copy(transcribed_text)
    print(f"Full transcription also ready to be copied from the clipboard")

    # Optionally save audio file
    recorded_fname = Path(RECORD_PATH) / f"recording_{now_str}.wav"
    with wave.open(str(recorded_fname), "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(FRAME_RATE)
        wf.writeframes(b''.join(frames))
    print(f"Audio saved to {recorded_fname}")
