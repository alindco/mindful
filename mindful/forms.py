__author__ = "Allan Lindgren"

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextField, ValdationError
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import TextArea
from mindful.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_user_name(self,username):
        user = User.query_by(username=username.data).first()
        if user:
            raise ValidationError('This user name has been used. Please choose another.'


class LoginForm(FlaskForm):
    first_name = StringField('FirstName')
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    first_name = StringField('Firstname')
    last_name = StringField('Lastname')
    submit = SubmitField('Search')


class NoteForm(FlaskForm):
    note_date = DateField('Note date')
    description = TextField('Description', widget=TextArea())
    submit = SubmitField('Save')
    #  add payment todo

class NoteNew(FlaskForm):
    note_date = DateField('Note date')
    description = TextField('Description', widget=TextArea())
    
    submit = SubmitField('Save')
    #  add payment todo

class ClientForm(FlaskForm):
    first_name = StringField('Firstname')
    last_name = StringField('Lastname')
    email = StringField('email')
    phone = StringField('Phone')
    street1 = StringField('Address')
    city = StringField('City')
    zipcode = StringField('zipcode')
    state = StringField('State')
    age = StringField('Age')

    submit = SubmitField('Update')


class ClientNew(FlaskForm):
    first_name = StringField('Firstname', validators=[DataRequired()])
    last_name = StringField('Lastname')
    email = StringField('email')
    phone = StringField('Phone')
    street1 = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('zipcode')
    submit = SubmitField('Save')
