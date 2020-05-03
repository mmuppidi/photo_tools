

import os 
from photo_tools import video


def test_create_video_from_frames(input_timelapse_images_path, destination_path):

    video.create_video_from_frames(sequence_dir=input_timelapse_images_path, output_dir=destination_path, framerate=25, path_suffix=".jpg")
