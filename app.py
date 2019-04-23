from flask import Flask, render_template, flash, redirect, url_for,session,request, logging,jsonify
from flask_pymongo import PyMongo
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

#MongoDB Config 
app.config["MONGO_DNAME"] = "test"
app.config["MONGO_URI"] = "mongodb://apex1000:1234@cluster0-shard-00-00-pykfw.gcp.mongodb.net:27017,cluster0-shard-00-01-pykfw.gcp.mongodb.net:27017,cluster0-shard-00-02-pykfw.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
mongo = PyMongo(app)

@app.route('/test', methods=['GET','POST'])
def test():
    db=mongo.db.users

    output = []

    for i in db.find():
        output.append({'name' :i['name'], 'lang':i['lang'] })

    return jsonify({'result':output})
@app.route('/')
def index():
    return render_template('index.html')

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=2, max=35)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


@app.route('/register', methods=['POST','GET'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = mongo.db.users
        user.insert_one({'name': form.name.data,'username':form.username.data,'email':form.email.data,'password':form.password.data})
        return redirect(url_for('index'))
        return 'User already registerd'
    return render_template('register.html',form=form)
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
    app.run(host='0.0.0.0', port=80, debug=True)