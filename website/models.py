from sqlalchemy.orm import backref
from sqlalchemy.sql.expression import false
from . import db # . means current package
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True) # Max length of characters is 150
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone = True), default = func.now())
    
    posts = db.relationship('Post', backref = 'user', passive_deletes = True)
    # Backref allows Post.User(), passive_deletes must be there for cascade to work

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False) # Nullable means there must be text
    date_created = db.Column(db.DateTime(timezone = True), default = func.now()) 
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False) 
    # One integer must match an ID from the User Class
    # When user is deleted, all of the posts the user has get deleted