#!/usr/bin/env python3.6

from base64 import b64encode
from flask import Blueprint
from flask_restful import Api, Resource
from io import BytesIO

from models import FenceImage
from schema import FenceImageSchema


# class FenceImages(Resource):
#
#     def get(self, id):
#         fence_image = FenceImage.query.filter_by(id=id).first()
#         if fence_image is None:
#             return "Fence image with id {} does not exist".format(id), 400
#
#         try:
#             img_io = BytesIO()


# access list of fence images
class FenceImageListResource(Resource):

    # get fence image list
    def get(self):
        data = FenceImageSchema(strict=True, many=True).dump(FenceImage.query.all()).data
        return data


# create API for fence image objects and register endpoints
fence_blocks_api = Blueprint('resources.fence_blocks', __name__)
api = Api(fence_blocks_api)
# api.add_resource(FenceImages, '/api/v1/fence_images/<id>', endpoint='images')
api.add_resource(FenceImageListResource, '/api/v1/fence_images', endpoint='images')