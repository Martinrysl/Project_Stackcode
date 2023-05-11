from flask import Flask, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, Pagination
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import Login, AddUser, SearchUser
from flask_bootstrap import Bootstrap
import werkzeug.security
from flask_bcrypt import Bcrypt
from os import getenv
import datetime
from dotenv import load_dotenv
from func_jwt import write_token, auth_token

app = Flask(__name__)
# Se crea la Secret Key para el uso del token y el CSRF Protection
app.config['SECRET_KEY'] = getenv("SECRET")
# Se Conecta la base de datos de mysql Workbench a la app mediante el usuario root de mi local instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oligopolio2@localhost/stackcode_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)


# Creacion de la Base de Datos con los elementos requeridos
class Database(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


@login_manager.user_loader
def load_user(user_id):
    return Database.query.get(int(user_id))


# Utilice dos tipos de rutas para add y login para que se pueda hacer mediante el API y la pagina HTML
@app.route('/')
def home():
    return render_template('index.html')


# Adding new user in JSON by POSTMAN
@app.route("/add", methods=["POST"])
def add():
    # Se encripta la password para generar una password_hash y tenga mas seguridad el API usando el metodo pbkdf2:sha256
    password_hash = generate_password_hash(password=request.json.get('password'), method='pbkdf2:sha256', salt_length=8)
    new_user = Database(
        name=request.json.get('name'),
        email=request.json.get('email'),
        password=password_hash,
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new user."})


# Se agrega el usuario mediante la ruta /adduser de igual forma con password_hash
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

        password_hash = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8)

        new_user = Database(
            name=name,
            email=email,
            password=password_hash
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html", form=form)


# Se realiza el inicio de sesion mediante POSTMAN en la ruta /loginapi
@app.route('/loginapi', methods=['GET', 'POST'])
def login_api():
    email = request.json.get('email')
    password = request.json.get('password')
    # Se busca el email del usuario escrito anteriormente en la base de datos para hacer match
    user_login = Database.query.filter_by(email=email).first()
    if not user_login:
        flash('Wrong email', 'error')
        return redirect(url_for("login"))
    # Se checa mediante el email en la DB la password, se vuelve a encriptar y se comprueba que sean las mismas.
    elif not werkzeug.security.check_password_hash(pwhash=user_login.password, password=password):
        flash('Wrong password', 'error')
        return redirect(url_for('login'))
    else:
        flash('Your have logged in successfully', 'success')
        return write_token(data=request.get_json())


# Se realiza el inicio de sesion mediante la pagina HTML ruta /login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user_login = Database.query.filter_by(email=email).first()

        if not user_login:
            flash('Wrong email', 'error')
            return redirect(url_for("login"))

        elif not werkzeug.security.check_password_hash(pwhash=user_login.password, password=password):
            flash('Wrong password', 'error')

            return redirect(url_for('login'))
        else:
            flash('Your have logged in successfully', 'success')
            return "User logged Successfully"

    return render_template('login.html', form=form)


# Muestra 10 registros por pagina de los usuario en la base de datos de forma ascendiente
@app.route('/userslist', methods=['GET', 'POST'])
def get_all_users():

    page = request.args.get('page', 1, type=int)
    per_page = 10
    users = Database.query.order_by(Database.created_at.asc()).paginate(page=page, per_page=per_page)

    return render_template("users.html", users=users)


# Se busca el usuario mediante el email o username
@app.route('/search', methods=['GET', 'POST'])
def search_users():
    query = request.args.get('query')
    if not query:
        return jsonify(error='No query specified')
    # Se filtra el email o username para encontrar sus datos en la base de datos
    users = Database.query.filter(
        (Database.name.ilike(f'%{query}%')) | (Database.email.ilike(f'%{query}%'))
    ).all()

    if not users:
        return jsonify(error='No matching users found')
    # Como resultado mostrara el id, name y email
    results = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(results=results)


# Se busca al Usuario mediante el ID
@app.route('/read', methods=['GET', 'POST'])
def search_user_id():
    # En POSTMAN: 'id' es el elemento Key y el elemento Value seria algun ID de usuario
    query = request.args.get('id')
    if not query:
        return jsonify(error='No query specified')
    # Se filtra el usuario mediante el ID para encontrarlo
    users = Database.query.filter(
        (Database.id.ilike(f'%{query}%')) | (Database.id.ilike(f'%{query}%'))
    ).all()

    if not users:
        return jsonify(error='No matching users found')

    results = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return jsonify(results=results)


# Se Actualiza al usuario mediante el id usando el metodo PATCH
@app.route("/update-username/<int:user_id>", methods=["PATCH"])
def patch_name(user_id):
    # En POSTMAN: 'new_name' es el elemento Key y el elemento Value seria algun ID de usuario
    # 'http://127.0.0.1:9090/update-username/1' de esta forma se inserta y despues se pone el Key y Value si queremos
    # editar el usuario de id=1= Martinis
    new_name = request.args.get("new_name")
    user = db.session.query(Database).get(user_id)
    if user:
        user.name = new_name
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the name."})
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."})


# Se actualiza un email de usuario a través de su ID.
@app.route("/update-email/<int:user_id>", methods=["PATCH"])
def patch_email(user_id):
    # En POSTMAN: 'new_email' es el elemento Key y el elemento Value seria algun ID de usuario
    # 'http://127.0.0.1:9090/update-email/1' de esta forma se inserta y despues se pone el Key y Value si queremos
    # editar el email de id=1= martinis@outlook.com
    new_email = request.args.get("new_email")
    user = db.session.query(Database).get(user_id)
    if user:
        user.email = new_email
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the email."})
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."})


# Eliminar un usuario a través de su ID.
@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    # http://127.0.0.1:9090/delete_user/1 , de esta forma se inserta, sin agregar values, de forma que
    # nos indica que se borrara el usuario con id = 1, cumpliendo el objetivo de este punto
    # Aunque en proyectos anteriores le pongo un token para que no se pueda borrar tan facilmente o
    # solo con permisos de administrador para mayor seguridad
    user = db.session.query(Database).get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(response={"success": "Successfully deleted the User from the database."}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a User with that id was not found in the database."}), 404


# Endpoint para Verificar el token
@app.route("/verify", methods=['GET', 'POST'])
def verify():
    # Del return que da, se omite el "Bearer" y nos deja el valor del token mediante la funcion de 'split'
    token = request.headers['Authorization'].split(" ")[1]
    return auth_token(token, output=True)


if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, port=9090)


