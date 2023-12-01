from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = StringField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

