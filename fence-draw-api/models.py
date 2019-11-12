#!/usr/bin/env python3.6

from flask_sqlalchemy import SQLAlchemy


# database object used by API resources
db = SQLAlchemy()


# define database schema

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)


class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # allow User objects to access list of associated drawings with user.drawings
    user = db.relationship('User', backref=db.backref('drawings', lazy=True))


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # various text fields used in contructing PDF
    title = db.Column(db.String)
    desc1 = db.Column(db.String)
    desc2 = db.Column(db.String)
    date = db.Column(db.String)
    scale = db.Column(db.String)
    contractor1 = db.Column(db.String)
    contractor2 = db.Column(db.String)
    owner1 = db.Column(db.String)
    owner2 = db.Column(db.String)

    # fence image contained on page
    fence_image_id = db.Column(db.Integer, db.ForeignKey('fence_image.id'))
    fence_image = db.relationship('FenceImage')

    drawing_id = db.Column(db.Integer, db.ForeignKey('drawing.id'), nullable=False)
    # allow Drawing objects to access list of associated pages with drawing.pages
    drawing = db.relationship('Drawing', backref=db.backref('pages', lazy=True))


class FenceImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)                 # image category (fence, gate, etc.)
    height = db.Column(db.Float, nullable=False)                         # height of fence (4FT, 6FT, etc.)

    image_width = db.Column(db.Integer, nullable=False)
    image_height = db.Column(db.Integer, nullable=False)
    left_space = db.Column(db.Integer, nullable=False)
    top_space = db.Column(db.Integer, nullable=False)
    right_space = db.Column(db.Integer, nullable=False)
    bottom_space = db.Column(db.Integer, nullable=False)

    # page = db.relationship('Page', backref=db.backref('fence_image'))