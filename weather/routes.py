
from flask import render_template,url_for,flash,redirect,request

from weather import app,db,bcrypt
from weather.user import User
from weather.forms import registrationForm, logInForm, cityData
from weather.weatherData import Weather
from flask_login import login_user,current_user,logout_user,login_required

with app.app_context():
    db.create_all()

@app.route("/",methods=['GET','POST'])
def home():
    form = cityData()
    weather = Weather()
    if form.validate_on_submit():
        tdData = weather.getdata(form.city.data,form.units.data)
        return redirect(url_for('weatherPage'))
     
    return render_template("home.html", form = form)

@app.route("/weather",methods=['GET','POST'])
@login_required
def weatherPage():
    return render_template("weather.html",title='city')

@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = registrationForm()
    if  form.validate_on_submit():
        hashPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        user = User(username = form.userName.data,email = form.email.data,password = hashPass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.userName.data}', 'success')
        return redirect(url_for('login'))
    return  render_template("registration.html", title='register',form = form)
     
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
      
    form = logInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.userName.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            nextPage = request.args.get('next')
            if nextPage:
                return redirect(nextPage)
            else:
                return redirect(url_for('home'))   
        else:     
            flash('Error please check your username and password again','danger')  
    return  render_template("logIn.html", title='login',form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))   