from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route("/")
def index():
    return redirect ('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/process', methods=['POST'])
def login_process():
    data = {
        'email': request.form['email']
    }
    user = User.check_email(data)
    if not user:
        flash('WRONG EMAIL YOU DUMMY')
        return redirect ('/login')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('WRONG PASSWORD YOU DUMMY')
        return redirect ('/login')
    if "id" not in session:
        session['id'] = ""
    # session['username'] = request.form['username']  ASK RYAN OR TA
    session['id'] = user.id 
    return redirect('/success')

@app.route('/add')
def create():
    return render_template('registration.html')

@app.route('/success')
def successful_login():
    return redirect('/dashboard')

@app.route('/add/process', methods=['POST'])
def creating_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password']
    }
    if request.form['password'] != request.form['confirmation']:
        flash("Password don't match")
        return redirect('/add')
        # wuv u Justin
    if not User.validate_user(data):
        return redirect('/add')
    data['password'] = bcrypt.generate_password_hash(request.form['password'])
    User.add_user(data)
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



