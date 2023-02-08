__author__ = "Allan Lindgren"

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextField, ValidationError
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
            raise ValidationError('This user name has been used. Please choose another.')


class LoginForm(FlaskForm):
    first_name = StringField('First Name')
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    submit = SubmitField('Search')


class NoteForm(FlaskForm):
    note_date = DateField('Note date', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Save')
    #  add payment todo

class NewNote(FlaskForm):
    note_date = DateField('Notedate',validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()], widget=TextArea())
    
    submit = SubmitField('Save')
    #  add payment todo

class ClientForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name')
    email = StringField('email')
    phone = StringField('Phone')
    street1 = StringField('Address')
    city = StringField('City')
    zipcode = StringField('zipcode')
    state = StringField('State')
    age = StringField('Age')
    submit = SubmitField('Update')


class ClientNew(FlaskForm):
    first_name = StringField('Firs tname', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('email')
    phone = StringField('Phone')
    street1 = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('zipcode')
    submit = SubmitField('Save')

class ClientUpdate(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('email')
    phone = StringField('Phone')
    street1 = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('zipcode')
    submit = SubmitField('Update')