import json
from flask import request, jsonify
from app import app, auth
from models.model import AccountUser

logger = app.logger
def validateData(content_func):
    def inner(*args, **kwargs):
        logger.info("validating data")
        logger.info(f"Request method is : {request.method}")
        data = request.get_json()

        if "username" not in data:
            return "username not in data.", 404
        
        if "password" not in data:
            return "password not in data", 404

        if "email" in data:
            pass
        elif "mobile_number" in data:
            pass
        else:
            return "email or mobile number not in data.", 404

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

# @app.route('/', methods = [ 'GET', 'POST' ])
# @auth.login_required
# def home():
#     return render_template('frontend1.html')

# @app.route('/bucket_item', methods = ['POST'])
# @auth.login_required
# def create_bucket_item():
#     return "Create a bucket item."

@app.route('/users', methods = ['POST'])
@validateData
def add_user(data):
    logger.info(data)
    logger.info("Creating user.")
    newUser = AccountUser()
    newUser.username = data["username"]
    newUser.password_hash = data["password"]
    newUser.email = data["email"]

    newUser.create()
    return "user registration successful."

@app.route('/users', methods = ['PATCH'])
def update_user():
    data = request.get_json()
    logger.info(data)
    uid = data["uid"]
    for attribute_name, value in data["update_data"].items():
        logger.info(f"Patching {attribute_name} with {value} for user {uid}")
        AccountUser.update(uid, attribute_name, value)
    return "updating registration successful."

@app.route('/users', methods = ['GET'])
def get_user():
    def formatify(ob):
        ob = json.loads(json.dumps(dict(ob.__dict__), default=str))
        ob.pop('id')
        ob.pop('_sa_instance_state')
        return ob

    out = [formatify(record) for record in AccountUser.get()]
    return jsonify(out)

@app.route('/users', methods = ['DELETE'])
def delete_user():
    data = request.get_json()
    uid_list = data["uids"]
    for uid in uid_list:
        logger.info(f"Deleting use with uid {uid}")
        AccountUser.delete(uid)
    return "deleteing user registration successful."