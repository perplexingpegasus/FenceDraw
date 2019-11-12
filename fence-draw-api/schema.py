#!/usr/bin/env python3.6

from marshmallow import fields, post_dump, post_load, pre_dump, pre_load, Schema, ValidationError
from config.text_config import get_default_page_text


# makes sure validation will fail if 'None' type object is passed in
class CustomValidator:

    @pre_load(pass_many=True)
    @post_dump(pass_many=True)
    def raise_error_if_none(self, data, many):
        if data is None:
            raise ValidationError('data cannot be None')


# validates data for page objects
class PageSchema(Schema, CustomValidator):
    title = fields.String(required=True)
    desc1 = fields.String(required=True)
    desc2 = fields.String(required=True)
    date = fields.String(required=True)
    scale = fields.String(required=True)
    contractor1 = fields.String(required=True)
    contractor2 = fields.String(required=True)
    owner1 = fields.String(required=True)
    owner2 = fields.String(required=True)
    fence_image_id = fields.Integer()

    # creates default page if no data is passed in (used when adding new page to drawing after POST request)
    @pre_load
    def create_default_page(self, data):
        if not 'new_page' in data:
            raise ValidationError('"new_page" attribute is missing')
        if data['new_page']:
            data = get_default_page_text(6)
        else:
            del data['new_page']
        return data

    # change key for fence image ID before deserializing to JSON
    @post_dump
    def change_fence_img_attr(self, data):
        if 'fence_image_id' in data:
            data['fenceImgId'] = data.pop('fence_image_id')
        else:
            data['fenceImgId'] = None
        return data


# validates data for drawing objects
class DrawingSchema(Schema, CustomValidator):
    filename = fields.String(required=True)
    n_pages = fields.Int(required=True, dump_only=True)

    # get attribute with number of pages before deserializing object
    @pre_dump(pass_many=True)
    def get_n_pages(self, data, many):
        _get_n_pages = lambda drawing: {'filename': drawing.filename, 'n_pages': len(drawing.pages)}
        if many:
            return [_get_n_pages(drawing) for drawing in data]
        else:
            return _get_n_pages(data)

    # creates are returns page with default attributes when new drawing is created in POST request
    @post_load
    def append_default_page(self, data):
        new_page_data = get_default_page_text(6)
        return data, new_page_data


# validates data for user objects
class UserSchema(Schema, CustomValidator):
    username = fields.String(required=True)


# validates data for fence image objects
class FenceImageSchema(Schema):
    id = fields.Integer(required=True, dump_only=True)
    filename = fields.String(required=True, dump_only=True)
    name = fields.String(required=True, dump_only=True)
    category = fields.String(required=True, dump_only=True)
    height = fields.Float(required=True, dump_only=True)

    # get distinct values of fields 'category' and 'height' for creating dropdown menus in frontend
    @post_dump(pass_many=True)
    def get_distincts(self, data, many):
        if many:
            data = dict(fenceImgs=data)
            data['uniqueCategories'] = sorted(list(set([img['category'] for img in data['fenceImgs']])))
            data['uniqueHeights'] = sorted(list(set([img['height'] for img in data['fenceImgs']])))
        return data