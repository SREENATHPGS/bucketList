from waitress import serve
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging, os
from logging.handlers import TimedRotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

#Setting up logger.
logger = logging.getLogger("app_logs")
logger.setLevel(logging.INFO)
handler = TimedRotatingFileHandler('./logs/app.log',when='d',interval=1,backupCount=10)
handler.setFormatter(logging.Formatter('%(asctime)s - %(process)d -  %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

app = Flask(__name__)
auth = HTTPBasicAuth()

POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PW=os.environ.get('POSTGRES_PW')
POSTGRES_URL=os.environ.get('POSTGRES_URL')
POSTGRES_DB=os.environ.get('POSTGRES_DB')
DB_URL = 'postgresql+psycopg2://{user}:{password}@{url}/{db}'.format(user=POSTGRES_USER, password=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

app.secret_key="veryl0ng555stronghgkeyy"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #database declaration

users = {
            "nat" : generate_password_hash("123456"),
            "admin" : generate_password_hash("1234")
        }

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash( users.get(username), password )
    return False

from views.login_api import *

if __name__ == '__main__':
    logger.info("Starting server on port 5050.")
    app.run(host = '0.0.0.0', port = 5050, debug = True)
    #serve(app, host = '0.0.0.0', port = 5050)
