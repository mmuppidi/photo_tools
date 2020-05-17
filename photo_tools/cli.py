"""Module with command line utility functions
"""


import os
import tempfile
import uuid

import click

from . import archive, organizer

import logging

logging.basicConfig(level=logging.INFO)


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
@click.option("--file-prefix", "-p", help="Prefix of the files to move")
@click.option("--file-suffix", "-s", help="Suffix of the files to move")
def render_video_from_image_frames(
    input_dir, output_dir, frame_rate, file_prefix, file_suffix
):
    from . import video

    video.create_video_from_frames(
        sequence_dir=input_dir,
        output_dir=output_dir,
        framerate=frame_rate,
        file_prefix=file_prefix,
        file_suffix=file_suffix,
    )


@main_cli.command("archive")
@click.option(
    "--input-dir",
    "-i",
    required=True,
    help="Path to source directory of the images",
)
@click.option(
    "--to-s3", is_flag=True, help="Should the archive be pushed to s3",
)
@click.option(
    "--output-prefix", "-p", help="Prefix of the output tarfile",
)
@click.option(
    "--bucket",
    default="mk-photo",
    help="Bucket where archive needs to be saved",
)
def archive_to_s3(input_dir, to_s3, output_prefix, bucket):

    output_prefix = output_prefix or uuid.uuid4().hex

    with tempfile.TemporaryDirectory(prefix=output_prefix) as tmpdirname:
        # create the archive of the input directory
        tmp_tar_file = os.path.join(tmpdirname, f"{output_prefix}.tar.gz")
        archive.archive_directory(input_dir, tmp_tar_file)

        # push to s3
        if to_s3:
            s3_path = f"{output_prefix}.tar.gz"
            archive.push_to_s3(tmp_tar_file, bucket, s3_path)
            archive.generate_presigned_url(bucket, s3_path)
