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

#obtiene un character en concreto
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

#obtiene un planetas en concreto
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
    return jsonify(results), 200

#obtener los favoritos de cada usuario
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.session.get('user_id')
    if user_id is not None:
        
        user = Users.query.get(user_id)

        if user is not None:
            
            fav_characters = Fav_character.query.filter_by(user_id=user_id).all()
            fav_planets = Fav_planet.query.filter_by(user_id=user_id).all()
        results = {
            "user": user.serialize(),
            "favorite_characters": [fav.serialize() for fav in fav_characters],
            "favorite_planets": [fav.serialize() for fav in fav_planets]
        }
        return jsonify(results), 200
    
#añadir planetas y characters a favoritos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.session.get('user_id')
    if user_id is not None:
        # Verificar si el planeta ya está en los favoritos del usuario
        if Fav_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first():
            return jsonify({"message": "El planeta ya está en los favoritos del usuario"}), 400

        # Crear una nueva entrada en la tabla Fav_planet asociando el usuario y el planeta
        new_favorite = Fav_planet(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"message": "Planeta agregado a los favoritos del usuario"}), 200
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401

@app.route('/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(character_id):
    user_id = request.session.get('user_id')
    if user_id is not None:
        # Verificar si el personaje ya está en los favoritos del usuario
        if Fav_character.query.filter_by(user_id=user_id, character_id=character_id).first():
            return jsonify({"message": "El personaje ya está en los favoritos del usuario"}), 400

        # Crear una nueva entrada en la tabla Fav_character asociando el usuario y el personaje
        new_favorite = Fav_character(user_id=user_id, character_id=character_id)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"message": "Personaje agregado a los favoritos del usuario"}), 200
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401

#Elimina planetas y characters favoritos de cada usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.session.get('user_id')
    if user_id is not None:
        favorite = Fav_planet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": "Planeta eliminado de los favoritos del usuario"}), 200
        else:
            return jsonify({"message": "El planeta no está en los favoritos del usuario"}), 404
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401

@app.route('/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(character_id):
    user_id = request.session.get('user_id')
    if user_id is not None:
        
        favorite = Fav_character.query.filter_by(user_id=user_id, character_id=character_id).first()

        if favorite:
            
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": "Personaje eliminado de los favoritos del usuario"}), 200
        else:
            return jsonify({"message": "El personaje no está en los favoritos del usuario"}), 404
    else:
        return jsonify({"error": "Usuario no autenticado"}), 401


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

#crear usuario
@app.route('/Users', methods=['POST'])
def add_users():
    data = request.json
    if data['name'] == "" or data['last_name'] == "" or data['email'] == "" or data['city'] == "":
        return jsonify('No debe haber campos vacíos'), 400
    user = Users(**data)
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": "Debes rellenar todos los campos"
    }

    return jsonify(response_body), 200

#crear character
@app.route('/Characters', methods=['POST'])
def add_character():
    data = request.json
    if data['name'] == "" or data['height'] == "" or data['gender'] == "" or data['specie'] == "":
        return jsonify('No debe haber campos vacíos'), 400
    character = Characters(**data)
    db.session.add(character)
    db.session.commit()
    response_body = {
        "msg": "Debes rellenar todos los campos"
    }

    return jsonify(response_body), 200

#crear planeta
@app.route('/Planets', methods=['POST'])
def add_planet():
    data = request.json
    if data['name'] == "" or data['population'] == "" or data['terrain'] == "" or data['climate'] == "":
        return jsonify('No debe haber campos vacíos'), 400
    planet = Planets(**data)
    db.session.add(planet)
    db.session.commit()
    response_body = {
        "msg": "Debes rellenar todos los campos"
    }

    return jsonify(response_body), 200

# Eliminar un usuario
@app.route('/Users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404

# Eliminar un planeta
@app.route('/Planets/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"message": "Planeta eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "Planeta no encontrado"}), 404

# Eliminar un personaje
@app.route('/Characters/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Characters.query.get(character_id)
    if character:
        db.session.delete(character)
        db.session.commit()
        return jsonify({"message": "Personaje eliminado exitosamente"}), 200
    else:
        return jsonify({"error": "Personaje no encontrado"}), 404






# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
