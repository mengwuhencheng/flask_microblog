from flask_wtf import Form
from wtforms import ValidationError
from wtforms import TextField, BooleanField,PasswordField,SubmitField,StringField
from wtforms.validators import Required,Length,Email,Regexp, EqualTo
from ..models import User

class LoginForm(Form):
    email = StringField('Email', validators = [Required(),Length(1,64),Email()])
    password = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Remember Me', default = False)
    submit = SubmitField('Log In')

class RegistrationForm(Form):
    """docstring for RegistrationForm"""
    email = StringField('Email', validators = [Required(),Length(1,64),Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Username must have only letters, ''numbers, dots or underscores')])
    password = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
class ChangePassword(Form):
    """docstring for ModifyPassword"""
    old_password = PasswordField('Old password', validators=[Required()])
    new_password = PasswordField('New Password', validators=[Required(), EqualTo('new_password2', message='Passwords must match.')])
    new_password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(Form):
    email = StringField('Email', validators = [Required(),Length(1,64),Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
