""" Module with functions to help with video creation and editing
"""

import os

import ffmpeg


def create_video_from_frames(
    sequence_dir: str, output_dir: str, framerate: int, path_suffix: str = None
):
    """ Function converts the sequence of frames into a MPEG-4 video this 
    function is a wrapper for the following ffmpeg command

        ::
            ffmpeg -framerate 25 -pattern_type glob -i '*.jpg' -c:v libx264 \
                -preset veryslow -pix_fmt yuv420p \
                -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" out.mp4

    Args:
        sequence_dir (str): Path to the directory with sequence of images 
        output_dir (str): Path to the directory where output should be written to
        framerate (int): framerate (fps) of the output video
        path_suffix (str, optional): Suffix of the input files. Defaults to None.
            ex: for JPEG images it would be .jpg or .jpeg or for PNG it would be
                .png
    """

    output_path = os.path.join(output_dir, "output.mp4")

    ffmpeg.input(
        os.path.join(sequence_dir, f"*{path_suffix or ''}"),
        pattern_type="glob",
        framerate=framerate,
    ).filter("pad", width="ceil(iw/2)*2", height="ceil(ih/2)*2").output(
        output_path, vcodec="libx264", preset="veryslow", pix_fmt="yuv420p"
    ).run()
