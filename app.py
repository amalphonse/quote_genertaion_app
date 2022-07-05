import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, Quotes, authorDetails

PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # Pagination
    def paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * PER_PAGE
        end = start + PER_PAGE
        records = [records.format() for records in selection]
        current_records = records[start:end]
        return current_records

    '''
  Using after_request decorator to set Access-Control-Allow
  '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    @app.route('/', methods=['GET'])
    def get_init():
        return jsonify({
            'success': True,
            'message': "Quote Generation App. Default page."
        })


    '''
        Implemented GET requests for quotes,
        -GET '/quotes' including pagination (every 10 records).
        -This endpoint returns a list of quotes from the database and the
        number of total number of available quotes.
    '''

    @app.route('/quotes', methods=['GET'])
    @requires_auth(permission='get:quotes')
    def get_quotes(payload):
        selection = Quotes.query.order_by(Quotes.id).all()
        current_selection = paginate(request, selection)
        return jsonify({
            'success': True,
            'quotes': current_selection,
            'total_quotes': len(Quotes.query.all()),
        })


    '''
        Implemented POST requests for quotes,
        - POST /quotes
        - only admins can add quotes
        - This endpoint gets the json using get_json()
        - This endpoint returns the success and the id of the quote added.

  '''

    @app.route('/quotes', methods=['POST'])
    @requires_auth(permission='post:quotes')
    def create_quotes(payload):
        body = request.get_json()

        quote = body.get('quote', None)
        author = body.get('author', None)
        author_details_id = body.get('author_details_id', None)

        if quote is None:
            abort(422)
        if author is None:
            abort(422)
        if author_details_id is None:
            abort(422)
        try:
            new_quote = Quotes(quote=quote, author=author, author_details_id=author_details_id)
            new_quote.insert()
            return jsonify({
                'success': True,
                'quote_added': new_quote.id
            })
        except Exception as e:
            abort(422)

    '''
  Implemented PATCH requests for quotes,
  - PATCH '/quotes'.
  - only admin can patch quotes
  - This endpoint is to update an quote based on id.
  - This endpoint returns id of the updated actor and success.
  '''

    @app.route('/quotes/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:quotes')
    def update_quotes(payload, id):
        quote = Quotes.query.filter(Quotes.id == id).one_or_none()

        if quote is None:
            abort(404)
        body = request.get_json()
        if body is None:
            abort(422)
        try:
            if 'quote' in body:
                quote.quote = body['quote']
            if 'author' in body:
                quote.author = body['author']
            if 'author_details' in body:
                quote.author_details = body['author_details']
            quote.update()
            return jsonify({
                'success': True,
                'quote-updated': id
            })
        except Exception:
            abort(422)
    '''
  Implemented DELETE requests for quotes,
  - DELETE '/quotes'.
  - This endpoint is to delete an quote based on id.
  - This endpoint returns id of the deleted quote and success.
  - Access to this is only for admins
  '''

    @app.route('/quotes/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:quotes')
    def delete_actor(payload, id):
        quote = Quotes.query.filter(Quotes.id == id).one_or_none()

        if quote is None:
            abort(404)
        try:
            quote.delete()

            return jsonify({
                'success': True,
                'deleted-actor': quote.id
            })
        except Exception:
            abort(422)
    '''
    Get the author details based on the author details id from Quotes class
    '''

    @app.route('/quotes/<int:id>/authordetails',methods=['GET'])
    @requires_auth(permission='get:authordetails')
    def retrieve_author_details_by_quote(id):
        quote_id = Quotes.query.filter(Quotes.id==id).one_or_none()

        if quote_id is None:
            abort(400)
        selection=authorDetails.query.filter(authorDetails.id==quote_id.author_details_id).first()
        current = paginate(request, selection)

        return jsonify({
        'success':True,
        'author_details': current
        })

    '''
    Author Details API calls
    '''

    '''
    Implemented POST requests for author details,
    - POST /author_details
    - This is for admin use only
    - This endpoint gets the json using get_json()
    - This endpoint returns the success and the id of the author details added.

  '''

    @app.route('/authordetails', methods=['POST'])
    @requires_auth(permission='post:authordetails')
    def create_author_details(payload):
        try:
            body = request.get_json()

            name = body.get('name', None)
            birth_year = body.get('birth_year', None)
            career = body.get('career', None)
            about = body.get('about', None)

            if name is None:
                abort(422)

            new_author_details = authorDetails(name=name, birth_year=birth_year, career=career, about=about)

            new_author_details.insert()
            return jsonify({
                'success': True,
                'new-author-details-added': new_author_details.id
            })
        except Exception as e:
            abort(422)

    '''
    @Error Handlers:
    Created error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Permission not found"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)