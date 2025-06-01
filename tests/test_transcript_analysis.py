import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.transcript_analysis import find_longest_transcript, find_transcript_with_longest_word, find_transcript_longer_or_shorter_than


@pytest.fixture
def transcripts_no_tie():
    transcriptions = [
        """
        the spirit and belief within 
        the team was\tpalpable
        """,  # max n_words = 9 (spread over two lines, with tab on second line)
        "green eggs and ham",
        "zed's dead",
        "concentration with unbelievable levels of skill"  # max word_length = 13
    ]
    assert len(transcriptions) == 4
    return transcriptions


@pytest.fixture
def transcripts_max_words_tie():
    transcriptions = [
        """
        the spirit and belief within 
        the team was palpable
        """,  # max n_words = 9 (spread over two lines)
        "foo bar baz lengthiness",
        "the spirit and belief within the team was palpable"  # same as 0, but on a single line
    ]
    assert len(transcriptions) == 3
    return transcriptions


@pytest.fixture
def transcripts_longest_word_tie():
    transcriptions = [
        "foo bar baz",
        "the spirit and belief within the team was palpable",
        "focus with unbelievable levels of skill",  # unbelievable = 12
        "The construction crew ate lunch by the old red barn.",  # construction = 12
    ]
    assert len(transcriptions) == 4
    return transcriptions


@pytest.fixture
def tmp_directory_populated_transcripts_no_tie_1(tmp_path, transcripts_no_tie):
    t1_tmp_path = tmp_path / "populated_transcripts_no_tie"
    os.makedirs(t1_tmp_path)
    for i, txt in enumerate(transcripts_no_tie):
        f_timestamp = datetime.now(timezone.utc) - timedelta(days=i) - timedelta(seconds=random.uniform(10*60, 120*60))
        f_timestamp_str = datetime.strftime(f_timestamp, '%Y%m%dT%H%M%S')
        fname = f"transcription_{i}_{f_timestamp_str}.txt"
        path = Path(t1_tmp_path) / fname

        with open(path, "w") as f:
            f.write(txt)

    assert len(os.listdir(t1_tmp_path)) == len(transcripts_no_tie)

    # throw in a random non-transcript file
    with open(Path(t1_tmp_path) / "foobar.txt", "w") as f:
        f.write("This has nothing to do with anything")

    assert len(os.listdir(t1_tmp_path)) == len(transcripts_no_tie) + 1

    yield t1_tmp_path


@pytest.fixture
def tmp_directory_populated_transcripts_max_words_tie_2(tmp_path, transcripts_max_words_tie):
    t2_tmp_path = tmp_path / "populated_transcripts_max_words_tie"
    os.makedirs(t2_tmp_path)
    for i, txt in enumerate(transcripts_max_words_tie):
        f_timestamp = datetime.now(timezone.utc) - timedelta(days=i) - timedelta(seconds=random.uniform(10*60, 120*60))
        f_timestamp_str = datetime.strftime(f_timestamp, '%Y%m%dT%H%M%S')
        fname = f"transcription_{i}_{f_timestamp_str}.txt"
        path = Path(t2_tmp_path) / fname

        with open(path, "w") as f:
            f.write(txt)

    assert len(os.listdir(t2_tmp_path)) == len(transcripts_max_words_tie)

    # throw in a random non-transcript file
    with open(Path(t2_tmp_path) / "foobar.txt", "w") as f:
        f.write("This has nothing to do with anything")

    assert len(os.listdir(t2_tmp_path)) == len(transcripts_max_words_tie) + 1

    yield t2_tmp_path


@pytest.fixture
def tmp_directory_populated_transcripts_longest_word_tie_3(tmp_path, transcripts_longest_word_tie):
    t3_tmp_path = tmp_path / "populated_transcripts_longest_word_tie"
    os.makedirs(t3_tmp_path)
    for i, txt in enumerate(transcripts_longest_word_tie):
        f_timestamp = datetime.now(timezone.utc) - timedelta(days=i) - timedelta(seconds=random.uniform(10*60, 120*60))
        f_timestamp_str = datetime.strftime(f_timestamp, '%Y%m%dT%H%M%S')
        fname = f"transcription_{i}_{f_timestamp_str}.txt"
        path = Path(t3_tmp_path) / fname

        with open(path, "w") as f:
            f.write(txt)

    assert len(os.listdir(t3_tmp_path)) == len(transcripts_longest_word_tie)

    # throw in a random non-transcript file
    with open(Path(t3_tmp_path) / "foobar.txt", "w") as f:
        f.write("This has nothing to do with anything")

    assert len(os.listdir(t3_tmp_path)) == len(transcripts_longest_word_tie) + 1

    yield t3_tmp_path


def load_transcripts_from_path(transcripts_path: str) -> dict:
    transcripts = {}
    for f in os.listdir(transcripts_path):
        if not (f.startswith('transcription_') and f.endswith('.txt')):
            continue
        with open(Path(transcripts_path) / f, 'r') as f_open:
            transcripts[str(Path(transcripts_path) / f)] = f_open.read()

    return transcripts


def test_find_longest_transcript_no_tie(tmp_directory_populated_transcripts_no_tie_1):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_no_tie_1)
    results = find_longest_transcript(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 1

    n_words, txt_path = results[0]
    assert n_words == 9
    assert "transcription_0" in txt_path
    assert "populated_transcripts_no_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path


def test_find_transcript_with_longest_word_no_tie(tmp_directory_populated_transcripts_no_tie_1):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_no_tie_1)
    results = find_transcript_with_longest_word(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 1

    word, txt_path = results[0]
    assert word == "concentration"
    assert "transcription_3" in txt_path
    assert "populated_transcripts_no_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path


def test_find_longest_transcript_max_words_tie(tmp_directory_populated_transcripts_max_words_tie_2):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_max_words_tie_2)
    results = find_longest_transcript(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 2

    n_words_list = [res[0] for res in results]
    fullpath_list = [res[1] for res in results]

    assert n_words_list == [9, 9]  # both results have same value
    # check the expected transcription paths have been found (idx: 0 and 2)
    for expected in ['transcription_0', 'transcription_2']:
        found = False
        for txt_path in fullpath_list:
            assert "populated_transcripts_max_words_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path
            if expected in txt_path:
                found = True
                break
        assert found


def test_find_transcript_with_longest_word_max_words_tie(tmp_directory_populated_transcripts_max_words_tie_2):
    """Note: this second case only causes a tie on the longest transcription, NOT the longest word - so this produces just one result"""
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_max_words_tie_2)
    results = find_transcript_with_longest_word(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 1

    word, txt_path = results[0]
    assert word == "lengthiness"
    assert "transcription_1" in txt_path
    assert "populated_transcripts_max_words_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path


def test_find_longest_transcript_longest_word_tie(tmp_directory_populated_transcripts_longest_word_tie_3):
    """Note: this third case only causes a tie on the longest word in transcriptions, NOT the transcription length -
    so this produces just one result
    """
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_longest_word_tie_3)
    results = find_longest_transcript(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 1

    n_words, txt_path = results[0]
    assert n_words == 10
    assert "transcription_3" in txt_path
    assert "populated_transcripts_longest_word_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path


def test_find_transcript_with_longest_word_longest_word_tie(tmp_directory_populated_transcripts_longest_word_tie_3):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_longest_word_tie_3)
    results = find_transcript_with_longest_word(transcripts=transcripts)

    assert isinstance(results, list)
    assert len(results) == 2
    fullpath_list = [res[1] for res in results]

    # check the expected transcription paths have been found (idx: 2 and 3) and contain their respective expected words
    for i, (expected_word, expected_fname_stump) in enumerate([
        ('unbelievable', 'transcription_2'),
        ('construction', 'transcription_3'),
    ]):
        found = False
        for txt_path in fullpath_list:
            assert "populated_transcripts_longest_word_tie" in txt_path and os.path.sep in txt_path  # ensure that its full path
            if expected_fname_stump in txt_path:
                found = True
                word, _ = [res for res in results if res[1] == txt_path][0]
                assert word == expected_word
                break
        assert found


def test_find_transcript_longer_or_shorter_than_word_no_tie(tmp_directory_populated_transcripts_no_tie_1):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_no_tie_1)

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=5)
    assert len(results) == 2  # "the spirit ..." and "concentration ..."
    n_words_list = [res[0] for res in results]
    assert set(n_words_list) == {9, 6}

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=-5)
    assert len(results) == 2  # "green egss..." and "zed's dead"
    n_words_list = [res[0] for res in results]
    assert set(n_words_list) == {4, 2}

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=5, year=1970)  # nothing from 1970
    assert len(results) == 0


def test_find_transcript_longer_or_shorter_than_max_words_tie(tmp_directory_populated_transcripts_max_words_tie_2):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_max_words_tie_2)

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=5)
    assert len(results) == 2  # "the spirit ..." x2
    n_words_list = [res[0] for res in results]
    assert set(n_words_list) == {9, 9}

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=-3)
    assert len(results) == 0


def test_find_transcript_longer_or_shorter_than_longest_word_tie(tmp_directory_populated_transcripts_longest_word_tie_3):
    transcripts = load_transcripts_from_path(transcripts_path=tmp_directory_populated_transcripts_longest_word_tie_3)

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=1, year=datetime.now().year)
    assert len(results) == 4  # all of them in this
    n_words_list = [res[0] for res in results]
    assert set(n_words_list) == {3, 9, 6, 10}

    results = find_transcript_longer_or_shorter_than(transcripts=transcripts, n_thresh=1, year=datetime.now().year-10)
    assert len(results) == 0  # nothing from 10 yrs ago
