
import os
import shutil
import tarfile

import pytest


_SAMPLE_IMAGES = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'pictures.tar.gz' ))

_SAMPLE_TIMELAPSE_IMAGES = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'timelapse.tar.gz' ))

_TEST_DATA_DIR = "/tmp/organizer_test"
_INPUT_PATH = os.path.join(_TEST_DATA_DIR, "source")
_OUTPUT_PATH = os.path.join(_TEST_DATA_DIR, "destination")


def reset_dir(path):
    try:
        shutil.rmtree(path)
        os.makedirs(path)
    except FileNotFoundError:
        os.makedirs(path)


@pytest.fixture
def input_raw_images_path():
    reset_dir(_INPUT_PATH)

    with tarfile.open(_SAMPLE_IMAGES, "r:gz") as tf:
        tf.extractall(_INPUT_PATH)

    return os.path.join(_INPUT_PATH, 'pictures')


@pytest.fixture
def destination_path():
    reset_dir(_OUTPUT_PATH)
    return _OUTPUT_PATH


@pytest.fixture
def destination_tar_file():
    reset_dir(_OUTPUT_PATH)
    return os.path.join(_OUTPUT_PATH, 'archive.tar.gz')


@pytest.fixture
def input_timelapse_images_path():
    reset_dir(_INPUT_PATH)

    with tarfile.open(_SAMPLE_TIMELAPSE_IMAGES, "r:gz") as tf:
        tf.extractall(_INPUT_PATH)

    return os.path.join(_INPUT_PATH, 'timelapse')


