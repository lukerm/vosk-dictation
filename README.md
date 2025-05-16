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