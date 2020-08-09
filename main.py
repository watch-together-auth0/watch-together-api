from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify, request
from flask import session
from flask_cors import CORS, cross_origin
from deta import Deta
load_dotenv()

deta = Deta(env['PROJECT_KEY']) # configure your Deta project
usersDb = deta.Base('users')
channelsDb = deta.Base('channel')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.secret_key = env['SECRET_KEY']


@app.route('/users', methods=['GET'])
@cross_origin()
def getUsers():
    email = request.args.get('email')
    if email:
        users = usersDb.fetch({"email": email})
    else:
        users = usersDb.fetch()
    return jsonify(result = next(users))

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    user = usersDb.get(id)
    if user:
        return user, 200
    else:
        return jsonify({"error": "Not found"}), 404


@app.route('/users', methods=['POST'])
@cross_origin()
def createUser():
    name = request.json.get("name")
    email = request.json.get("email")
    user = usersDb.put({
        "name": name,
        "email": email
    })
    return jsonify(user), 201

@app.route('/channels', methods=['POST'])
@cross_origin()
def createChannel():
    name = request.json.get("name")
    ownerId = request.json.get("owner_id")
    channel = channelsDb.put({
        "name": name,
        "owner_id": ownerId,
        "members": [],
        "video_url": "",
        "video_title": "",
        "video_thumb_url": "",
        "video_description": ""
    })
    return jsonify(channel), 201

@app.route('/channels/<id>/add', methods=['PATCH'])
@cross_origin()
def addMember(id):
    channel = channelsDb.get(id)
    print(channel['members'])
    userid = request.json.get("userId")
    if userid in channel['members']:
        print('User already in channel')
        return jsonify({"message": "User is already a member"}), 204
    updates = {
        "members": channelsDb.util.append(userid)
    }
    channelsDb.update(updates, id)
    return jsonify({}), 204

@app.route('/channels/<id>', methods=['PATCH'])
@cross_origin()
def updateChannel(id):
    video_url = request.json.get("video_url")
    video_title = request.json.get("video_title")
    video_thumb_url = request.json.get("video_thumb_url")
    video_description = request.json.get("video_thumb_url")
    updates = {
        "video_url": video_url,
        "video_title": video_title,
        "video_thumb_url": video_thumb_url,
        "video_description": video_description,
    }
    channelsDb.update(updates, id)
    return jsonify({}), 204

@app.route('/channels', methods=['GET'])
@cross_origin()
def getChannels():
    ownerId = request.args.get('ownerId')
    if ownerId:
        channels = channelsDb.fetch({"owner_id": ownerId})
    else:
        channels = channelsDb.fetch()
    return jsonify(result = next(channels))