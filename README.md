## Installation and usage

```bash
git clone git@github.com:lukerm/vosk-dictation
cd vosk-dictation
mkvirtualenv vosk

# sudo apt install portaudio19-dev  # possibly needed
pip install -r requirements.txt

# Download STT model (~70MB)
mkdir ~/.vosk/
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d ~/.vosk

# Microphone at the ready
python src/voice_recorder.py -s 30
```

## Example output

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

## Usage with other tools

### Ollama 🦙

The Ollama project [page](https://github.com/ollama/ollama).

```bash
export OLLAMA_MODEL=llama3.2:1b
export PROMPT_RULES="Make this text grammatically correct and well-structured. Do not include preamble in your output, just the corrected version of what follows."
python $HOME/vosk-dictation/src/voice_recorder.py && \
  echo && \
  ollama run $OLLAMA_MODEL "`echo $PROMPT_RULES` \n ----- \n `cat /tmp/vosk_transcription_latest.txt`"
```

### Useful aliases

```bash
alias vosk2ollama='echo "Prompt rules are: $PROMPT_RULES" && \
  python $HOME/vosk-dictation/src/voice_recorder.py && \
  echo && echo "Sanitised version (by $OLLAMA_MODEL):" && echo && \
  ollama run llama3.2:1b "`echo $PROMPT_RULES` \n ----- \n `cat /tmp/vosk_transcription_latest.txt`"'
```