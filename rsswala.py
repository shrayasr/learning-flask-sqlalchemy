
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from datetime import datetime

# Requirements
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/rsswala_test'
db = SQLAlchemy(app)

"""
    user_feeds table.
    Holds the mapping between what feeds are owned by which users
"""
UserFeeds = db.Table('user_feeds',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('feed_id', db.Integer, db.ForeignKey('feed.id'))
        )

"""
    user_read_items table.
    Holds the mapping between which items have been marked "read" by which 
    user
"""
UserReadItems = db.Table('user_read_items',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
        )

class User(db.Model):
    """
        user table.

        Each user is identified by:
            - A running serial
            - A email address, used to login
            - A password

        TODO bring in salt here.
    """

    # Column defs
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(32))

    """
        Define a relationship with the "Item" table.

        Gives the list of items read for that user.

        Use the user_read_items as a secondary relationship on which
        this relationship is defined. Additionally add a back reference
        to the Item table as well; which means that this would give the
        list of users who have marked that item as read
    """
    items_read = db.relationship('Item', secondary=UserReadItems,
            backref = db.backref('read_by', lazy='dynamic'))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

class Feed(db.Model):
    """
        feed table.

        Stores the list of feeds in the system. Each feed is identified by:
            - Running serial
            - Feed URL, the URL of the feed itself
            - Title 
            - Description 
            - Link to the site where the feed is hosted
    """

    # Column defs
    id = db.Column(db.Integer, primary_key=True)
    feed_url = db.Column(db.String(120), unique=True)
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(120))

    """
        Define a relationship with the "User" table.

        Gives the list of users associated to a feed.

        Use the user_feeds as a secondary relationship on which 
        this relationship is defined. Additionally add a back reference
        to the User table as well. This would give the list of feeds
        associated to that user
    """
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
    """
        item table.

        Stores the individual items for all the feeds. Each item is identified by:
            - Running serial
            - The feed it is associated to. This is a foreign key to the feed
                table. It references the running serial defined on the feed table
                then
            - Title
            - Description
            - Link
            - guid; usually the permalink, but can also not be the permalink
            - guid_hash, we hash the guid to get a more unique identifier
            - published date
    """

    # Column defs
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    title = db.Column(db.String(120))
    description = db.Column(db.Text)
    link = db.Column(db.String(120))
    guid = db.Column(db.String(120), unique=True)
    guid_hash = db.Column(db.String(32), unique=True)
    pub_date = db.Column(db.DateTime)

    """
        Define a relationship with the "Feed" table.

        Gives the list of items associated to that feed.

        Add a back reference to the Feed table as well. This would give the feed
        associated to that item. The cascade='all, delete-orphan' makes sure that 
        deletes are cascade
    """
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

