#!/usr/bin/env python3.6

"""

 //////////////     Fence PDF-Image Pipeline

Reads PDF files from static/pdfs, adds their relevant attributes to the database and creates JPGs used by the frontend

Before adding a fence image, the image and filename must be processed as described in README.md

"""


from os import listdir
from pdf2image import convert_from_path
import numpy as np

from config.app_config import *
from models import db, FenceImage


# determines where to crop the image based on empty space
# 'spacing' parameter determines how many pixels of whitespace to pad the actual image with
def get_crop_window(img, spacing=10):
    img_array = np.asarray(img)                               # convert to numpy array
    h, w, c = img_array.shape                                 # height, width, channels (RBG or RGBA)
    vertical_blank = np.ones([h, c], np.uint8) * 255          # vertical bar of image whitespace
    horizontal_blank = np.ones([w, c], np.uint8) * 255        # horizontal bar of image whitespace

    # calculates the maximum padding (whitespace) from the top, left, right or bottom of an image
    def get_space(horizontal, reverse):
        dim, blank = (h, horizontal_blank) if horizontal else (w, vertical_blank)
        indices = range(dim)
        if reverse: indices = reversed(indices)

        for i in indices:
            section = img_array[i] if horizontal else w
            if not np.all(section == blank):

                if reverse:
                    return min(i + 1 + spacing, dim)
                else:
                    return max(i - spacing, 0)

        return dim

    left = get_space(False, False)
    top = get_space(True, False)
    right = get_space(False, True)
    bottom = get_space(True, True)

    return [left, top, right, bottom]

# extract height, category and name attributes from PDF filename
def parse_filename(filename):
    substrings = filename.split('_')
    height = float(substrings[0])
    category = substrings[1]
    name = ' '.join(substrings[2:]).upper()
    return height, category, name

# convert PDFs to JPGS (stored in frontend directory) and register image attributes in database
def register_images():

    # get filenames and filter for files not already in the database
    new_filenames = {f[:-4] for f in listdir(PDF_DIR) if f.endswith('.pdf')}
    registered_filenames = set([fence_img.filename for fence_img in FenceImage.query.all()])
    new_filenames = list(new_filenames - registered_filenames)

    for filename in new_filenames:

        # throws an error and moves to next file if filename can't be parsed
        try:
            height, category, name = parse_filename(filename)
        except (IndexError, ValueError):
            print('cannot parse filename: {}.pdf'.format(filename))
            continue

        img = convert_from_path(join(PDF_DIR, filename + '.pdf'), dpi=144)[0]  # convert PDF to JPG (2 pixels per point)
        image_width, image_height = img.size                                   # get height, width of JPG
        crop_window = get_crop_window(img)                                     # get crop window by measuring whitespace
        img = img.crop(crop_window)                                            # crop JPG

        # create FenceImage row and add to database
        # there are 2 pixels per point, so pixel dimensions are divided by 2
        fence_img = FenceImage(
            filename=filename,
            name=name,
            height=height,
            category=category,
            image_width=image_width // 2,
            image_height=image_height // 2,
            left_space=crop_window[0] // 2,
            top_space=crop_window[1] // 2,
            right_space=(image_width - crop_window[2]) // 2,
            bottom_space=(image_height - crop_window[3]) // 2
        )
        db.session.add(fence_img)
        db.session.commit()

        # save JPG in image directory
        img.save(join(IMG_DIR, str(fence_img.id) + '.jpg'))

        print('registered image: {}, category: {}, height: {}'.format(name, category, height))

# removes all fence image data from the database
def purge_images():
    fence_images = FenceImage.query.all()
    for fence_image in fence_images:
        db.session.delete(fence_image)
        db.session.commit()