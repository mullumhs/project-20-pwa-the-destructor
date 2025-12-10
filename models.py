from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Define your database model here
# Example: class Item(db.Model):


class Playlists(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    creator = db.Column(db.String(100))
    description = db.Column(db.String(256))
    songs = db.Column(db.JSON)
    image = db.Column(db.String(100), nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre = db.Column(db.String(100))
    image = db.Column(db.String(100), nullable=False)