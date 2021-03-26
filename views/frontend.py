import json
from flask import request, jsonify, render_template
from app import app, auth

@app.route('/', methods = [ 'GET', 'POST' ])
@auth.login_required
def home():
    return render_template('frontend1.html')