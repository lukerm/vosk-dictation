import os
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from src.utils import mv_old_transcriptions


@pytest.fixture
def empty_tmp_directory_from(tmp_path):
    ef_tmp_path = tmp_path / "from_dir"
    os.makedirs(ef_tmp_path)
    assert len(os.listdir(ef_tmp_path)) == 0
    return ef_tmp_path


@pytest.fixture
def empty_tmp_directory_to(tmp_path):
    et_tmp_path = tmp_path / "to_dir"
    os.makedirs(et_tmp_path)
    assert len(os.listdir(et_tmp_path)) == 0
    return et_tmp_path


@pytest.fixture
def populated_tmp_directory_from(tmp_path):
    ff_tmp_path = tmp_path / "populated_from_dir"
    os.makedirs(ff_tmp_path)
    for i in range(1, 12):
        f_timestamp = datetime.now(timezone.utc) - timedelta(days=i) - timedelta(seconds=random.uniform(10*60, 120*60))
        f_timestamp_str = datetime.strftime(f_timestamp, '%Y%m%dT%H%M%S')
        fname = f"transcription_{f_timestamp_str}.txt"
        path = Path(ff_tmp_path) / fname
        path.touch()

    assert len(os.listdir(ff_tmp_path)) == 11

    yield ff_tmp_path


def test_mv_old_transcriptions_has_moved_7days(populated_tmp_directory_from, empty_tmp_directory_to):
    # this is a dryrun operation => no file movements
    n_files = mv_old_transcriptions(n_days=7, from_folder=populated_tmp_directory_from, to_folder=None)
    assert n_files == 5
    assert len(os.listdir(populated_tmp_directory_from)) == 11
    assert len(os.listdir(empty_tmp_directory_to)) == 0

    # this command carries out the real set of operations
    n_files = mv_old_transcriptions(n_days=7, from_folder=populated_tmp_directory_from, to_folder=empty_tmp_directory_to)
    assert n_files == 5
    assert len(os.listdir(populated_tmp_directory_from)) == 6
    assert len(os.listdir(empty_tmp_directory_to)) == 5


def test_mv_old_transcriptions_hasnt_moved_empty_empty(empty_tmp_directory_from, empty_tmp_directory_to):
    assert len(os.listdir(empty_tmp_directory_from)) == len(os.listdir(empty_tmp_directory_to)) == 0
    assert mv_old_transcriptions(n_days=1_000, from_folder=empty_tmp_directory_from, to_folder=empty_tmp_directory_to) == 0
    assert len(os.listdir(empty_tmp_directory_from)) == len(os.listdir(empty_tmp_directory_to)) == 0
