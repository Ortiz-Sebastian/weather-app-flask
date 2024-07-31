from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, EqualTo,Email, InputRequired, ValidationError
from weather.weatherData import Weather,ApiKey

class registrationForm(FlaskForm):
    userName = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField('Email',validators=[DataRequired(), Length(min=2, max=20),Email()])
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