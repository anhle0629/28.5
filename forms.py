from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import input_required
from wtforms.validators import Length, NumberRange, Email, Optional

class UserForm(FlaskForm):
    username = StringField("Username", validators=[input_required(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[input_required(), Length(min=6, max=55)])
    email = StringField('Email', validators=[input_required(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[input_required(), Length(max=30)])
    last_name = StringField("Last Name", validators=[input_required(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[input_required(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[input_required(), Length(min=6, max=55)])

class DeleteForm(FlaskForm):
    "intentionally leaving blank!"

class feedbackform(FlaskForm):
    title = StringField("Title", validators=[input_required(), Length(max=100)])
    content = StringField("Content", validators=[input_required()])