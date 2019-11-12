#!/usr/bin/env python3.6

from argparse import ArgumentParser
from flask import Flask, render_template
from flask_cors import CORS

from config.app_config import *
from models import db
from resources.drawings import drawings_api
from resources.fence_images import fence_blocks_api
from resources.pages import pages_api
from resources.users import users_api
from utils.frontend import rebuild_frontend
from utils.image_pipeline import register_images


# parses arguments from the command line
parser = ArgumentParser()
parser.add_argument('--host', type=str, default=HOST)               # host for application
parser.add_argument('--port', type=int, default=PORT)               # port for application
parser.add_argument('--user', type=str, default=USER)               # user for MySQL database
parser.add_argument('--password', type=str, default=PASSWORD)       # password for MySQL database
parser.add_argument('--dbhost', type=str, default=DB_HOST)          # host for MySQL database
parser.add_argument('--dbname', type=str, default=DB_NAME)          # database name
parser.add_argument('--mysql', action='store_true')                 # runs the app with a MySQL database, if not provided use SQLite
parser.add_argument('--rebuild', action='store_true')               # registers and new images (PDFs) and rebuilds the frontend of the app
args = parser.parse_args()

app = Flask(__name__)                # create Flask app
app.secret_key = SECRET_KEY          # configure app with secret key
CORS(app)                            # enable cross origin resource sharing

# register API endpoints with Flask app
app.register_blueprint(drawings_api)
app.register_blueprint(fence_blocks_api)
app.register_blueprint(pages_api)
app.register_blueprint(users_api)

# URI string for connection to MySQL database
db_uri = 'mysql://{}:{}@{}/{}'.format(
    args.user, args.password, args.dbhost, args.dbname) if args.mysql else 'sqlite:///' + args.dbname

# configure the Flask app with flask-sqlalchemy
db.app = app
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db.create_all()

# registers images and rebuilds the frontend files using npm build
if args.rebuild:
    register_images()
    rebuild_frontend()

# route to main page, renders index.html
@app.route('/')
def index():
    return render_template('index.html')

# runs the app if this script is called directly from the command line
if __name__ == '__main__':
    app.run(debug=DEBUG, host=args.host, port=args.port)