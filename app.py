from waitress import serve
from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import logging, os, sys
from logging.handlers import TimedRotatingFileHandler
from flask_sqlalchemy import SQLAlchemy

from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    },
    'custom': {
        'class' : 'logging.handlers.TimedRotatingFileHandler',
        'formatter' : 'default',
        'filename' :'./logs/app.log'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'custom']
    }
})

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

from views.users import *
from views.wishes import *

if __name__ == '__main__':
    app.logger.info("Starting server on port 5050.")
    app.run(host = '0.0.0.0', port = 5050, debug = True)
    #serve(app, host = '0.0.0.0', port = 5050)
