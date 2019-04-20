from flask import Flask, render_template, flash, redirect, url_for,session,request, logging
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register')
def register():
    return render_template('register.html')
# User login
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/add_room_emd')
def add_room_emd():
    return render_template('environment/extra/_addroom.html')



# Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

#Environment Dashboard

@app.route('/allemdboard')
def allemdboard():
    return render_template('./environment/index.html')




@app.route('/emd')
def emd():
    return render_template('./environment/home.html')
@app.route('/emd_indoor')
def emd_indoor():
    return render_template('./environment/emd_indoor.html')

#RoadTraffic
@app.route('/road_traffic')
def road_traffic():
    return render_template('./roadtraffic/home.html')

#RoadTraffic
@app.route('/distancemap')
def pointmap():
    return render_template('./roadtraffic/index.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)