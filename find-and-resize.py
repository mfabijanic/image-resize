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
from PIL import Image


logging.config.fileConfig(fname='logging.ini', disable_existing_loggers=False)
# Get the logger specified in the file
logger = logging.getLogger('resize');

config = configparser.ConfigParser()
config.read('find-and-resize.ini')
basewidth = int(config['image']['basewidth'])


def resize_image(img_file, img_file_resized):
    # fullsized image
    img = Image.open(img_file)
    img_width, img_hsize = img.size

    # Skip if width is smaller or equal as basewidth
    if img_width <= basewidth:
        return logger.info('SKIP converting picture "%s"; img_width: %s' % (img_file, img_width))

    wpercent = (basewidth / float(img_width))
    hsize = int((float(img_hsize) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    logger.info('"%s" [RESIZE]-> "%s"' % (img_file, img_file_resized))
    img.save(img_file_resized)
    logger.info('Move "%s" -> "%s"' % (img_file_resized, img_file))
    shutil.move(img_file_resized, img_file)


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
                    resize_image(img_file, os.path.join(path_tmp, file))
            else:
                logger.info('Invalid "%s"' % os.path.join(path, file))


if __name__== "__main__":
    main()
