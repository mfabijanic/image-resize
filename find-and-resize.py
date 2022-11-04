#
# Resize image files in directory
#
# Used for resize OTOBO Helpdesk images in articles that are saved on filesystem.
# OTOBO articles directory: /opt/otobo/var/articles
#
# Author: Matej Fabijanic <root4unix@gmail.com>
#

import filetype
import os
import configparser
import logging
import logging.config
import shutil
from PIL import Image, ImageOps


logging.config.fileConfig(fname='logging.ini', disable_existing_loggers=False)
# Get the logger specified in the file
logger = logging.getLogger('resize');

config = configparser.ConfigParser()
config.read('find-and-resize.ini')
# Maximal width or heigth
max_threshold_size = int(config['image']['max_threshold_size'])


def get_file_size(file_path, unit='bytes'):
    file_size = os.path.getsize(file_path)
    exponents_map = {'bytes': 0, 'kb': 1, 'mb': 2, 'gb': 3}
    if unit not in exponents_map:
        raise ValueError("Must select from \
        ['bytes', 'kb', 'mb', 'gb']")
    else:
        size = file_size / 1024 ** exponents_map[unit]
        return round(size, 3)


def get_new_size(width, height, max_threshold_size):
    width_new = max_threshold_size / max(width, height) * width
    height_new = max_threshold_size / max(width, height) * height
    return (int(width_new), int(height_new))


def resize_image(img_file):
    EXIF_ORIENTATION = 0x0112

    # Original file size
    img_file_size_old = get_file_size(img_file, 'kb');

    # fullsized image
    img = Image.open(img_file)
    code = img.getexif().get(EXIF_ORIENTATION, 1)
    if code and code != 1:
        logger.info('ROTATE "%s"; EXIF rotation code: %s' % (img_file, code))
        img = ImageOps.exif_transpose(img)
        img.save(img_file)

    # Image size
    img_wsize, img_hsize = img.size
    # New image size
    img_wsize_new, img_hsize_new = get_new_size(img_wsize, img_hsize, max_threshold_size)

    resize_ratio = (float(img_wsize) / img_wsize_new)

    # Skip if width or heigth is smaller or equal as max_threshold_size
    if img_wsize <= img_wsize_new:
        return logger.info('SKIP "%s" %skB %sx%s -> %sx%s (resize_ratio %s)' %
            (img_file, img_file_size_old, img_wsize, img_hsize, str(img_wsize_new), str(img_hsize_new), str(resize_ratio)))

    img = img.resize((img_wsize_new, img_hsize_new), Image.ANTIALIAS)
    img.save(img_file, quality=50)
    img.close()

    # New file size
    img_file_size_new = get_file_size(img_file, 'kb');
    resize_ratio_file_size = (img_file_size_old / img_file_size_new)

    logger.info('RESIZE "%s" %skB %sx%s -> %skB %sx%s (file size ratio %s; resize ratio %s)' %
        (img_file, img_file_size_old, img_wsize, img_hsize, img_file_size_new,
        str(img_wsize_new), str(img_hsize_new), str(resize_ratio_file_size),
        str(resize_ratio)))


def main():
    path = config['image']['path']
    # temp files
    path_tmp = config['image']['path_tmp']
    # image formats
    formats = [x.strip() for x in config['image']['formats'].split(',')]

    if not os.path.isdir(path_tmp):
        try:
            os.mkdir((path_tmp))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    for (path, dirs, files) in os.walk(path):
        for file in files:
            if file.endswith(tuple(formats)):
                img_file = os.path.join(path, file)
                if filetype.is_image(img_file):
                    resize_image(img_file)


if __name__== "__main__":
    main()