#!/usr/bin/env python3.6

from bs4 import BeautifulSoup
from os import rename, renames, remove
from os.path import exists
from shutil import rmtree
import subprocess

from config.app_config import *


# calls 'npm run build' from frontend React app directory
# moves and formats resulting build files to be accessible by Flask app
def rebuild_frontend():

    # call npm build from shell
    subprocess.call('npm run build', shell=True, cwd=FRONTEND_DIR)

    # directories that need to be deleted or moved
    build_dir = join(FRONTEND_DIR, 'build')
    new_build_dir = join(WORKING_DIRECTORY, 'static', 'build')
    media_dir = join(build_dir, 'static', 'media')
    new_media_dir = join(STATIC_DIR, 'media')
    new_index_html_path = join(WORKING_DIRECTORY, 'templates', 'index.html')

    # delete old index.html file if it exists
    if exists(new_index_html_path): remove(new_index_html_path)
    # move new index.html file to templates directory
    rename(join(build_dir, 'index.html'), new_index_html_path)
    # delete media (images) directory if it exists
    if exists(new_media_dir): rmtree(new_media_dir)
    # move new media directory inside static directory
    renames(media_dir, new_media_dir)
    # delete old build files if they exists
    if exists(new_build_dir): rmtree(new_build_dir)
    # move the rest of the build files
    renames(build_dir, new_build_dir)

    # open index.html with BeautifulSoup HTML parsing library
    with open(new_index_html_path, 'r+') as f:
        soup = BeautifulSoup(f)

        # change file paths in index.html to Jinja2 format so they're accessible by Flask app
        for element in soup.find_all(['link', 'script']):
            attribute = 'href' if element.name == 'link' else 'src'

            if element.has_attr(attribute):
                element[attribute] = "{{url_for('static',filename='build" + element[attribute] + "')}}"

        # save file
        f.seek(0)
        f.write(str(soup))
        f.truncate()