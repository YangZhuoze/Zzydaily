from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('Email:', validators = [Required(), Email()])
    password = PasswordField('Password:', validators = [Required()])
    remember = BooleanField('Auto login')
    submit = SubmitField('Login')

class RegisterForm(Form):
    username = StringField('Username:', validators = [Required(), Length(4, 20)])
    email = StringField('Email:', validators = [Email()])
    password = PasswordField('Password:', validators = [Required(), Length(6, 20)])
    confirm = PasswordField('Confirm Password:', validators = [Required(), \
        EqualTo('confirm', message = 'Passwords must match')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already in use.')