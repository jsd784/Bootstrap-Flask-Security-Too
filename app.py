import os

from flask import Flask, render_template
from flask_security import Security, current_user, auth_required,roles_required, hash_password, \
                            SQLAlchemySessionUserDatastore, UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, \
                       String, ForeignKey
from flask_mail import Mail,Message
from customforms import ExtendedRegisterForm

# Create app
app = Flask(__name__)

# Generate a nice key using secrets.token_urlsafe()
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'r-p0L-3zrfuEksIvwV1GVbfmeYF6qRiqmoPoJfn1iYk')
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get("SECURITY_PASSWORD_SALT", '291968833846239932315041384143203481776')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/test.db'

#User Behavior Config
app.config['SECURITY_TRACKABLE'] = True

# Create database connection object
db = SQLAlchemy(app)

class RolesUsers(db.Model):
    __tablename__ = 'app_roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('app_user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('app_role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'app_role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

class User(db.Model, UserMixin):
    __tablename__ = 'app_user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255))
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='app_roles_users',
                         backref=backref('users', lazy='dynamic'))

# Configure Mail SMTP object
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['MAIL_SERVER'] = "mail.pacificasolutions.com"
app.config['MAIL_PORT'] = "465"
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get("GATOR_MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("GATOR_MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = "no-reply@pacificasolutions.com"

mail = Mail(app)

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore,register_form=ExtendedRegisterForm)


# # Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email="jsd784@yahoo.com", password=hash_password("yourpassword"),firstname="Jasvir",lastname="Dhillon")
#     db.session.commit()

# Views
@app.route("/")
@auth_required()
def home():
    return render_template("index.html",name=current_user.firstname)

# Views
@app.route("/protected")
@roles_required('admin')
def protected():
    return render_template("protected.html",name=current_user.firstname)

if __name__ == '__main__':
    app.run(debug=True)