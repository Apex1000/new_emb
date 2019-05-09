from flask import Flask, render_template, flash, redirect, url_for,session,request, logging,jsonify
from flask_pymongo import PyMongo
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import flask_excel as excel
import flask_excel
import pyexcel_xls

app = Flask(__name__)
flask_excel.init_excel(app)
#MongoDB Config 
app.config["MONGO_DNAME"] = "test"
app.config["MONGO_URI"] = "mongodb://apex1000:1234@cluster0-shard-00-00-pykfw.gcp.mongodb.net:27017,cluster0-shard-00-01-pykfw.gcp.mongodb.net:27017,cluster0-shard-00-02-pykfw.gcp.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"
mongo = PyMongo(app)

@app.route('/test', methods=['GET','POST'])
def test():
    db=mongo.db.users

    output = []

    for i in db.find():
        output.append({'name' :i['name'] })

    return jsonify({'result':output})
@app.route('/')
def index():
    return render_template('index.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap



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
        existing_user = user.find_one({'email': form.email.data})
        if existing_user is None:
            user.insert_one({'name': form.name.data,'username':form.username.data,'email':form.email.data,'password':form.password.data})
            return redirect(url_for('index'))
        return 'User already registerd'
    return render_template('register.html',form=form)
# User login

class LoginForm(Form):
    email = StringField('Email',[validators.Length(min=6,max=35)])
    password = PasswordField('Password',[validators.DataRequired()])

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST': 
        user = mongo.db.users
        auth_user = user.find_one({'email':form.email.data})
        
        if auth_user:
            if (auth_user['password'])==(request.form['password']):
                session['username'] = form.email.data
                session['logged_in'] = True
                return redirect(url_for('dashboard'))
            return 'Password Incorrect'
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


#Environment Dashboard
@app.route('/allemdboard')
def allemdboard():
    return render_template('./environment/index.html')

@app.route('/emd',methods=['GET'])
def emd():
    indoor_room = mongo.db.indoor_room
    output=[]
    for i in indoor_room.find():
        output.append({'name' :i['name_of_the_institute'] })
    # return jsonify({'indoor_room':output})
    return render_template('./environment/home.html',indoor_room=output)



#Class Add Rooms EMD
class AddRoomEmd(Form):
    name_of_the_institute = StringField('Name of the institute', [validators.Length(min=1, max=50)])
    name_of_classroom = StringField('Name of Classroom', [validators.Length(min=1, max=50)])
    no_of_occupants = StringField('No of Occupants', [validators.Length(min=1,max=100)])
    age_range = StringField('Age Range', [validators.Length(min=1,max=100)])
    size_of_the_room = StringField('Size of the Room', [validators.Length(min=1,max=100)])
    no_of_windows = StringField('No of Windows', [validators.Length(min=1,max=100)])
    no_of_doors = StringField('No of Doors', [validators.Length(min=1,max=100)])
    no_of_ac = StringField('No of AC', [validators.Length(min=1,max=100)])
    no_of_fan = StringField('No of Fan', [validators.Length(min=1,max=100)])
    no_of_ac_on_status = StringField('No of ac on Status', [validators.Length(min=1,max=100)])
    no_of_fan_on_status = StringField('No of Fan on Status', [validators.Length(min=1,max=100)])
    no_of_open_window = StringField('No of open Window', [validators.Length(min=1,max=100)])
    no_of_open_doors = StringField('No of open Doors', [validators.Length(min=1,max=100)])

@app.route('/add_room_emd', methods=['GET','POST'])
def add_room_emd():
    form = AddRoomEmd(request.form)
    indoor_room = mongo.db.indoor_room
    if request.method == 'POST' and form.validate():
        indoor_room.insert_one({
        'name_of_the_institute' : form.name_of_the_institute.data,
        'name_of_classroom' : form.name_of_classroom.data,
        'no_of_occupants' : form.no_of_occupants.data,
        'age_range' : form.age_range.data,
        'size_of_the_room' : form.size_of_the_room.data,
        'no_of_windows' : form.no_of_windows.data,
        'no_of_doors' : form.no_of_doors.data,
        'no_of_ac' : form.no_of_fan.data,
        'no_of_fan' : form.no_of_ac.data,
        'no_of_ac_on_status' : form.no_of_ac_on_status.data,
        'no_of_fan_on_status' : form.no_of_fan_on_status.data,
        'no_of_open_window' : form.no_of_open_window.data,
        'no_of_open_doors' : form.no_of_open_doors.data
        })
    return render_template('./environment/extra/_addroom.html',form=form)

@app.route('/upload_box_data', methods=['GET','POST'])
@is_logged_in
def upload_box_data():
    box_data = mongo.db.box_data
    if request.method == 'POST':
        output = []
        c=[]
        output = request.get_array(field_name='file')
        for i in output:
            box_data.insert({  "DATE":"DATE",
                                "DATA": [{"DATE_TIME": i[0],
                                            "SL_NO":i[1],
                                            "PM1":i[2],
                                            "PM2-5":i[3],
                                            "PM10":i[4],
                                            "NO2":i[5],
                                            "CO2":i[6],
                                            "CO":i[7],
                                            "HUMIDITY":i[8],
                                            "TEMP":i[9]}]
                                })
        # box_data.insert({'box':c})
        # return jsonify({"result": c })
    return render_template('./environment/upload.html')


@app.route('/get_box_data',methods=['GET'])
def get_box_data():
    box_data = mongo.db.box_data
    output = []
    for i in box_data.find():
        output.append({'data': i['DATA']})
    return jsonify({'result' : output})

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
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=80, debug=True)