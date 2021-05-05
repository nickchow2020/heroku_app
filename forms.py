from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Email

class Register(FlaskForm):
    """Register Form"""

    username = StringField("Username",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    email = StringField("Email",validators=[Email(),InputRequired()])
    first_name = StringField("First Name",validators=[InputRequired()])
    last_name = StringField("Last Name",validators=[InputRequired()])

class Login(FlaskForm):
    """Login Form"""

    username = StringField("Username",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])

class Feedback(FlaskForm):
    """Feedback Form"""
    title = StringField("Title",validators=[InputRequired()])
    content = StringField("Content",validators=[InputRequired()])

