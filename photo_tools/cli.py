"""Module with command line utility functions
"""


import click

from . import organizer
from . import video


@click.group()
def main_cli():
    pass


@main_cli.command("import")
@click.option(
    "--input-dir",
    "-i",
    required=True,
    help="Path to source directory of the images",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    help="Path to destinatiom directory of the images",
)
@click.option("--file-suffix", "-s", help="Suffix of the files to move")
def import_images(input_dir, output_dir, file_suffix):
    organizer.move_images(input_dir, output_dir, file_suffix)


@main_cli.command("render-video")
@click.option(
    "--input-dir",
    "-i",
    required=True,
    help="Path to source directory of the images",
)
@click.option(
    "--output-dir",
    "-o",
    required=True,
    help="Output path of the rendered video",
)
@click.option("--frame-rate", "-fps", type=int, help="Frames per second")
@click.option("--file-suffix", "-s", help="Suffix of the files to move")
def render_video_from_image_frames(
    input_dir, output_path, frame_rate, file_suffix
):
    video.create_video_from_frames(
        sequence_dir=input_dir,
        output_dir=output_path,
        framerate=frame_rate,
        path_suffix=file_suffix,
    )
