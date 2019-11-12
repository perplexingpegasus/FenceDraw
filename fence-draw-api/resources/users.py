#!/usr/bin/env python3.6

from flask import Blueprint, request
from flask_restful import Api, Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, User
from schema import UserSchema


# access individual users
class UserResource(Resource):

    # get user by username
    def get(self, username):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # deserialize user object into JSON
        return UserSchema(strict=True).dump(user).data

    # delete user by username
    def delete(self, username):

        # find user by username
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User {} does not exist".format(username), 400

        # delete all drawings associated with user
        for drawing in user.drawings:
            # delete all pages associated with drawing
            for page in drawing.pages:
                db.session.delete(page)
            db.session.delete(drawing)
        db.session.delete(user)
        db.session.commit()

        # send success response
        return "User was successfully deleted", 200


# access list of users
class UserListResource(Resource):

    # create new user
    def post(self):

        # validate initial post data
        try:
            data = UserSchema(strict=True).load(request.json).data
        except ValidationError:
            return "Incorrect parameters were passed", 400

        username = data['username']

        # try to create user
        try:
            user = User(**data)
            db.session.add(user)
            db.session.commit()

        # if user with username already exists, send 400 status error
        except IntegrityError:
            return "User {} already exists".format(username), 400

        # return success response and API endpoint to access user object
        return {'Location': '/api/v1/users/{}'.format(username)}, 201


# create API for user objects and register endpoints
users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(UserResource, '/api/v1/users/<username>', endpoint='user')
api.add_resource(UserListResource, '/api/v1/users', endpoint='users')