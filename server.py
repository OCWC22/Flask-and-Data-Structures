from calendar import c
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
#import event and engine to enforce foreign key constraints
from sqlalchemy import event
from sqlalchemy.engine import Engine

from flask import Flask, request, jsonify
#use flaskSQLAlchemy for rest of app
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

# configure sqlite3 to enforce foreign key constraints (Don't need to know how it works)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# uses SQLAlchemy class to conenct ORM to Flask app 
db = SQLAlchemy(app)
now = datetime.now()

# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    #blog post user id has to be user id from user table and _set-sqlite_pragam) enforces foreign key constraints
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
