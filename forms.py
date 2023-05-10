from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email, Length, ValidationError


class Login(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(granular_message=True, check_deliverability=True)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddUser(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    email = EmailField(label='Email', validators=[DataRequired(), Email(granular_message=True,
                                                                        check_deliverability=True)])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(max=50, min=8,
                                                            message='Password must have at least 8 characters')])
    submit = SubmitField('Add')