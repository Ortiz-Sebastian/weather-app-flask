from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,PasswordField, SubmitField,BooleanField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, EqualTo,Email, InputRequired, ValidationError
from weather.weatherData import Weather,ApiKey
from weather.user import User
from weather import db

def checkUsernamexist(self,field):
    if User.query.filter_by(username = field.data).first():
        raise ValidationError("username already exist")

def checkEmailexist(self,field):
    if User.query.filter_by(email = field.data).first():
        raise ValidationError("email already exist")
    
def checkEmailNotExist(self,field):
    if User.query.filter_by(email = field.data).first() is None:
        raise ValidationError("email is not registered to an account")


def checkUsernamexistUpdate(self,field):
    if field.data != current_user.username:
        if User.query.filter_by(username = field.data).first():
            raise ValidationError("username already exist")

def checkEmailexistUpdate(self,field):
    if field.data != current_user.email:
        if User.query.filter_by(email = field.data).first():
            raise ValidationError("email already exist")
    
class registrationForm(FlaskForm):
    userName = StringField('Username',validators=[DataRequired(), Length(min=2, max=20),checkUsernamexist])
    email =  StringField('Email',validators=[DataRequired(), Length(min=2, max=50),Email(),checkEmailexist])
    password = PasswordField('Password', validators= [DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')



class updateForm(FlaskForm):
    userName = StringField('Username',validators=[DataRequired(), Length(min=2, max=20),checkUsernamexistUpdate])
    email =  StringField('Email',validators=[DataRequired(), Length(min=2, max=50),Email(),checkEmailexistUpdate])
    submit = SubmitField('Update')

class logInForm(FlaskForm):
    userName = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators= [DataRequired()])
    remember = BooleanField("remember me")
    submit = SubmitField('Log in')



class cityData(FlaskForm):
    city = StringField('City',validators=[DataRequired(),InputRequired()])
    units = RadioField('Units', choices=['Metric','Imperial'],validators=[DataRequired(),InputRequired()])
    enter = SubmitField("Enter")

    def validate_city(self,field):
        w= Weather()
        data = w.getdata(field.data,"imperial")
        if data['cod'] == '404':
            raise ValidationError('City does not exist')
        
class RequestReset(FlaskForm):
    email =  StringField('Email',validators=[DataRequired(), Length(min=2, max=50),Email(),checkEmailNotExist])
    enter = SubmitField("Send Request")

class ChangePassword(FlaskForm):
    password = PasswordField('Password', validators= [DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    enter = SubmitField("Change Password")