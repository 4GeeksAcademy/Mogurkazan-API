"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Characters, Planets, Users, Fav_character, Fav_planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



#mis elementos
@app.route('/Characters', methods=['GET'])
def get_characters():
    all_characters = Characters.query.all()
    results = list(map(lambda characters: characters.serialize(), all_characters))
    response_body = {
        "msg": "Hello, no sé lo que hago"
    }

    return jsonify(results), 200

@app.route('/Characters/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Characters.query.filter_by(id=character_id).first()

    return jsonify(character.serialize()), 200

@app.route('/Planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    results = list(map(lambda planets: planets.serialize(), all_planets))
    response_body = {
        "msg": "Hello, no sé lo que hago con planetas"
    }

    return jsonify(results), 200
@app.route('/Planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()

    return jsonify(planet.serialize()), 200

@app.route('/Users', methods=['GET'])
def get_users():
    all_users = Users.query.all()
    results = list(map(lambda users: users.serialize(), all_users))
    response_body = {
        "msg": "Hello, no sé lo que hago con users"
    }
@app.route('/Fav_character', methods=['GET'])
def get_fav_character():
    all_fav_character = Fav_character.query.all()
    results = list(map(lambda fav_character: fav_character.serialize(), all_fav_character))
    response_body = {
        "msg": "Hello, no sé lo que hago con favs"
    }

    return jsonify(results), 200
@app.route('/Fav_planet', methods=['GET'])
def get_fav_planet():
    all_fav_planet = Fav_planet.query.all()
    results = list(map(lambda fav_planet: fav_planet.serialize(), all_fav_planet))
    response_body = {
        "msg": "Hello, no sé lo que hago con favs"
    }

    return jsonify(results), 200
@app.route('/Users', methods=['POST'])
def add_users():
    data = request.json
    
    user = Users(**data)
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": "Hello, no sé lo que hago con users en POST"
    }

    return jsonify(results), 200







# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
