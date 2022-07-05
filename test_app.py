import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Quotes, authorDetails


class QuoteGenerationAppTestCase(unittest.TestCase):
    """This class represents the Quote Generation App test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        admin_token = os.environ.get('admin_token')
        public_token = os.environ.get('public_token')
        

        self.admin_auth_header = {'Authorization':
                                        'Bearer ' + admin_token}
        self.public_auth_header = {'Authorization':
                                          'Bearer ' + public_token}
        

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "quotes_api"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        '''
        Test data for Quotes and Author Details
        Roles: admin and public
        '''

        self.new_quote1 = {
            'quote': 'All Birds find shelter during rain. But Eagle avoids rain by flying above clouds.',
            'author': 'Dr APJ Abdul Kalam',
            'author_details_id': 1
        }

        self.new_quote2 = {
            'quote': 'Don’t take rest after your first victory because if you fail in second, more lips are waiting to say that your first victory was just luck.',
            'author': 'Dr APJ Abdul Kalam',
            'author_details_id': 1
        }

        self.new_quote3 = {
            'quote': 'All of us do not have equal talent. But, all of us have an equal opportunity to develop our talents.',
            'author': 'Dr APJ Abdul Kalam'
        }

        self.new_author_details = {
            'name': 'Dr APJ Abdul Kalam',
            'birth_year': 1931,
            'career': 'Former President of India' ,
            'about': "Dr APJ Abdul Kalam, popularly known as the Missile Man of India, was a source of inspiration for tens and thousands of Indians."
            }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Tests:
        One test for success behavior of each endpoint
        One test for error behavior of each endpoint
        At least two tests for RBAC 
    """
    # Test cases for Quotes end points.
    # testing public and admin RBAC along with get quotes.

    def test_get_quotes(self):
        res = self.client().get('/quotes?page=1',
                                headers=self.public_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['quotes']) > 0)


    # testing post for quotes
    def test_post_quotes(self):
        res = self.client().post('/quotes',
                                 json=self.new_quote1,
                                 headers=self.admin_auth_header)
        data = json.loads(res.data)
        quote = Quotes.query.filter_by(id=data['quote_added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(quote)

    def test_post_quotes1(self):
        res = self.client().post('/quotes',
                                 json=self.new_quote2,
                                 headers=self.admin_auth_header)
        data = json.loads(res.data)
        quote = Quotes.query.filter_by(id=data['quote_added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(quote)
    
    #testing adding author details
    def test_post_authordetails(self):
        res = self.client().post('/authordetails',
                                 json=self.new_author_details,
                                 headers=self.admin_auth_header)
        data = json.loads(res.data)
        authordetails = authorDetails.query.filter_by(id=data['new-author-details-added']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(authordetails)

    # testing negative case for post quote
    def test_post_quote_422_missing_authordetails(self):
        res = self.client().post('/quotes',
                                 json=self.new_quote3,
                                 headers=self.admin_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # testing RBAC - without authorization -  should result negative
    def test_without_auth(self):
        res = self.client().get('/quotes?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    # testing RBAC - testing casting director deleting a movie should result
    # negative
    def test_wrong_auth(self):
        res = self.client().delete('/quotes/1',
                                   headers=self.public_auth_header)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
