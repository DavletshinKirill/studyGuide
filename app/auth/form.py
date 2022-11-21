from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField, PasswordField, StringField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = EmailField("Email: ", validators=[DataRequired()])
    user_name = StringField("Name: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 30), EqualTo('check_password')])
    check_password = PasswordField("Password: ", validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField("Log In")
