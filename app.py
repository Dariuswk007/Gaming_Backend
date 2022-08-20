from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String, nullable = False)
    genre = db.Column(db.String, nullable = False)
    console_used = db.Column(db.String, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False)

    def __init__(self, title, genre, console_used, price, description, rating, image_url):
        self.title = title
        self.genre = genre
        self.console_used = console_used
        self.price = price
        self.description = description
        self.rating = rating
        self.image_url = image_url

class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'genre', 'console_used', 'price', 'description', 'rating', 'image_url')
    
game_schema = GameSchema()
multiple_game_schema = GameSchema(many=True)





#Games End Points
@app.route('/game/add', methods = ["POST"])
def add_game():
    post_data = request.get_json()
    title = post_data.get('title')
    genre = post_data.get('genre')
    console_used = post_data.get('console_used')
    price = post_data.get('price')
    description = post_data.get('description')
    rating = post_data.get('rating')
    image_url = post_data.get('image_url')

    new_game = Game(title, genre, console_used, price, description, rating, image_url)
    db.session.add(new_game)
    db.session.commit()

    return jsonify('Game added successfully')

@app.route('/game/get', methods = ["GET"])
def get_games():
    game = db.session.query(Game).all()
    return jsonify(multiple_game_schema.dump(game))

@app.route('/game/get/<id>', methods = ["GET"])
def get_game(id):
    game = Game.query.get(id)
    return game_schema.jsonify(game)

@app.route('/game/update/<id>', methods=["PUT"])
def game_update(id):
    post_data = request.get_json()
    title = post_data.get('title')
    genre = post_data.get('genre')
    console_used = post_data.get('console_used')
    price = post_data.get('price')
    description = post_data.get('description')
    rating = post_data.get('rating')

    game_data = db.session.query(Game).filter(Game.id == id).first()

    game_data.title = title
    game_data.genre = genre
    game_data.console_used = console_used
    game_data.price = price
    game_data.description = description
    game_data.rating = rating

    db.session.commit()
    return jsonify("The has been updated.")


if __name__ == "__main__":
    app.run(debug=True)