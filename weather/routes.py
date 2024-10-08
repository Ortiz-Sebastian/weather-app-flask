
from flask import render_template,url_for,flash,redirect,request, abort
import time
from weather import app,db,bcrypt,mail
from weather.user import User, SavedCities
from weather.forms import registrationForm, logInForm, cityData, updateForm, RequestReset, ChangePassword
from weather.weatherData import Weather
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message

with app.app_context():
    db.create_all()

@app.route("/",methods=['GET','POST'])
def home():
    form = cityData()
    if form.validate_on_submit():
        return redirect(url_for('weatherPage',city = form.city.data,unit = form.units.data))
     
    return render_template("home.html", form = form)

@app.route("/weather/<string:city>/<string:unit>",methods=['GET','POST'])
@login_required
def weatherPage(city,unit):
    w = Weather()
    tdData = w.getdata(city,unit)
    currUnit = unit

    weekData = w.getweeklydata(tdData['coord']['lon'],tdData['coord']['lat'], currUnit)

    
   

    sunrise = w.getTime(tdData['sys']['sunrise'], weekData[0]['timezone'],True)
    sunrise = sunrise[17:]

    sunset = w.getTime(tdData['sys']['sunset'],weekData[0]['timezone'], True)
    sunset = sunset[17:]

    imageUrl = w.getImageUrl(tdData['weather'][0]['icon'])
    tdTime = w.getTime(time.time(),weekData[0]['timezone'],True)

    buttonShow = True
    nextClicked = False
    prevClicked = False
    
    

    if SavedCities.query.filter_by(city=tdData['name'], user_id=current_user.id).first():
        buttonShow = False
    
    if request.method == "POST":
        if 'add' in request.form:
            city = SavedCities(city=tdData['name'],user_id=current_user.id,unit=currUnit)
            db.session.add(city)
            db.session.commit()
            flash(f'{tdData['name']} added to your saved cities', 'success')
            return redirect(url_for('weatherPage',city=tdData['name'],unit=currUnit))

        if 'day1' in request.form:
            return "Button 1 WORKED"
        if 'next' in request.form:
            nextClicked = True
        if 'prev' in request.form:
            prevClicked = True

    return render_template("weather.html",title='city', data = tdData,time = tdTime,url = imageUrl, sunrise=sunrise, sunset=sunset, buttonShow=buttonShow,
    wData = weekData, nextClicked=nextClicked,prevClicked=prevClicked)

@app.route("/mycities",methods=['GET','POST'])
@login_required
def mycities():
    w= Weather()
    
    citiesInfo =[]
    numIunit = 0
    numMunit = 0

    cityData = SavedCities.query.filter_by(user_id=current_user.id).all()
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
        wdata = w.getweeklydata(info['coord']['lon'],info['coord']['lat'],freqUnit)

        timezone = wdata[0]['timezone']
                         
        info['dt'] = w.getTime(time.time(),timezone,True)
        info['dt'] = info['dt'][17:]
        info['weather'][0]['icon'] = w.getImageUrl(info['weather'][0]['icon'])
        dict = {'time': info['dt'], 'url':info['weather'][0]['icon'], 'temp': info['main']['temp'],'max': info['main']['temp_max'], 'min': info['main']['temp_min'],'country': info['sys']['country'],'description': info['weather'][0]['description'], 'cityInfo':city  }
        citiesInfo.append(dict)

    

    return render_template("mycities.html", citiesData=citiesInfo)

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
    city = SavedCities.query.get_or_404(cityid)
    if city.user != current_user:
        abort(403)
    db.session.delete(city)
    db.session.commit()
    flash('city has been deleted', 'success')
    return redirect(url_for('mycities'))

def sendResetEmail(user):
    token = user.getResetToken()
    msg = Message('Password Reset Request',sender='noreply@weatherapp.com',recipients=[user.email])
    msg.body = f''' click the following link to change your password:
    {url_for('resetToken',token=token, _external=True)}
    '''
    mail.send(msg)
@app.route("/reset-password",methods=['POST','GET'])
def resetRequest():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestReset()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        sendResetEmail(user)
        flash('Password reset instructions has been sent to email','success')
        return redirect(url_for('login'))
    return  render_template("resetRequest.html", title="Reset Password", form =form)

@app.route("/reset-password/<token>",methods=['POST','GET'])
def resetToken(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verifyResetToken(token=token)
    if user is None:
        flash('Invalid Token','danger')
        return redirect(url_for('resetRequest'))
    form = ChangePassword()
    if  form.validate_on_submit():
        hashPass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashPass
        db.session.add(user)
        db.session.commit()
        flash(f'Password has been changed for {user.username}', 'success')
        return redirect(url_for('login'))
    return  render_template("resetToken.html", title="Reset Password", form=form)

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404

@app.errorhandler(403)
def error403(error):
    return render_template('403.html'),403

@app.errorhandler(500)
def error500(error):
    return render_template('500.html'),500