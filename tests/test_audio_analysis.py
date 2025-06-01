import os
from pathlib import Path

import pytest

from src.audio_analysis import get_recording_lengths, get_recording_silence_lengths


@pytest.fixture
def wav_directory():
    return Path(__file__).parent / "fixtures" / "wav"

@pytest.fixture
def empty_tmp_directory(tmp_path):
    ed_tmp_path = tmp_path / "empty1"
    os.makedirs(ed_tmp_path)
    assert len(os.listdir(ed_tmp_path)) == 0
    return ed_tmp_path


@pytest.fixture
def audio_file_0(wav_directory):
    """Largest of the three audio files => """
    path_to_wav = wav_directory / "recording_20250517T062603.wav"
    assert os.path.exists(path_to_wav)
    return path_to_wav

@pytest.fixture
def audio_file_1(wav_directory):
    path_to_wav = wav_directory / "recording_20250516T190844.wav"
    assert os.path.exists(path_to_wav)
    return path_to_wav

@pytest.fixture
def audio_file_2(wav_directory):
    path_to_wav = wav_directory / "recording_20250516T224440.wav"
    assert os.path.exists(path_to_wav)
    return path_to_wav



def test_get_recording_lengths(wav_directory, audio_file_0, audio_file_1, audio_file_2):
    audio_lengths = get_recording_lengths(recordings_folder=wav_directory)

    assert isinstance(audio_lengths, list)
    assert len(audio_lengths) == 3

    # Longest recording
    duration, file_path = audio_lengths[0]
    assert duration == 14.85
    assert os.path.split(file_path)[1] == os.path.split(audio_file_0)[1]
    # Second longest
    duration, file_path = audio_lengths[1]
    assert duration == 4.86
    assert os.path.split(file_path)[1] == os.path.split(audio_file_1)[1]
    # shortest
    duration, file_path = audio_lengths[2]
    assert duration == 3.84
    assert os.path.split(file_path)[1] == os.path.split(audio_file_2)[1]


def test_get_recording_lengths_empty_dir(empty_tmp_directory):
    audio_lengths = get_recording_lengths(recordings_folder=empty_tmp_directory)
    assert isinstance(audio_lengths, list)
    assert len(audio_lengths) == 0


def test_get_recording_silence_lengths(wav_directory, audio_file_0, audio_file_1, audio_file_2):

    silence_lengths = get_recording_silence_lengths(recordings_folder=wav_directory)

    assert isinstance(silence_lengths, list)
    assert len(silence_lengths) == 3
    assert silence_lengths[0][0] > silence_lengths[-1][0]  # check ordered descending

    for silence_duration, file_path in silence_lengths:
        if str(file_path) == str(audio_file_0):
            assert 9.0 < silence_duration < 9.5  # real answer: 9.23
        if str(file_path) == str(audio_file_1):
            assert 1.5 < silence_duration < 2.0  # real answer: 1.74
        if str(file_path) == str(audio_file_2):
            assert 1.7 < silence_duration < 2.2  # real answer: 1.92


def test_get_recording_silence_lengths_empty_dir(empty_tmp_directory):
    silence_lengths = get_recording_silence_lengths(recordings_folder=empty_tmp_directory)
    assert isinstance(silence_lengths, list)
    assert len(silence_lengths) == 0