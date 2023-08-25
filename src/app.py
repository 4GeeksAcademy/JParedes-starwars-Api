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
from models import db, User , Planet , People , Favorite
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

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()

    return jsonify(users = [user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_id(user_id):

    user = User.query.get(user_id)
    if user is not None:
        return jsonify(user = [user.serialize()]), 200
    return jsonify({"msg":"No existe el usuario"}),400

@app.route('/people', methods=['GET'])
def get_people():

    peoples = People.query.all()

    return jsonify(characters = [people.serialize() for people in peoples]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    people = People.query.get(people_id)

    if people is not None:
     return jsonify(character = [people.serialize()]), 200
    
    return jsonify({"msg":"No existe el personaje"}),400


@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()

    return jsonify(planets = [planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
     
    planet = Planet.query.get(planet_id)

    if planet is not None:
     return jsonify(planet = [planet.serialize()]), 200

    return jsonify({"msg":"No existe el planeta"}),400

@app.route('/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    favorites = Favorite.query.filter_by(user = user_id).first()
    if favorites == None:
        return "No existe favoritos para el user_id: "+str(user_id), 404
    return jsonify(favorites = [favorites.serialize()]), 200

@app.route('/<int:user_id>/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(user_id, people_id):
    favorite = Favorite()
    favorite.name = request.json.get("name")
    favorite.people_id = people_id
    favorite.user = user_id
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"El personaje favorito a sido agregado!"})

@app.route('/<int:user_id>/favorites/plante/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    favorite = Favorite()
    favorite.name = request.json.get("name")
    favorite.planet_id = planet_id
    favorite.user = user_id
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"El planeta favorito a sido agregado!"})

@app.route('/<int:user_id>/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorites = Favorite.query.filter_by(user = user_id).first()
    if favorites == None:
        return "No hay favoritos para user_id: "+str(user_id), 404
    response_body = list(map(lambda x:x.serialize(),favorites))
    for favorite in response_body:
        if "planet_id" in favorite:
            if favorite.planet_id == planet_id:
                db.session.delete(favorite)
                return "Planeta favorito eliminado!", 200
        return "No hay planeta en favoritos", 404
    return "No favoritos", 404

@app.route('/<int:user_id>/favorites/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(user_id, people_id):
    favorites = Favorite.query.filter_by(user = user_id).first()
    if favorites == None:
        return "No hay favoritos para user_id: "+str(user_id), 404
    response_body = list(map(lambda x:x.serialize(),favorites))
    for favorite in response_body:
        if "people_id" in favorite:
            if favorite.people_id == people_id:
                db.session.delete(favorite)
                return "Personaje favorito eliminado", 200
        return "No hay personaje en favoritos", 404
    return "No favoritos", 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
