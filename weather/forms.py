from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, EqualTo,Email, InputRequired, ValidationError
from weather.weatherData import Weather,ApiKey
from weather.user import User
from weather import db

def checkUsernamexist(self,field):
    if User.query.filter_by(username = field.data).first():
        raise ValidationError("username already exist")

def checkEmailExist(self,field):
    if User.query.filter_by(email = field.data).first():
        raise ValidationError("email already exist")


class registrationForm(FlaskForm):
    userName = StringField('Username',validators=[DataRequired(), Length(min=2, max=20),checkUsernamexist])
    email =  StringField('Email',validators=[DataRequired(), Length(min=2, max=20),Email(),checkEmailExist])
    password = PasswordField('Password', validators= [DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

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