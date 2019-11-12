#!/usr/bin/env python3.6

from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import db, Drawing, Page, User
from schema import PageSchema


# access individual pages
class PageResource(Resource):

    # get page by username, drawing filename and page number
    def get(self, username, filename, page_number):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing by filename
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # find page by page number
        try:
            page = drawing.pages[page_number - 1]
        except IndexError:
            return "Page {} on drawing {} with user {} does not exist".format(page_number, filename, username), 400

        # deserialize page object into JSON
        return PageSchema(strict=True).dump(page).data

    # update page data by username, drawing filename and page number
    def put(self, username, filename, page_number):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing by filename
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # find page by page number
        try:
            page = drawing.pages[page_number - 1]
        except IndexError:
            return "Page {} on drawing {} with user {} does not exist".format(page_number, filename, username), 400

        # validate UPDATE post data
        try:
            data = PageSchema(strict=True).load(request.json).data
        except ValidationError:
            return "Incorrect parameters were passed", 400

        # update attributes on page object
        for k, v in data.items():
            setattr(page, k, v)
        db.session.commit()

        # return success response
        return "Page was successfully updated".format(page_number), 200

    # delete page data by username, drawing filename and page number
    def delete(self, username, filename, page_number):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing by filename
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # find page by page number
        try:
            page = drawing.pages[page_number - 1]
        except IndexError:
            return "Page {} on drawing {} with user {} does not exist".format(page_number, filename, username), 400

        # delete page
        db.session.delete(page)
        db.session.commit()

        # return success response
        return "Page was successfully deleted".format(page_number), 200


# access list of pages for given user and drawing
class PageListResource(Resource):

    # create new page associated with user by username
    def post(self, username, filename):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing by filename
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # validate initial post data
        try:
            page_data = PageSchema(strict=True).load(request.json).data
        except ValidationError:
            return "Incorrect parameters were passed", 400

        # create page
        Page(drawing=drawing, **page_data)
        db.session.commit()
        page_number = len(drawing.pages)

        # return success response and API endpoint to access page object
        return {'Location': '/api/v1/users/{}/drawings/{}/pages/{}'.format(username, filename, page_number),
                'page_number': page_number}, 201


# create API for page objects and register endpoints
pages_api = Blueprint('resources.pages', __name__)
api = Api(pages_api)
api.add_resource(PageResource, '/api/v1/users/<username>/drawings/<filename>/pages/<int:page_number>', endpoint='page')
api.add_resource(PageListResource, '/api/v1/users/<username>/drawings/<filename>/pages', endpoint='pages')