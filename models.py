import os
#from typing import Text
from sqlalchemy import Column, String, Integer, Text, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy.sql.sqltypes import Date

# for local variables
#database_name = "quotes_api"
#database_path = "postgresql://{}/{}".format('localhost:5432', database_name)

# for global variables
database_path = os.environ.get('DATABASE_URL')
print("Database path:")
print(database_path)
#if database_path.startswith("postgres://"):
    #database_path = database_path.replace("postgres://", "postgresql://", 1)
#database_path = 'postgresql://localhost:5432/quotes_api'
#print("Database path:")
#print(database_path)
#if database_path.startswith("postgres://"):
    #database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Quotes

'''


class Quotes(db.Model):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quote = Column(Text)
    author = Column(String)
    author_details_id = Column(Integer)
    #author_details_id = db.Column(db.Integer, db.ForeignKey('authordetails.id'), nullable=True)

    def __init__(self, quote, author, author_details_id):
        self.quote = quote
        self.author = author
        self.author_details_id = author_details_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'quote': self.quote,
            'author': self.author,
            'author_details_id': self.author_details_id
        }


'''
Author Details

'''


class authorDetails(db.Model):
    __tablename__ = 'authordetails'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_year = Column(Integer)
    career = Column(String)
    about = Column(Text)
    #quotes = db.relationship('Quotes', backref='author_details', lazy=True)

    def __init__(self, name, birth_year,career, about):
        self.name = name
        self.birth_year = birth_year
        self.career = career
        self.about = about
        #self.quotes = quotes

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'birth_year': self.birth_year,
            'career': self.career,
            'about': self.about
            #'quotes': self.quotes
        }
