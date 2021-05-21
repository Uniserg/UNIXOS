from flask import Flask, request, jsonify, make_response, abort
from datetime import date

from models.user import User
from service.config import Config
from service.dbms import *


app = Flask(__name__)
app.config.from_object(Config)


@app.route("/users", methods=['GET'])
def get_user_controller() -> str:
    if not request.json:
        abort(400)
    user = get_one_user(request.json['login'])
    return user.toJSON() if user is not None else abort(404)


@app.route("/users", methods=['POST'])
def add_user_controller() -> str:
    if (not request.json or
            not 'login' in request.json or
            not 'password' in request.json):
        abort(400)
    user = User(
        request.json['login'],
        request.json['password'],
        None,
        date.today()
    )
    return jsonify({'status': 'OК'}) if add_user(user) else abort(404)


@app.route("/users", methods=['PUT'])
def update_user_controller():
    if (not request.json or
            not 'old_login' in request.json or
            not 'login' in request.json or
            not 'password' in request.json):
        abort(400)
    new_user = User(
        request.json['login'],
        request.json['password'],
        None,
        date.today()
    )
    return jsonify({'status': 'OК'}) if update_user(request.json['old_login'], new_user) else abort(404)


@app.route("/users", methods=['DELETE'])
def delete_user_controller():
    if (not request.json or
            not 'login' in request.json):
        abort(400)
    user = User(request.json['login'])
    return jsonify({'status': 'OК'}) if delete_user(user) else abort(404)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'NOT FOUND'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'BAD REQUEST'}), 400)