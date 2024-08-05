
from flask import render_template,url_for,flash,redirect,request

from weather import app,db,bcrypt
from weather.user import User, SavedCitys
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
        global tdData 
        tdData = weather.getdata(form.city.data,form.units.data)\
        
        global currUnit
        currUnit = form.units.data

        tdData['main']['temp'] = round(tdData['main']['temp'])
        tdData['main']['feels_like'] = round(tdData['main']['feels_like'])

        global tdTime
        tdTime = weather.getTime(tdData["dt"],True)
        global imageUrl
        imageUrl = weather.getImageUrl(tdData['weather'][0]['icon'])
        global sunrise
        sunrise = weather.getTime(tdData['sys']['sunrise'], True)
        sunrise = sunrise[17:]

        global sunset
        sunset = weather.getTime(tdData['sys']['sunset'], True)
        sunset = sunset[17:]
        return redirect(url_for('weatherPage'))
     
    return render_template("home.html", form = form)

@app.route("/weather",methods=['GET','POST'])
@login_required
def weatherPage():
    buttonShow = True
    if SavedCitys.query.filter_by(city=tdData['name']).first():
        buttonShow = False

    if request.method == "POST":
       city = SavedCitys(city=tdData['name'],user_id=current_user.id,unit=currUnit)
       db.session.add(city)
       db.session.commit()
       flash(f'{tdData['name']} added to your saved citys', 'success')
       return redirect(url_for('weatherPage'))
    return render_template("weather.html",title='city', data = tdData,time = tdTime,url = imageUrl, sunrise=sunrise, sunset=sunset, buttonShow=buttonShow)

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