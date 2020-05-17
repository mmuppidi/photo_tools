
from photo_tools import archive


def test_archive_directory(input_raw_images_path, destination_tar_file):

    archive.archive_directory(input_raw_images_path, destination_tar_file)