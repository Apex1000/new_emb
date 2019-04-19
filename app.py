from flask import Flask, render_template, flash, redirect, url_for,session,request, logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'user_emb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=50)])
    email = StringField('Email', [validators.Length(min=7,max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Paaword do not match')
    ])
    confirm = PasswordField('Comfirm Password')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('index'))
        
    return render_template('register.html',form=form)



# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

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


#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

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

#Add Rooms EMD
@app.route('/add_room_emd', methods=['GET','POST'])
@is_logged_in
def add_room_emd():
    form = AddRoomEmd(request.form)
    if request.method == 'POST' and form.validate():
        name_of_the_institute = form.name_of_the_institute.data
        name_of_classroom = form.name_of_classroom.data
        no_of_occupants = form.no_of_occupants.data
        age_range = form.age_range.data
        size_of_the_room = form.size_of_the_room.data
        no_of_windows = form.no_of_windows.data
        no_of_doors = form.no_of_doors.data
        no_of_ac = form.no_of_fan.data
        no_of_fan = form.no_of_ac.data
        no_of_ac_on_status = form.no_of_ac_on_status.data
        no_of_fan_on_status = form.no_of_fan_on_status.data
        no_of_open_window = form.no_of_open_window.data
        no_of_open_doors = form.no_of_open_doors.data


        #Create Cursor
        cur = mysql.connection.cursor()

        #Ececute
        cur.execute("INSERT INTO emd_indoor_room(name_of_the_institute,name_of_classroom,no_of_occupants,age_range,size_of_the_room,no_of_windows,no_of_doors,no_of_ac,no_of_fan,no_of_ac_on_status,no_of_fan_on_status,no_of_open_window,no_of_open_doorsname_of_the_institute,name_of_classroom,no_of_occupants,age_range,size_of_the_room,no_of_windows,no_of_doors,no_of_ac,no_of_fan,no_of_ac_on_status,no_of_fan_on_status,no_of_open_window,no_of_open_doors) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name_of_the_institute,name_of_classroom,no_of_occupants,age_range,size_of_the_room,no_of_windows,no_of_doors,no_of_ac,no_of_fan,no_of_ac_on_status,no_of_fan_on_status,no_of_open_window,no_of_open_doors))

        #Commit to DB
        cur.connection.commit()

        #Close Connection
        cur.close()

        flash('Room Added','success')

        return redirect(url_for('emd'))

    return render_template('environment/extra/_addroom.html', form=form)



# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

#Environment Dashboard

@app.route('/allemdboard')
@is_logged_in
def allemdboard():
    return render_template('./environment/index.html')




@app.route('/emd')
@is_logged_in
def emd():

    # Create cursor
    cur = mysql.connection.cursor()

    # Get rooms
    result = cur.execute("SELECT * FROM emd_indoor_room")
    print (result)
    emd_indoor_room = cur.fetchall()

    if result > 0:
        return render_template('./environment/home.html',emd_indoor_room=emd_indoor_room)
    else:
        msg = 'No Articles Found'
        return render_template('./environment/home.html',msg=msg)

    #Close connection
    cur.close()

@app.route('/emd_indoor')
@is_logged_in
def emd_indoor():
    return render_template('./environment/emd_indoor.html')

#RoadTraffic
@app.route('/road_traffic')
@is_logged_in
def road_traffic():
    return render_template('./roadtraffic/home.html')

#RoadTraffic
@app.route('/distancemap')
def pointmap():
    return render_template('./roadtraffic/index.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)