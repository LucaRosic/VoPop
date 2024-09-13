# Backend Documentation

## Setup

**Note: make sure you're in the VoPop directory before you start**

Before running the backend server, install dependencies by creating a virtual environment:

- python -m venv .venv

Activate it:

- (Unix/Mac) source .venv/bin/activate
- (Windows) .\.venv\Scripts\activate

Then install the dependencies needed to run the backend:

- pip install -r backend/requirements.txt

## Start up Backend Server

To start the backend server all you need to do is:

- cd backend
- python manage.py runserver

If the server is running correctly you should see:<br>

"Django version 4.2.14, using settings 'backend.settings'<br>
Starting development server at http://127.0.0.1:8000/ <br>
Quit the server with CONTROL-C."

To access the backend server enter http://127.0.0.1:8000/ into your browser.

## File structure

There are many files within the backend folder. The main files to observe are:

- api
  - models.py: ORM Schema for the database
  - serializer.py: Specifies the structure of data exchanged between frontend and backend
  - views.py: Contains the implementated of API endpoints
  - urls.py: Maps URLs to the APIs.
- backend
  - settings.py: Contains settings for the backend server (e.g. connection to database)
  - urls.py: more mappings of URLs to the APIs (register, login and logout request)

## APIs

All the apis implemented into the Vopop backend.

**Note: All APIs require user authentication.**

### Authentication APIs

- POST api/user/register/ (CreateUserView)
  - registers a user
- POST api/token/
  - log a user in
- POST api/token/refresh/
  - refreshes a users login token if it has expired
- POST api/logout/
  - logs a user out

### Data APIs

- /admin
  - access and manage users and data in the connected database
- POST api/product/ (CreateProduct)
  - Takes a url link, processes it and stores all data in the database
  - If link is valid, GETs data to make 'product card'
  - Expects data in JSON format
- GET api/product/home/ (GetUserProduct_Home)
  - Retrieves all the users 'product card' data (name, average sentiment, overview, etc) aka all data needed for home page
- GET api/product/dashboard/sentiment/product_id/ (GetReviewSent_Dash)
  - Retrieves all reviews sentiment data (data and sentiment label) for a specified product
- GET api/product/dashboard/meta/product_id/ (GetProductMeta_Dash)
  - Retrieves the meta data of the specified product (name, brand, etc)
- GET api/product/dashboard/summ/product_id/ (GetProductSum_Dash)
  - Retrieves the summary data of product (summary, average rating, date, etc) for a specfied product
- DELETE api/product/delete/product_id/ (ProductDelete)
  - Stops the user tracking the specified product
  - Also deletes all data related to a product (meta, summary and reviews) if no user is currently tracking the product.
