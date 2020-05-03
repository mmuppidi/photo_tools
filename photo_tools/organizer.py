"""
Module with functions to help organizing pictures from sd card
"""

import glob
import logging
import os
import time
from shutil import copyfile, move
from typing import Iterable

from tqdm import tqdm

# from typing import Text,


logger = logging.getLogger(__name__)


def list_files(glob_pattern: str) -> Iterable:
    """List files with the provided glob_pattern
    
    Args:
        glob_pattern (str): glob pattern for finding the images

    Returns:
        Iterable: iglob iterator will be returned
    """
    return glob.iglob(glob_pattern)


def get_creation_date(path: str) -> str:
    """Extract creation time of the file
    On Linux machines this function can only get the last modified time of a 
    file instead of creation time. As long as you use this function on the 
    images directly from sd card this should be okay.
    Ref: https://stackoverflow.com/questions/237079

    Args:
        path (str): Path to the file

    Returns:
        str: Timestamp provided in the form of 
            "%Y-%m-%d-%b"
            Ex: "2020-05-02-May"
    """

    try:
        # works on a mac
        ctime = os.stat(path).st_birthtime
    except AttributeError:
        # gets creation time for windows machine
        # get the last modification time for
        # linux machine
        ctime = os.stat(path).st_ctime
    return time.strftime("%Y-%m-%d-%b", time.localtime(ctime))


def mkdir(path: str):
    """ Create a directory if it doesn't exists

    Args:
        path (str): path of the directory to create
    """
    try:
        os.makedirs(path)
    except FileExistsError:
        return


def move_images(input_dir: str, output_dir: str, file_suffix: str = None):
    """ Moves images from input directory to provided output directory.
    This function identifies the creation time of the image and creates a 
    directory structure which looks like
        ::
            /<output_dir>/year/month/day/<image-name>

        ::
            /<output_dir>/2020/05-May/01/<image-name>

    Intended use of this function is to move image directly from cameras sd 
    card to external hard disk or path on the machine 

    On Linux machines this function can only get the last modified time of a file
    instead of creation time. As long as you use this function on the images 
    directly from sd card this should be okay.
    Ref: https://stackoverflow.com/questions/237079

    Args:
        input_dir (str): Path to raw images
        output_dir (str): Path where the images with the new directory structure
            should be moved to
        file_suffix (str, optional): Suffix of the files to move. For a JPEG 
            file this would be "jpg" or "jpeg". For a canon raw image this 
            would be "CR2". Defaults to None which will move all types of files.
    """

    file_suffix = f"*{file_suffix or ''}"

    for image in tqdm(list_files(os.path.join(input_dir, file_suffix))):
        # get creation date time
        year, month, date, month_abbr = get_creation_date(image).split("-")
        # construct destination path based on data time for
        new_path = os.path.join(
            output_dir, year, "{}-{}".format(month, month_abbr), date
        )
        # make sure destination directory exists
        mkdir(new_path)
        # try moving the images to destination location
        try:
            logger.debug(f"Moving {image} to {new_path}")
            move(image, os.path.join(new_path, os.path.basename(image)))
        except PermissionError:
            logger.error(f"Failed to move {image} to {new_path}", exc_info=True)
