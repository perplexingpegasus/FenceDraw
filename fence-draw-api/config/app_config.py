#!/usr/bin/env python3.6

from os import pardir, sep
from os.path import dirname, join, normpath, realpath


# default configuration parameters for Flask app
HOST = '127.0.0.1' # '64.207.183.212'
PORT = 5000
DEBUG = True
SECRET_KEY = 'dsjbaidsuvbasc0u8y04387qb8)&F&*^F&903f2yv0fvter'

# default configuration parameters for MySQL database
USER = 'fence-draw'
PASSWORD = 'g?4Ed05k'
DB_HOST = '127.0.0.1'
DB_NAME = 'fence-draw.db'

# define file paths to avoid FileNotFoundError, OSError, etc.
WORKING_DIRECTORY = dirname(realpath(__file__))
BACK_DIRECTORY = normpath(WORKING_DIRECTORY + sep + pardir)
FRONTEND_DIR = join(BACK_DIRECTORY, 'fence-draw-frontend')
STATIC_DIR = join(WORKING_DIRECTORY, 'static')
IMG_DIR = join(FRONTEND_DIR, 'src', 'images')
PDF_DIR = join(STATIC_DIR, 'pdfs')
FONT_DIR = join(STATIC_DIR, 'fonts')