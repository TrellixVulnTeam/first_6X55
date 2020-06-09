from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, email_validator, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email(email_validator)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email(email_validator)])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                          'Username must have onlu letters, numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message="Passswords must match")])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data.lower()).first():
            raise ValidationError('Username already in use')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Enter your password', validators=[DataRequired()])
    password = PasswordField('Enter new password', validators=[DataRequired(),
                                                     EqualTo('password2', message="Passswords must match")])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    sibmit = SubmitField('Submit password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email(email_validator)])
    submit = SubmitField('Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter new password', validators=[DataRequired(),
                                                               EqualTo('password2', message="Passswords must match")])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    sibmit = SubmitField('Submit password')


class ChangeEmailForm(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Length(1, 64), Email(email_validator)])
    password = PasswordField('Your password', validators=[DataRequired()])
    submit = SubmitField('Change')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered')