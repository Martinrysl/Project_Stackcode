from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, Pagination
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import Login, AddUser, SearchUser
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

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

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


@app.route('/userslist', methods=['GET', 'POST'])
def get_all_users():

    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = Database.query.order_by(Database.created_at.asc()).paginate(page=page, per_page=per_page)

    return render_template("users.html", users=users)


@app.route('/search', methods=['GET', 'POST'])
def search_users():
    query = request.args.get('query')
    if not query:
        return jsonify(error='No query specified')

    users = Database.query.filter(
        (Database.name.ilike(f'%{query}%')) | (Database.email.ilike(f'%{query}%'))
    ).all()

    if not users:
        return jsonify(error='No matching users found')

    results = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(results=results)


@app.route('/read', methods=['GET', 'POST'])
def search_user_id():
    query = request.args.get('id')
    if not query:
        return jsonify(error='No query specified')

    users = Database.query.filter(
        (Database.id.ilike(f'%{query}%')) | (Database.id.ilike(f'%{query}%'))
    ).all()

    if not users:
        return jsonify(error='No matching users found')

    results = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(results=results)


@app.route("/update-username/<int:user_id>", methods=["PATCH"])
def patch_name(user_id):
    new_name = request.args.get("new_name")
    user = db.session.query(Database).get(user_id)
    if user:
        user.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the name."})
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."})


@app.route("/update-email/<int:user_id>", methods=["PATCH"])
def patch_email(user_id):
    new_email = request.args.get("new_email")
    user = db.session.query(Database).get(user_id)
    if user:
        user.email = new_email
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the email."})
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."})


@app.route("/delete_user/<int:id>", methods=["DELETE"])
def delete(user_id):
    user = Database.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."}), 404



if __name__ == "__main__":
    app.run(debug=True, port=9090)

