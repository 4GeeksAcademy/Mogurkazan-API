from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


    #GET a mis tablas
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    specie = db.Column(db.String(250), nullable=False)
    fav_users = relationship("Fav_character", back_populates="character")

    def __repr__(self):
        return '<Characters %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "gender": self.gender,
            "specie": self.specie,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    fav_users = relationship("Fav_planet", back_populates="planet")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "climate": self.climate,
            # do not serialize the password, its a security breach
        }
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250), nullable=False)
    fav_characters = relationship("Fav_character", back_populates="user")
    fav_planets = relationship("Fav_planet", back_populates="user")

    def __repr__(self):
        return '<Users %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "city": self.city,
            # do not serialize the password, its a security breach
        }
class Fav_character(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)
    user = relationship("Users", back_populates="fav_characters")
    character = relationship("Characters", back_populates="fav_users")
    
    def __repr__(self):
        return '<Fav_character %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            # do not serialize the password, its a security breach
        }
class Fav_planet(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), primary_key=True)
    user = relationship("Users", back_populates="fav_planets")
    planet = relationship("Planets", back_populates="fav_users")
    
    def __repr__(self):
        return '<Fav_planet %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            # do not serialize the password, its a security breach
        }
    
   

