from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oligopolio2@localhost/stackcode_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    return' Hey'


@app.route('/add', methods=["POST"])
def add_user():
    new_user = Database(
        name=request.json.get('name'),
        email=request.json.get('email'),
        password=request.json.get('password'),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(response={"success": "Successfully added new User."})


if __name__ == "__main__":
    app.run(debug=True, port=9090)

