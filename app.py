from flask import Flask, render_template, request
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

POSTGRES_USER=os.environ.get('POSTGRES_USER', 'bucketuser')
POSTGRES_PW=os.environ.get('POSTGRES_PW', 'dbpw')
POSTGRES_URL=os.environ.get('POSTGRES_URL', '0.0.0.0:5432')
POSTGRES_DB=os.environ.get('POSTGRES_DB', 'bucketlist')
DB_URL = 'postgresql+psycopg2://{user}:{password}@{url}/{db}'.format(user=POSTGRES_USER, password=POSTGRES_PW, url=POSTGRES_URL, db=POSTGRES_DB)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db =  SQLAlchemy(app)

migrate = Migrate(app, db)

from views import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
