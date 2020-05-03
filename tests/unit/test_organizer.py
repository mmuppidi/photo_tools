
import os
import glob

import pytest

from photo_tools import organizer


def test_move_images(input_raw_images_path, destination_path):
    
    organizer.move_images(input_raw_images_path, destination_path)

    assert len(glob.glob(os.path.join(destination_path, "*/*/*/*"))) == 3
