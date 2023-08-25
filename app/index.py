from flask import Flask, redirect, url_for, request
from flask_restful import Api, Resource, reqparse
from flask_migrate import Migrate
from models import db, UserModel, OtpUserModel
from passwordGen import generate_password
from otpGen import crearKey
import smtplib, ssl
from twilio.rest import Client
import base64
from datetime import date, datetime


account_sid = 'ACad7bb08d5242ed707d01a5ac72fab067'
auth_token = '6992de4509ba55d64a09b0ae4b7b8b5c'
client = Client(account_sid, auth_token)

app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credentials_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

def create_app():
    create_table()

def create_table():
    db.create_all()

# Function to test api connection
@app.route("/test_connection", methods = ['GET'])
def test_connection():
    return "Alive..."

# Function to generate an OTP code for authentication
@app.route("/generate_otp", methods = ['GET'])
def generate_otp():
    otp_code = crearKey()
    json = { "otp_code" : otp_code }
    return json

# Function to generate an OTP code for authentication
@app.route("/generate_password", methods = ['GET'])
def generate_pwd():
    pwd = generate_password()
    return pwd

# Function to send
@app.route("/send_message", methods = ['POST'])
def send_message():
    otp_code = crearKey()
    sms_otp = 'This is your generated otp code: ' + otp_code 
    message = client.messages.create(
         body=sms_otp,
         from_='+17067103642',
         to='+50662573259'
     )
    return message.sid

@app.route("/send_email", methods = ['POST'])
def send_email():
    message = "This is your generated email with your generated otp code: " + crearKey()
    gmail_user = 'fortitechcr@gmail.com'
    gmail_password = 'F0rtit3ch.'

    sent_from = gmail_user
    to = ['mkjg16@gmail.com']
    subject = 'OMG Super Important Message'

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, message)
    server.close()

    print ('Email sent!')
    return message


@app.route("/send_magic_email", methods = ['POST'])
def send_magic_email():
    now = 'expiration=' + datetime.now().strftime("%d_%m_%Y-%H_%M_%S") + '&'
    email = request.json
    email = list(email.values())
    email_param = 'email=' + email[0]
    text_to_encode = now + email_param
    text_to_encode_bytes = text_to_encode.encode('ascii')
    base64_bytes = base64.b64encode(text_to_encode_bytes)
    base64_string = base64_bytes.decode("ascii")
    magic_link = '?magic_link=' + base64_string
    return magic_link

@app.route("/sign_in", methods = ['POST'])
def sign_in():
    return True

@app.route("/login", methods = ['POST'])
def login():
    if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
    else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route("/forgot_password", methods = ['POST'])
def forgot_password():
    return "Hello, World!"


# CRUD User
class UsersView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
    )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
    )'''
 
    def get(self):
        users = UserModel.query.all()
        return {'Users':list(x.json() for x in users)}
 
    def post(self):
        data = request.get_json()
        #data = UsersView.parser.parse_args()
 
        new_user = UserModel(data['username'],data['email'] ,data['password'], data['phone'], data['client_token'], data['client_secret'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.json(),201
 
 
class UserView(Resource):
    '''
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help = "Can't leave blank"
        )
    parser.add_argument('author',
        type=str,
        required=True,
        help = "Can't leave blank"
        )'''
 
    def get_by_username(self,username):
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user.json()
        return {'message':'User not found'},404
    
    def get_by_email(self,email):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return user.json()
        return {'message':'User not found'},404
 
    def put(self,username,password, email, phone):
        data = request.get_json()
        #data = UserView.parser.parse_args()
 
        user = UserModel.query.filter_by(username=username).first()
 
        if user:
            user.price = data["price"]
            user.author = data["author"]
        else:
            user = UserModel(username=username,**data)
 
        db.session.add(user)
        db.session.commit()
 
        return user.json()
 
    def delete(self,name):
        user = UserModel.query.filter_by(username=name).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message':'Deleted'}
        else:
            return {'message': 'user not found'},404
 
api.add_resource(UsersView, '/users')
api.add_resource(UserView,'/user/<string:name>')
 
app.debug = True

if __name__ == '__main__':
    app.run(host='localhost', port=5001)