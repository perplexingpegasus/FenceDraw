#!/usr/bin/env python3.6

from io import BytesIO
from os.path import join
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab import platypus, rl_config
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

from config.app_config import PDF_DIR, FONT_DIR, WORKING_DIRECTORY
from config.dimensions import *
from config.text_config import subcontractor1_config, subcontractor2_config, textarea_configs


# register fonts with report lab
rl_config.TTFSearchPath.clear()
rl_config.TTFSearchPath.append(FONT_DIR)
registerFont(TTFont('Arial', 'Arial.ttf'))
registerFont(TTFont('ArialBd', 'ArialBd.ttf'))

# open logo image
logo_img = Image.open(join(WORKING_DIRECTORY, 'static', 'logo.png'))


# function for creating report lab ParagraphStyle objects used to style text boxes in PDF
def get_paragraph_style(font_size, bold=False, alignment='left'):
    if alignment == 'left':
        alignment = 0
    elif alignment == 'center':
        alignment = 1
    else:
        alignment = 2
    return ParagraphStyle(
        name='Normal', fontName='ArialBd' if bold else 'Arial', fontSize=font_size, leading=font_size * 1.2,
        alignment=alignment)

# position and crop PDF of fence image on the page based on available height (dynamic) and available width (static)
def get_scale_and_offset(fence_image, max_height):

    # width and height of cropped fence image PDF
    crop_width = fence_image.image_width - fence_image.left_space - fence_image.right_space
    crop_height = fence_image.image_height - fence_image.top_space - fence_image.bottom_space

    border_aspect_ratio = border_width / max_height        # aspect ratio of available space for positioning image
    image_aspect_ratio = crop_width / crop_height          # aspect ratio of cropped PDF image

    x_offset = x_margin                                    # left offset of space available for image on page
    y_offset = y_margin + border_height - max_height       # bottom offset of space available for image on page

    if image_aspect_ratio > border_aspect_ratio:              # image upsizing is limited by width
        scale = border_width / crop_width                     # expansion factor
        y_offset += (max_height - crop_height * scale) / 2    # center image vertically

    else:                                                     # image upsizing is limited by height
        scale = max_height / crop_height                      # expansion factor
        x_offset += (border_width - crop_width * scale) / 2   # center image horizontally

    # subtract crop margins from image placement
    x_offset -= fence_image.left_space * scale
    y_offset -= fence_image.bottom_space * scale

    return scale, round(x_offset), round(y_offset)

# add text data from page object onto PDF canvas
def add_page_data(canvas, page):

    # create dictionary containing names, styles and text data for text boxes to be drawn on page
    paragraphs = {
        config.id: PdfParagraph(canvas, text=getattr(page, config.id), **config.__dict__)
        for config in textarea_configs}

    # add static text boxes (not pulled from page object) to dictionary
    paragraphs.update({
        config.id: PdfParagraph(canvas, text=config.default_text, **config.__dict__)
        for config in (subcontractor1_config, subcontractor2_config)})

    # get necessary height for each text box
    heights = {id: paragraph.height for id, paragraph in paragraphs.items()}

    # draw border
    canvas.setStrokeColorRGB(0, 0, 0)
    canvas.setFillColorRGB(1, 1, 1)
    canvas.rect(x_margin, y_margin, border_width, border_height)

    # add text boxes for image description and title
    h1 = max(heights['desc1'], heights['desc2'])
    paragraphs['title'].paste(y=h1)
    paragraphs['desc1'].paste(height=h1)
    paragraphs['desc2'].paste(height=h1)

    # add text boxes for central column (date and scale)
    h2 = heights['date']
    paragraphs['scale'].paste(y=h2)
    paragraphs['date'].paste()

    # add text boxes for rightmost column (owner, contractor, subcontractor)

    # bottom row
    h3 = max(heights['owner1'], heights['owner2'])
    paragraphs['owner1'].paste(height=h3)
    paragraphs['owner2'].paste(height=h3)

    # middle row
    h4 = max(heights['subcontractor1'], heights['subcontractor2'])
    paragraphs['subcontractor1'].paste(y=h3, height=h4)
    paragraphs['subcontractor2'].paste(y=h3, height=h4)

    # position and insert logo image
    logo_y = logo_y_offset + h3 + y_margin
    img_io = BytesIO()
    logo_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    img_reader = ImageReader(img_io)
    canvas.drawImage(img_reader, logo_x, logo_y, logo_w, logo_h)

    # top row
    h5 = max(heights['contractor1'], heights['contractor2'])
    paragraphs['contractor1'].paste(y=h3 + h4, height=h5)
    paragraphs['contractor2'].paste(y=h3 + h4, height=h5)

    # available height space for placing image
    available_space = border_height - max(
        h1 + heights['title'],
        h2 + heights['scale'],
        h3 + h4 + h5)

    # save data on current page and open next page for editing
    canvas.showPage()

    # return available height space for use in positioning image
    return available_space


# contains all attributes for styling and positioning text boxes with dynamic height adjustment
class PdfParagraph:
    def __init__(self,
        canvas, x, y, width,
        font_size, padding=3, alignment='left', bold=False, border=True,
        text='', *args, **kwargs
    ):

        self.canvas = canvas      # Canvas object onto which the paragraph is drawn
        self.x = x                # x position on canvas
        self.y = y                # initial y position on canvas (can be changed when text box is pasted on canvas)
        self.width = width        # fixed width of text box
        self.padding = padding
        self.border = border
        self.report_lab_style = get_paragraph_style(font_size, bold, alignment)
        self.text = text

    # get styled paragraph object
    @property
    def paragraph(self):
        return platypus.Paragraph(self._text, self.report_lab_style)

    # get text
    @property
    def text(self):
        return self._text

    # set text (new lines must be replaced by break tags)
    # minimum height requirements also calculated when text is set
    @text.setter
    def text(self, new_text):
        new_text = new_text.replace('\n', '<br/>')
        self._text = new_text

        offset = self.padding * 2
        paragraph = self.paragraph
        _, height = paragraph.wrap(self.width - offset, 0)
        self.height = height + offset

    # paste page on canvas at position (x, y)
    # if 'height' is None, paragraph height is set as minimum height
    def paste(self, x=None, y=None, height=None):
        if x is None: x = self.x
        else: x += x_margin

        if y is None: y = self.y
        else: y += y_margin

        paragraph = self.paragraph
        if height is None:
            height = self.height

        # paragraph must be wrapped in Frame object before pasting
        frame = platypus.Frame(x, y, self.width, height, showBoundary=self.border, leftPadding=self.padding,
            rightPadding=self.padding, topPadding=self.padding, bottomPadding=self.padding)
        frame.addFromList([paragraph], self.canvas)


# main function for creating PDF from drawing objects
def make_pdf(drawing):

    # initialize bytes stream and associate Canvas object with it
    pdf_io = BytesIO()
    canvas = Canvas(pdf_io, (total_width, total_height))

    # get list of pages associated with drawing object
    pages = drawing.pages

    max_img_heights = []
    for page in pages:
        available_space = add_page_data(canvas, page)    # add text data from each page object to page on canvas
        max_img_heights.append(available_space)          # append available height space for each page

    # save Canvas object to 'pdf_io' bytes stream
    # 'pdf_io' now contains PDF document with text boxes and no images
    canvas.save()
    pdf_io.seek(0)

    # this part uses the PyPDF2 library to merge PDF's of fence images onto the pages of the PDF document

    # open PDF file in bytes stream with PdfFileReader
    reader = PdfFileReader(pdf_io)
    # open PdfFileWriter object to hold final PDF document
    writer = PdfFileWriter()

    # hold list of PDF fence image files that need to be closed after merging operation is complete
    files_to_close = []
    for pdf_page, page_row, max_height in zip(reader.pages, pages, max_img_heights):

        # get fence image object from database linked by page object
        fence_img_row = page_row.fence_image
        if fence_img_row is not None:

            # open fence image PDF from filename attribute of fence image object
            fence_img_filename = join(PDF_DIR, fence_img_row.filename + '.pdf')
            fence_img_pdf_file = open(fence_img_filename, 'rb')
            fence_img_pdf_page = PdfFileReader(fence_img_pdf_file).pages[0]

            # merge fence image PDF onto page of PDF with text boxes
            # calculate space requirements and position
            pdf_page.mergeScaledTranslatedPage(fence_img_pdf_page, *get_scale_and_offset(fence_img_row, max_height))
            files_to_close.append(fence_img_pdf_file)

        # append page to PdfFileWriter
        writer.addPage(pdf_page)

    # we're done with the old bytes stream
    # new bytes stream object onto which PdfFileWriter writes its pages
    pdf_io = BytesIO()
    writer.write(pdf_io)
    pdf_io.seek(0)

    # get string from bytes stream and close the object for writing
    pdf = pdf_io.getvalue()
    pdf_io.close()

    # close all fence image PDF files opened during this operation
    for f in files_to_close: f.close()

    # return string form of PDF file
    return pdf