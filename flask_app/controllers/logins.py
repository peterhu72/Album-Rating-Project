from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash, url_for, jsonify
import os
from flask_app.models.login import Login

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def users():
    return render_template("register.html", login = Login.get_all())


@app.route('/login/create', methods=['POST'])
def create():
    if not Login.validate_input_reg(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }

    user_id = Login.insert(data)
    session['user_id'] = user_id
    return redirect('/login/display')

@app.route('/login/display')
def display():
    print(session['user_id'])
    return redirect('/dashboard')


@app.route('/login/page', methods=['POST'])
def login():
    if not Login.validate_input_inp(request.form):
        return redirect('/')
    
    data = { 
        "email" : request.form["email"] 
    }
    user_in_db = Login.get_by_email(data)
    
    if not user_in_db:
        flash("Invalid Email/Password", 'err_password_login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        
        flash("Invalid Email/Password", 'err_password_login')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    
    return redirect("/login/display")



