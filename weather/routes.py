
from flask import render_template,url_for,flash,redirect
from weather.user import User
from weather import app,db,bcrypt
from weather.forms import registrationForm, logInForm, cityData
from weather.weatherData import Weather

@app.route("/",methods=['GET','POST'])
def home():
    form = cityData()
    weather = Weather()
    if form.validate_on_submit():
        tdData = weather.getdata(form.city.data,form.units.data)
        return redirect(url_for('weatherPage'))
     
    return render_template("home.html", form = form)

@app.route("/weather",methods=['GET','POST'])
def weatherPage():
     return  render_template("weather.html",title='city')

@app.route("/register", methods=['GET','POST'])
def register():
    form = registrationForm()
    if  form.validate_on_submit():
        hashPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.userName.data,email = form.email.data,password = hashPass)
        flash(f'Account created for {form.userName.data}', 'success')
        return redirect(url_for('home'))
    return  render_template("registration.html", title='register',form = form)
     
@app.route("/login", methods=['GET','POST'])
def login():
     form = logInForm()
     if form.validate_on_submit():
        if form.userName.Data == 'anon@gmail.com' and form.password.data =="deez":
            flash('welcome back ' + form.userName.data, 'success')
            return redirect(url_for('home'))
        else:
             flash('Error please check your username and password again','danger')  
     return  render_template("logIn.html", title='login',form = form)