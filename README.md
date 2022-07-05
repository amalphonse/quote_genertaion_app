# Quote Generation App

## Getting Started

### Motivation

While creating my personal website i thought why not have quotes displayed on the page in a timed rotation, for which I built this quote generation API, with two tables created are: quotes and author details and I sued Auth0 for authentication and authorization: two roles created are: admin and public. This is phase 1 of my project I am looking to expand to more phases in future. 


This project demostrates skill in:
- Coding in Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet Protocols and Communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying Applications

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

Working within a virtual environment whenever using Python for projects, is recommended. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [PostgreSQL](https://www.postgresqltutorial.com/) is the database used in localhost and heroku cloud.

## Database Setup

Used insert_data.py to load the postgres SQL with data.

## Running the server

From within the directory first ensure you are working using your created virtual environment.

Note: The setup.sh doesn't contain the Auth0 tokens for privacy purpose.

To run the server, execute:

```bash
source setup.sh
flask run
```
The FLASK_ENV and FLASK_APP are set in the setup.sh file.
Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file to find the application. 


## API Reference

### Getting Started
- The app is hosted on herouku https://quote-generation-app.herokuapp.com/
- Authentication uses Auth0 authentication.

### Role Based Access - Roles defined are:

- Public
 `Can view quotes and author details`
 get:quotes, get:authordetails

- Admin
`All permissions the public has and`
`Add, modify or delete an quote from the database`
`Modify author details`
post:quotes, delete:quotes, patch:quotes, post:authordetails, get:quotes, get:authordetails

Token Type: Bearer

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: unauthorized
- 403: forbidden
- 404: Resource Not Found
- 422: unprocessable

### Endpoints 

#### GET '/quotes'
- General:
    - Fetches a list of quotes with their id, quote, author and auhtor details id.
    - Request Arguments: None
    - Returns a list of quotes with pagnination in groups of 10 along with number of total quotes, success.

    ```
    {
        "quotes": [
            {
                "author": "Dr APJ Abdul Kalam",
                "author_details_id": 1,
                "id": 1,
                "quote": "All Birds find shelter during rain. But Eagle avoids rain by flying above clouds."
            }
        ],
        "success": true,
        "total_quotes": 1
    }
    ```

#### GET '/quotes/1/authordetails'
- General:
    - Returns author details with pagnination in groups of 10 along with success.


```
{
    "author_details": [
        {
            "id": 1,
            "name": "Paulo Coelho",
            "birth_year": 1947,
            "career":"writer",
            "about":"The Alchemist"
        }
    ],
    "success": true,
}
```

#### POST '/quotes'
- General:
    - To create a new quote with quote, author and author details id,
    - Returns the success value and id of the created quotes. 

```
{
  "id": 5,
  "success": True
}
```

#### POST '/authordetails'
- General:
    - To create a new author details with name, birth year, career and about.
    - Returns the success value and id of the created author details. 

```
{
  "id": 4,
  "success": True
}
```

#### PATCH '/quotes/{id}'
- General:
    - Patch the quote of the given ID if it exists. 
    - Returns the id of the updated quote, success value.

```
{
  "success": True,
  "quote-updated": 1
}
```


#### DELETE '/quotes/{id}'
- General:
    - Deletes the quote of the given ID if it exists. 
    - Returns the id of the deleted quote, success value.
```
{
  "success": True,
  "deleted": 2
}
```



## Deployment
Deployed on heroku.

## Authors
Anju Mercian

## Run Database Migrations

Note: Use 'python3 manage.py db init' if you have two versions installed 

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

## Testing

Note: The owner is currently my personal account, the owner will need to be changed for the postgres sql.

To run the tests, while server is running run
```
source setup.sh
dropdb quotes_api
createdb quotes_api
python insert_data.py    #to add quotes to the db
python test_app.py
```