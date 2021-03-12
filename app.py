from waitress import serve
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging.handlers import TimedRotatingFileHandler

#Setting up logger.
logger = logging.getLogger("app_logs")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('./logs/app.log',when='d',interval=1,backupCount=10)
handler.setFormatter(logging.Formatter('%(asctime)s - %(process)d -  %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
            "nat" : generate_password_hash("123456"),
            "admin" : generate_password_hash("1234")
        }

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
    logger.info("Starting server on port 5050.")
    app.run(host = '0.0.0.0', port = 5050, debug = True)
    #serve(app, host = '0.0.0.0', port = 5050)
