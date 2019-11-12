#!/usr/bin/env python3.6

from datetime import date
from config.dimensions import *


# helper class for defining text, text styles and text box configuration
class TextConfig:

    def __init__(self,
        id, width, height, x_offset, y_offset,
        font_size, padding=3, bold=False, border=True, alignment='left',
        default_text=''):

        self.id = id
        self.width = width
        self.height = height
        self.x = x_margin + x_offset
        self.y = y_margin + y_offset
        self.font_size = font_size
        self.padding = padding
        self.bold = bold
        self.border = border
        self.font_weight = 'bold' if bold else 'normal'
        self.alignment = alignment
        self.default_text = default_text

    @property
    def formatted_text(self):
        return self.default_text.replace('\n', '<br/>')


# create TextConfig object for each text box on page
subcontractor1_config = TextConfig(
    id='subcontractor1',
    width=col3a_w,
    height=subcontractor_h,
    x_offset=col1_w + col2_w,
    y_offset=owner_h,
    font_size=10,
    alignment='left',
    default_text=
        'SUBCONTRACTOR\n'
        'ADDRESS:\n\n'
        'PHONE NO.:\n'
)

subcontractor2_config = TextConfig(
    id='subcontractor2',
    width=col3b_w,
    height=subcontractor_h,
    x_offset=col1_w + col2_w + col3a_w,
    y_offset=owner_h,
    font_size=10,
    alignment='right',
    default_text=
        '1775 ROUTE 25:\n'
        'P.O. BOX 430:\n'
        'RIDGE, NY 11961\n'
        '(631) 924-3011 FAX NO.: (631) 924-3275'
)

textarea_configs = []
def add_textarea(*args, **kwargs):
    textarea_configs.append(TextConfig(*args, **kwargs))

add_textarea(
    id='desc1',
    width=col1a_w,
    height=desc_h,
    x_offset=0,
    y_offset=0,
    font_size=10,
    default_text=
        'CHAIN LINK FABRIC:\n\n'
        'LINE/GATE/TERMINAL POSTS:\n\n'
        'TOP RAIL:\n'
        'BOTTOM TENSION WIRE:\n'
        'GATE AND BRACE:\n'
        'TIE WIRES:\n'
        'FITTINGS AND ACCESSORIES:\n\n'
        '*NOTE:'
)

add_textarea(
    id='desc2',
    width=col1b_w,
    height=desc_h,
    x_offset=col1a_w,
    y_offset=0,
    font_size=10
)


add_textarea(
    id='title',
    width=col1_w,
    height=title_h,
    x_offset=0,
    y_offset=desc_h,
    font_size=18,
    bold=True,
    alignment='center',
    default_text='{}’-0” HIGH CHAIN LINK FENCE'
)

add_textarea(
    id='date',
    width=col2_w,
    height=datescale_h,
    x_offset=col1_w,
    y_offset=0,
    font_size=14,
    alignment='center',
    default_text=date.today().strftime('%x')
),

add_textarea(
    id='scale',
    width=col2_w,
    height=datescale_h,
    x_offset=col1_w,
    y_offset=datescale_h,
    font_size=14,
    alignment='center',
    default_text='NTS'
)

add_textarea(
    id='contractor1',
    width=col3a_w,
    height=contractor_h,
    x_offset=col1_w + col2_w,
    y_offset=owner_h + subcontractor_h,
    font_size=10,
    default_text=
        'GENERAL CONTRACTOR:\n'
        'ADDRESS:\n\n'
        'PHONE #:'
)

add_textarea(
    id='contractor2',
    width=col3b_w,
    height=contractor_h,
    x_offset=col1_w + col2_w + col3a_w,
    y_offset=owner_h + subcontractor_h,
    font_size=10
)

add_textarea(
    id='owner1',
    width=col3a_w,
    height=owner_h,
    x_offset=col1_w + col2_w,
    y_offset=0,
    font_size=10,
    default_text=
        'OWNER:\n'
        'LOCATION:\n\n'
        'PROJECT NAME:\n\n'
        'CONSULTANT:\n'
        'PROJECT NO.:'
)

add_textarea(
    id='owner2',
    width=col3b_w,
    height=owner_h,
    x_offset=col1_w + col2_w + col3a_w,
    y_offset=0,
    font_size=10
)

# gets default page configuration for when a new page or drawing is created
def get_default_page_text(fence_height=6):
    page_dict = {config.id: config.default_text for config in textarea_configs}
    page_dict['title'] = page_dict['title'].format(fence_height)
    return page_dict