
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY']= '362e9dc97985bf83e5d1d781248111d4'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///user.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from weather import routes