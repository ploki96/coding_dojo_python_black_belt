from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.painting import Painting

@app.route('/dashboard')
def dashboard():
    data = {
        'id': session['id']
    }
    user = User.single_user_w_purchases(data)
    print(user)
    users = User.get_all()
    paintings = Painting.get_all()
    purchases = User.show_purchases(data)
    return render_template('dashboard.html', user = user, paintings = paintings, purchases = purchases)

@app.route('/painting/new')
def new_painting():
    if 'id' not in session:
        flash('You must be logged in to view this page')
        return redirect ('/login')
    return render_template('add_painting.html')

@app.route('/painting/create', methods=["POST"])
def add_painting():
    if not Painting.validate_painting(request.form):
        return redirect('/painting/new')
    data = {
    'user_id': session['id'],
    'title': request.form['title'],
    'description': request.form['description'],
    'quantity_made': request.form['quantity_made'],
    'price': request.form['price']
    }
    Painting.add_painting(data)
    return redirect('/dashboard')

@app.route('/painting/edit/<int:num>')
def edit_painting(num):
    return render_template('edit_painting.html',id = num)

@app.route('/painting/edit/<int:num>/process', methods=['POST'])
def process_edit_painting(num):
    if not Painting.validate_painting(request.form):
        s = f'/painting/edit/{num}'
        return redirect(s)
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'quantity_made': request.form['quantity_made'],
        'price': request.form['price'],
        'id': num
    }
    Painting.edit_painting(data)
    return redirect ('/dashboard')

@app.route('/painting/delete/<int:num3>')
def delete_painting(num3):
    data={
        'id': num3
    }
    Painting.delete_painting(data)
    return redirect('/dashboard')

@app.route('/painting/<int:num2>')
def painting(num2):
    data = {
        'id': num2
    }
    painting = Painting.get_painting(data)

    users = User.get_all()
    
    return render_template('painting_info.html', painting = painting[0], users = users)

@app.route('/painting/purchase/<int:num4>')
def purchase(num4):
    data = {
        'id': num4
    }
    Painting.purchase(data)
    data2 = {
        'users': session['id'],
        'paintings': num4
    }
    User.purchase(data2)
    s = f'/painting/{num4}'
    return redirect(s)