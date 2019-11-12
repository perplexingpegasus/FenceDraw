# FENCE-DRAW

Web application for creating fence blueprint PDF's from text input and selected images

## Running the application

cd to the fence-draw-api directory and run 'python app.py'

The following flagged arguments may be passed in when running app.py:

'--host={ }'       host for Flask application

'--port={ }'       port for Flask application

'--mysql'          run the app configured with a MySQL database if this flag is used, if not then use SQLite

'--user={ }'       user for MySQL database

'--password={ }'   password for MySQL database

'--dbhost={ }'     host for MySQL database

'--dbname={ }'     database name

'--rebuild'        register new images and rebuild the React frontend (use if changes were made to frontend or new fence
image PDF's were added)

## Application structure

### fence-draw-frontend/

React code used for maintaining frontend

### fence-draw-api/

**config/**

--- *app_config.py*: default configuration for Flask app and database, absolute filepath strings

--- *dimensions.py*: dimensions (in pt) of text boxes and other parameters on PDF documents

--- *text_config.py*: default configurations for text boxes, helper class for storing the configuration and function for 
    creating default page
    
**resources/**

--- *drawings.py*: defines API endpoints for drawing objects, which are used to create multi-page PDF's

--- *fence_images.py*: defines API endpoints for accessing data about fence images

--- *pages.py*: defines API endpoints for page objects, which store data for individual PDF pages

--- *users.py*: defines API endpoints for users logins

**static/**

stores files created by 'npm run build', PDF's, image files, CSS and javascript

**templates/**

--- *index.html*: HTML file used by Flask app as starting point for frontend interface

**utils.py/**

--- *frontend.py*: utility for rebuilding React frontend from fence-draw-frontend directory and moving build files so 
they can be run by the Flask app

--- *image_pipeline.py*: utility for processing new fence image PDF's that have been placed in the static/pdfs directory

*app.py*: main file for running application, should be called from command line

*models.py*: defines database schema and creates global connection to database used by other scripts

*pdf_rendering.py*: utilities for creating PDF files from page and drawing objects in database and fence image PDF's

*schema.py*: validator classes for sending and receiving requests between API and frontend

## Adding new fence images

To add a new fence image to the application, insert a PDF file of the fence image into the static/pdfs directory. The
application automatically calculates cropping and spacing of the image, so this is not important when creating the 
initial fence image PDF file.

A fence image PDF should have the a filename in the format '{height}\_{category}\_{name}.pdf', which is parsed by the
application.

For example, '4_fence_top_rail_bottom_rail_1.pdf' is registered in the database as a fence image with height 4FT,
category 'fence' and name 'TOP RAIL BOTTOM RAIL 1'.

All fence image PDF's should be processed with Adobe Illustrator in order to make sure textures behave correctly when 
creating blueprint PDF's.

First, open the PDF in Adobe Illustrator. Then for each texture in the PDF (these are typically the chain mesh images) 
select the texture and go to Object > Expand at the top menu. Make sure 'Fill' is checked in the pop up window, and 
click 'OK'. Finally, save the PDF.

If new fence images have been added, the '--rebuild' flag must be used when starting the application again in order for
the application to add them to the database.