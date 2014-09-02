
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/rsswala_test'
db = SQLAlchemy(app)

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(32), unique=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Feeds(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    feed_url = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)
    link = db.Column(db.String(120), unique=True)

    def __init__(self, feed_url, title, description, link):
        self.feed_url = feed_url
        self.title = title
        self.description = description
        self.link = link

    def __repr__(self):
        return '<Feed %r %r>' % (self.feed_url, self.title)

class Items(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(120))
    guid = db.Column(db.String(120), unique=True)
    guid_hash = db.Column(db.String(32), unique=True)
    pubdate = db.Column(db.DateTime)

    feed = db.relationship('Feeds', 
            backref = db.backref('items', cascade='all, delete-orphan', lazy='dynamic'))

    def __init__(self, feed, title, description, link, guid, guid_hash, 
            pub_date):
        self.feed = feed
        self.title = title
        self.description = description
        self.link = link
        self.guid = guid
        self.guid_hash = guid_hash
        self.pub_date = pub_date

    def __repr__(self):
        return '<Item %r %r>' % (self.title, self.feed)

"""
  `user_id` bigint(20) unsigned NOT NULL,
  `feed_id` bigint(20) unsigned NOT NULL,
  `subscription_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,

class UserFeeds(db.Model):

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))

    user = db.relationship

    subscription_date = db.Column(db.DateTime)

    def __init__(self, user_id, feed_id, subscription_date=None):
        self.user_id = user_id
        self.feed_id = feed_id
        self.subscription_date = subscription_date

class Post(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', 
            backref = db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return "<Post %r>" % self.title

class Category(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Category %r>" % self.name
"""
