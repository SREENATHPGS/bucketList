import json
from flask import request, jsonify, render_template
from app import app, auth
from models.model import Wish, getApiKey

logger = app.logger
def validateData(content_func):
    def inner(*args, **kwargs):
        logger.info("validating data")
        logger.info(f"Request method is : {request.method}")
        data = request.get_json()
        logger.info(data)

        if "wish" not in data:
            return "username not in data.", 404
        
        return content_func(data)
    inner.__name__ = content_func.__name__
    return inner

def authenticate(content_func):
    def inner(*args, **kwargs):
        print("authenticating")
        print(request.headers)
        if "api_key" in request.headers:
            print("api found.")
            if request.headers["api_key"] == "nsfkjxxcesskkzzzQQQWWW234##@$ESR$FWA":
                print("Authenticated!!")
                #return True
            else:
                return "Unauthorized", 401
        else:
            return "Unauthorized", 401
        return content_func(*args, **kwargs)
    inner.__name__ = content_func.__name__
    return inner


@app.route('/wish', methods = ['POST'])
@validateData
def add_wish(data):
    logger.info(data)
    logger.info("Creating wish.")
    newWish = Wish()
    newWish.wish = data["wish"]
    newWish.uid = getApiKey(16)
    newWish.create()
    del newWish
    return "Adding wish successful."

@app.route('/wish', methods = ['PATCH'])
def update_wish():
    data = request.get_json()
    logger.info(data)
    uid = data["uid"]
    for attribute_name, value in data["update_data"].items():
        logger.info(f"Patching {attribute_name} with {value} for user {uid}")
        Wish.update(uid, attribute_name, value)
    return "updating wish successful."

@app.route('/wish', methods = ['GET'])
def get_wish():
    def formatify(ob):
        ob = json.loads(json.dumps(dict(ob.__dict__), default=str))
        ob.pop('id')
        ob.pop('_sa_instance_state')

        return ob

    out = [formatify(record) for record in Wish.get()]
    return jsonify(out)

@app.route('/wish', methods = ['DELETE'])
def delete_wish():
    data = request.get_json()
    uid_list = data["uids"]
    for uid in uid_list:
        logger.info(f"Deleting use with uid {uid}")
        Wish.delete(uid)
    return "deleteing user registration successful."