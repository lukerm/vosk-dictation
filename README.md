Installation and usage:

```bash
git clone git@github.com:lukerm/vosk-dictation
cd vosk-dictation
mkvirtualenv vosk

# sudo apt install portaudio19-dev  # possibly needed
pip install -r requirements.txt

# Microphone at the ready
python src/voice_recorder.py -s 30
```

Example output:

```text
(vosk) lukerm:~/vosk-dictation$ python src/voice_recorder.py
Recording for 60 seconds...
Press Ctrl+C at any time to exit safely
a program to record your vocal mutterings so you don't have to type them
^C

Recording finished


a program to record your vocal mutterings so you don't have to type them

Full transcription saved to /home/luke/.vosk/transcriptions/transcription_20250516T224655.txt
Full transcription also ready to be copied from the clipboard
Audio saved to /home/luke/.vosk/recordings/recording_20250516T224655.wav
```