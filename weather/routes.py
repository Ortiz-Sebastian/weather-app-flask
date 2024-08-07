
from flask import render_template,url_for,flash,redirect,request, abort
import time
from weather import app,db,bcrypt
from weather.user import User, SavedCitys
from weather.forms import registrationForm, logInForm, cityData, updateForm
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
        tdData = weather.getdata(form.city.data,form.units.data)
        
        global currUnit
        currUnit = form.units.data

        global tdTime
        tdTime = weather.getTime(time.time(),True)

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
    nextClicked = False
    prevClicked = False
    w = Weather()
    weekData = w.getweeklydata(tdData['coord']['lon'],tdData['coord']['lat'], currUnit)

    if SavedCitys.query.filter_by(city=tdData['name']).first():
        buttonShow = False
    
    if request.method == "POST":
        if 'add' in request.form:
            city = SavedCitys(city=tdData['name'],user_id=current_user.id,unit=currUnit)
            db.session.add(city)
            db.session.commit()
            flash(f'{tdData['name']} added to your saved citys', 'success')
            return redirect(url_for('weatherPage'))

        if 'day1' in request.form:
            return "Button 1 WORKED"
        if 'next' in request.form:
           nextClicked = True
        if 'prev' in request.form:
           prevClicked = True

    return render_template("weather.html",title='city', data = tdData,time = tdTime,url = imageUrl, sunrise=sunrise, sunset=sunset, buttonShow=buttonShow,wData = weekData, nextClicked=nextClicked,prevClicked=prevClicked)

@app.route("/mycitys",methods=['GET','POST'])
@login_required
def mycitys():
    w= Weather()
    
    citysInfo =[]
    numIunit = 0
    numMunit = 0

    cityData = SavedCitys.query.all()
    if 'Imperial' in request.form:
           freqUnit = "Imperial"
    elif 'Metric' in request.form:
           freqUnit = "Metric"
    else:
        for city in cityData:
            if city.unit == "Imperial":
                numIunit = numIunit + 1
            else:
                numMunit = numMunit + 1
            
        if numIunit > numMunit:
            freqUnit = 'Imperial'
        else:
            freqUnit = 'Metric'
    
    for city in cityData:
        info = w.getdata(city.city,freqUnit)
        info['dt'] = w.getTime(time.time(),True)
        info['dt'] = info['dt'][17:]
        info['weather'][0]['icon'] = w.getImageUrl(info['weather'][0]['icon'])
        dict = {'time': info['dt'], 'url':info['weather'][0]['icon'], 'temp': info['main']['temp'],'max': info['main']['temp_max'], 'min': info['main']['temp_min'],'country': info['sys']['country'],'description': info['weather'][0]['description'], 'cityInfo':city  }
        citysInfo.append(dict)

    

    return render_template("mycitys.html", citysData=citysInfo, numIunit=numIunit, numMunit=numMunit)

@app.route("/account",methods=['GET','POST'])
@login_required
def account():
    form = updateForm()
    if form.validate_on_submit():
        current_user.username = form.userName.data
        current_user.email = form.email.data
        db.session.commit()
        flash("account has been updated",'success')
        return redirect(url_for("account"))
    elif request.method == 'GET':
        form.userName.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html",form=form)

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


@app.route("/delete/<int:cityid>",methods=['POST'])
@login_required
def delete(cityid):
    city = SavedCitys.query.get_or_404(cityid)
    if city.user != current_user:
        abort(403)
    db.session.delete(city)
    db.session.commit()
    flash('city has been deleted', 'success')
    return redirect(url_for('mycitys'))

