from crypt import methods
import os
from flask import Blueprint, redirect, render_template, abort, request, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from event_app.models import User
from event_app import app, db

users = Blueprint('users', __name__)

@users.route('/login', methods=['GET', 'POST'])
def login():
  if (request.method == 'GET'):
    return(render_template('users/login.html'))
  else:
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    if (not user or not check_password_hash(user.password, password)):
      flash('Check email or password and try again', category='danger')
      return(redirect(url_for('users.login')))

    login_user(user, True)
    return(redirect('/'))

@users.route('/signup', methods=['GET', 'POST'])
def signup():
  if (request.method == 'GET'):
    return(render_template('users/signup.html'))
  else:
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if (user):
      flash('Email address already exists', category='danger')
      return redirect(url_for('users.signup'))

    new_user = User(
      name=name,
      email=email,
      password=generate_password_hash(password, method='sha256'),
    )
    
    db.session.add(new_user)
    db.session.commit()

    return(redirect(url_for('users.login')))

@users.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return(redirect('/'))
