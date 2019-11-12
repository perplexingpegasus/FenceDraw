#!/usr/bin/env python3.6

'''
dimensions of text boxes in pt
'''

total_width = 1224
total_height = 792
x_margin = 36
y_margin = 18
border_width = total_width - 2 * x_margin
border_height = total_height - 2 * y_margin

col1a_w = 156
col1b_w = 490
col1_w = col1a_w + col1b_w
col2_w = 164
col3a_w = 142
col3b_w = 200
col3_w = col3a_w + col3b_w
sheet_num_w = 200

desc_h = 160
title_h = 32
datescale_h = 28
owner_h = 100
subcontractor_h = 54
contractor_h = 60
sheet_num_h = 32

logo_x = x_margin + col1_w + col2_w + col3a_w + 6
logo_y_offset = 18
logo_y = y_margin + owner_h + logo_y_offset
logo_w = 82
logo_h = 36

img_container_y_offset = max(desc_h + title_h, datescale_h, logo_h + contractor_h + owner_h)
img_container_y = y_margin + img_container_y_offset
img_container_h = border_height - sheet_num_h - img_container_y

pdf_img_h = 576
pdf_img_y = total_height - pdf_img_h - 8