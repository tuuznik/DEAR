import os
from datetime import datetime
from forms import LoginForm, RegistrationForm
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)

user = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
db_host = os.environ['DB_HOST']

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{db_host}:5432/dear_db' # 'sqlite:///mydb.db''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), index=True, unique=True)
  email = db.Column(db.String(150), unique = True, index = True)
  password_hash = db.Column(db.String(150))
  registration_date = db.Column(db.DateTime(), default = datetime.utcnow, index = True)

  def set_password(self, password):
        self.password_hash = generate_password_hash(password)

  def check_password(self,password):
        return check_password_hash(self.password_hash,password)

db.create_all()
db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=["GET"])
def main_page():
    return render_template("index.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else: 
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                next = request.args.get("next")
                return redirect(next or '/')
            flash('Invalid email address or Password.')
        return render_template('login.html', form=form)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('sign_up.html', form=form)
    else: 
        if form.validate_on_submit():
            user = User(username =form.username.data, email = form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('sign_in'))
        else:
            return render_template('sign_up.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)