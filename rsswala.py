
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/rsswala_test'
db = SQLAlchemy(app)

UserFeeds = db.Table('user_feeds',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
        )

UserReadItems = db.Table('user_read_items',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
        )

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(32))

    items_read = db.relationship('Item', secondary=UserReadItems,
            backref = db.backref('read_by', lazy='dynamic'))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Feed(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    feed_url = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(120))

    users = db.relationship('User', secondary=UserFeeds,
            backref = db.backref('feeds', lazy='dynamic'))

    def __init__(self, feed_url, title, description, link, user):
        self.feed_url = feed_url
        self.title = title
        self.description = description
        self.link = link
        self.users.append(user)

    def __repr__(self):
        return '<Feed %r %r>' % (self.feed_url, self.title)

class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(120))
    guid = db.Column(db.String(120), unique=True)
    guid_hash = db.Column(db.String(32), unique=True)
    pub_date = db.Column(db.DateTime)

    feed = db.relationship('Feed', 
            backref = db.backref('items', cascade='all, delete-orphan', 
                lazy='dynamic'))

    def __init__(self, feed, title, description, link, guid, guid_hash, 
            pub_date):
        self.feed = feed
        self.title = title
        self.description = description
        self.link = link
        self.guid = guid
        self.guid_hash = guid_hash
        self.pub_date = datetime.strptime(pub_date, "%Y-%m-%d")

    def __repr__(self):
        return '<Item %r %r>' % (self.title, self.feed)

