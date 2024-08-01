from weather import db,loginManager
from flask_login import UserMixin

@loginManager.user_loader
def Loaduser(userId):
     return User.query.get(userId)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    citys = db.relationship('SavedCitys',backref='user',lazy=True)

    def __repr__(self):
         return f"User('{self.username}','{self.email}')"
class SavedCitys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, unique=True, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    unit = db.Column(db.String(), nullable = False)
    def __repr__(self):
         return f"User('{self.city}')"
