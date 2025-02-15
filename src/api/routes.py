from flask import Blueprint, jsonify, request
from flask_cors import CORS
from api.models import db, People, Planets, Users, Favorites

api = Blueprint("api", __name__)
CORS(api)

# People Endpoints
@api.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.serialize() for person in people])

@api.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize())

# Planets Endpoints
@api.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([planet.serialize() for planet in planets])

@api.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize())

# Users Endpoints
@api.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.serialize() for user in users])

@api.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites])

# Favorites Endpoints
@api.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Favorite already exists"}), 400

    try:
        favorite = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    existing_favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"error": "Favorite already exists"}), 400

    try:
        favorite = Favorites(user_id=user_id, people_id=people_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    try:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite person deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
