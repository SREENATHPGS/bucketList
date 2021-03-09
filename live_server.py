from waitress import serve
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
            "nat" : generate_password_hash("123456"),
            "admin" : generate_password_hash("1234")
        }

#class Users(db.Model):
#    pass

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash( users.get(username), password )
    return False

@app.route('/', methods = [ 'GET', 'POST' ])
@auth.login_required
def home():
    return render_template('frontend1.html')

@app.route('/bucket_item', methods = ['POST'])
@auth.login_required
def create_bucket_item():
    return "Create a bucket item."

if __name__ == '__main__':
    serve(host = '0.0.0.0', port = 5050, debug=True)
