from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class Login(FlaskForm):
    email = StringField("Email", [validators.InputRequired()])
    password = PasswordField("Password", [validators.InputRequired()])