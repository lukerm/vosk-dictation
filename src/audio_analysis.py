import os
import wave
from pathlib import Path
from typing import List, Tuple

import numpy as np


def get_wav_length(file_path: str) -> float:
    """
    Open the wave file given by file_path, returning duration in seconds, round to 2 decimal places.
    """
    # Open the wave file
    with wave.open(str(file_path), 'rb') as wf:
        # Calculate duration: frames / framerate = seconds
        frames = wf.getnframes()
        rate = wf.getframerate()
        duration = frames / rate
        # Round to 2 decimal places
        duration_rounded = round(duration, 2)
    return duration_rounded


def get_recording_lengths(recordings_folder: str) -> List[Tuple[float, str]]:
    """
    Find the duration in seconds of all audio files in the given folder.

    Args:
        recordings_folder: Path to the folder containing audio recordings

    Returns:
        List of tuples containing (duration, filepath) ordered by duration (decreasing)
    """
    durations = []

    # Convert to Path object if it's a string
    folder_path = Path(recordings_folder) if isinstance(recordings_folder, str) else recordings_folder

    # Iterate through all files in the folder
    for file_path in folder_path.glob('*.wav'):
        try:
            duration = get_wav_length(str(file_path))
            durations.append((duration, str(file_path)))
        except (wave.Error, IsADirectoryError, PermissionError) as e:
            # Skip files that aren't valid wave files
            continue

    # Sort by duration in descending order
    durations.sort(reverse=True)
    return durations


def get_wav_data(file_path: str) -> np.ndarray:
    """Load the data from the given the wave file in file_path."""
    with wave.open(str(file_path), 'rb') as wf:
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        nframes = wf.getnframes()

        if sampwidth != 2 or channels != 1:
            print('Wav file not in expected format: {sampwidth=} and {channels=} (should be 2 and 1 respectively. Skipping')
            raise ValueError

        # Read all frames and unpack to integers
        frames = wf.readframes(nframes)
        audio_data = np.frombuffer(frames, dtype=np.int16)

    return audio_data.astype(np.int64)


def get_silence_length(file_path: str) -> float:
    """Get the total length of silences by iterating over chunks, checking whether their RMS values are below a threshold."""
    audio_data = get_wav_data(file_path=file_path)

    # Calculate the RMS for each chunk of audio
    threshold = 20
    chunk_size = 1000  # Adjust this to suit your needs
    rms_values = []
    bad_chunks = {}
    for i in range(0, len(audio_data), chunk_size):
        chunk = audio_data[i:i + chunk_size]
        rms = np.sqrt(np.mean(chunk ** 2))
        if np.isnan(rms):
            print(i)
            bad_chunks[i] = chunk
        rms_values.append(rms)

    # Identify silences based on the threshold
    silence_indices = [i for i, rms in enumerate(rms_values) if rms < threshold]

    silence_proportion = len(silence_indices) / len(rms_values)
    return silence_proportion * get_wav_length(file_path=file_path)


def get_recording_silence_lengths(recordings_folder: str) -> List[Tuple[float, str]]:
    """
    Find the silence length (duration in seconds) in each audio file in the given folder.

    Args:
        recordings_folder: Path to the folder containing audio recordings

    Returns:
        List of tuples containing (silence_duration, filepath) ordered by silence duration (decreasing)
    """
    silence_durations = []

    # Convert to Path object if it's a string
    folder_path = Path(recordings_folder) if isinstance(recordings_folder, str) else recordings_folder

    # Iterate through all files in the folder
    for file_path in folder_path.glob('recording_*.wav'):
        try:
            silence_duration = get_silence_length(str(file_path))
            silence_durations.append((silence_duration, str(file_path)))
        except (wave.Error, IsADirectoryError, PermissionError, ValueError) as e:
            continue # Skip files that aren't valid wave files

    # Sort by duration in descending order
    silence_durations.sort(reverse=True)
    return silence_durations


if __name__ == "__main__":
    # Get the path where voice_recorder.py saves recordings
    ROOT_DIR = os.path.expanduser("~/.vosk")
    RECORD_PATH = Path(ROOT_DIR) / "recordings"

    # Get the recording lengths
    recording_lengths = get_recording_lengths(RECORD_PATH)

    # Print the three longest recordings
    print("Three longest recordings:")
    for i, (duration, filepath) in enumerate(recording_lengths[:3], 1):
        print(f"{i}. Duration: {duration:.2f} seconds - File: {filepath}")

    # If there are fewer than 3 recordings
    if len(recording_lengths) < 3:
        print(f"Note: Only {len(recording_lengths)} recordings found.")
    elif not recording_lengths:
        print("No recordings found.")

    # Get silence lengths and calculate densities
    silence_lengths = get_recording_silence_lengths(RECORD_PATH)

    # Create dictionaries for quick lookup
    duration_dict = {filepath: duration for duration, filepath in recording_lengths}
    silence_dict = {filepath: silence for silence, filepath in silence_lengths}

    # Calculate silence densities (silence_duration / total_duration)
    densities = []
    for filepath, total_duration in duration_dict.items():
        if filepath in silence_dict:
            silence_duration = silence_dict[filepath]
            density = silence_duration / total_duration if total_duration > 0 else 0
            densities.append((density, filepath, silence_duration, total_duration))

    # Sort by density descending
    densities.sort(reverse=True)

    # Print top 3 with highest silence densities
    print("\nTop 3 recordings with highest silence densities:")
    for i, (density, filepath, silence_dur, total_dur) in enumerate(densities[:3], 1):
        print(f"{i}. Density: {density:.2%} (Silence: {silence_dur:.2f}s / Total: {total_dur:.2f}s) - File: {filepath}")

    if len(densities) < 3:
        print(f"Note: Only {len(densities)} valid recordings with silence data found.")
    elif not densities:
        print("No valid recordings with silence data found.")