from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
 
db = SQLAlchemy()
 
class UserModel(db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True)
    phone = db.Column(db.String(20), unique=True)
    client_token = db.Column(db.String(80), unique=True)
    secret_secret = db.Column(db.String(80), unique=True)
 
    def __init__(self, username, email, password, phone, client_token, secret_secret):
        self.username = username
        self.email = email
        self.password = password
        self.client_token = client_token
        self.secret_secret = secret_secret
        self.phone = phone
     
    def json(self):
        return {"username":self.username, "email":self.email , "client_token":self.client_token, "secret":self.secret_secret, "phone": self.phone}
    
    def get_password(self):
        return {"password":self.password, "email": self.email}
    
class OtpUserModel(db.Model):
    __tablename__ = 'otpUsers'

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, ForeignKey("users.id"))
    otp_code = db.Column(db.String(6))

    def __init__(self, userId, otp_code):
        self.userId = userId
        self.otp_code = otp_code

    def json(self):
        return {"userId":self.userId, "otp":self.otp_code}
