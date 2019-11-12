#!/usr/bin/env python3.6

from flask import Blueprint, request, Response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import db, Drawing, Page, User
from pdf_rendering import make_pdf
from schema import DrawingSchema


# access individual drawings
class DrawingResource(Resource):

    # get drawing from username and filename
    def get(self, username, filename):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing with filename from drawings belonging to user
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # deserialize drawing object into JSON
        return DrawingSchema(strict=True).dump(drawing).data


    # delete drawing from username and filename
    def delete(self, username, filename):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing with filename from drawings belonging to user
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        # delete all pages belonging to drawing
        for page in drawing.pages:
            db.session.delete(page)

        # delete drawing
        db.session.delete(drawing)
        db.session.commit()

        # send success response
        return "Drawing was successfully deleted", 200


# access list of drawings for a given user
class DrawingListResource(Resource):

    # get drawing list by username
    def get(self, username):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # deserialize list of drawing objects to JSON
        return DrawingSchema(strict=True, many=True).dump(user.drawings).data

    # create new drawing associated with user by username
    def post(self, username):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # validate initial post data
        try:
            drawing_data, page_data = DrawingSchema(strict=True).load(request.json).data
        except ValidationError:
            return "Incorrect parameters were passed", 400

        # create drawing with post data and user object
        drawing = Drawing(user=user, **drawing_data)
        Page(drawing=drawing, **page_data)
        db.session.commit()

        # return success response and API endpoint to access drawing object
        return {'Location': '/api/v1/users/{}/drawings/{}'.format(username, drawing_data['filename'])}, 201


# access PDF's created from drawing objects
class PdfResource(Resource):

    # get PDF of drawing by username and filename
    def get(self, username, filename):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # find drawing with filename from drawings belonging to user
        drawing = Drawing.query.with_parent(user).filter_by(filename=filename).first()
        if drawing is None:
            return "Drawing {} with user {} does not exist".format(filename, username), 400

        try:
            pdf = make_pdf(drawing)       # use drawing object to create PDF written to bytes stream
            response = Response(pdf)      # create Response object from bytes stream

            # insert metadata (filename and file type) into response
            response.headers['Content-Disposition'] = "inline; filename={}.pdf".format(filename)
            response.mimetype = 'application/pdf'

        # report errors when making PDF
        except Exception as e:
            print(e)
            return "Error when creating PDF: {}".format(e), 400

        # return file download response
        return response


# create API for drawing objects and register endpoints
drawings_api = Blueprint('resources.drawings', __name__)
api = Api(drawings_api)
api.add_resource(DrawingResource, '/api/v1/users/<username>/drawings/<filename>', endpoint='drawing')
api.add_resource(DrawingListResource, '/api/v1/users/<username>/drawings', endpoint='drawings')
api.add_resource(PdfResource, '/api/v1/users/<username>/drawings/<filename>/pdf', endpoint='pdf')