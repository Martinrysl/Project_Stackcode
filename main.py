from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import Login, AddUser
from flask_bootstrap import Bootstrap
import werkzeug.security
from functools import wraps
import os
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oligopolio2@localhost/stackcode_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)


class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@app.route('/')
def index():
    return' Welcome'


@app.route('/adduser', methods=['GET', 'POST'])
def register():
    form = AddUser()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        if Database.query.filter_by(email=email).first():
            flash(message="You have already signed up with that email", category="danger")
            return redirect(url_for("login"))

        new_user = Database(
            name=name,
            email=email,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return "User Added Successfully"

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_login = Database.query.filter_by(email=email).first()
        password_login = Database.query.filter_by(password=password).first()
        if not user_login:
            flash(message='That email does not exist, please register')
            return redirect(url_for("login"))

        elif not password_login:
            flash(message="Invalid password", category="danger")
            print('Wrong Password')
            return redirect(url_for('login'))
        else:

            return "User logged Successfully"

    return render_template('login.html', form=form)


if __name__ == "__main__":
    app.run(debug=True, port=9090)

