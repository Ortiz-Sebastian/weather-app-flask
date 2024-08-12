from weather import db,loginManager,app
from flask_login import UserMixin
from itsdangerous import TimedSerializer as Serializer

@loginManager.user_loader
def Loaduser(userId):
     return User.query.get(userId)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    citys = db.relationship('SavedCitys',backref='user',lazy=True)

    def getResetToken(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'userid': self.id})
    @staticmethod
    def verifyResetToken(token, max_age=1600):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            userid = s.loads(token,max_age=max_age)['userid']
        except:
            return None
        return User.query.get(userid)
        
    def __repr__(self):
         return f"User('{self.username}','{self.email}')"
class SavedCitys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    unit = db.Column(db.String, nullable = False)
    def __repr__(self):
         return f"User('{self.city}')"
