from datetime import datetime,timedelta
import os, json, jwt
from hashlib import md5
from time import time
from flask import current_app, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model,UserMixin):
    __searchable__ = ['institution','department','programme','username']

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32),nullable=False)
    lastname = db.Column(db.String(32),nullable=False)
    username = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    pwhash = db.Column(db.String(128))
    institution = db.Column(db.String(120),nullable=False, index=True)
    department = db.Column(db.String(64),nullable=False, index=True)
    programme = db.Column(db.String(64),nullable=False, index=True)
    registered_on = db.Column(db.DateTime, nullable=False) 
    projects = db.relationship('Project', backref='author', lazy='dynamic')


    def __init__(self,firstname, lastname, username, email, password, institution, department, programme):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.pwhash = generate_password_hash(password)
        self.institution = institution
        self.department = department
        self.programme = programme
        self.registered_on = datetime.utcnow()


    def verify_password_from_db(self, password):
        return check_password_hash(self.password_hash, password)


    def setResetPassword(self,password):
        self.pwhash = generate_password_hash(password)

        

    def save(self):
        """
        Persist the user in the database
        """
        db.session.add(self)
        db.session.commit()

        return self


    def generate_auth_token(self, expires_in=3600):
        """
        generate user specific token to authenticate requests for 1hr
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(seconds=expires_in),
                'iat': datetime.utcnow(),
                'sub': self.id
            }

            return jwt.encode(
                    payload,
                    current_app.config['SECRET_KEY'],
                    algorithm='HS256'
                ).decode('UTF-8')
        except Exception as e:
            return e


        

    @staticmethod
    def verify_auth_token(token):
        """
        Decoding the token to get the payload and then return the user
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
            user = User.query.filter_by(id=payload['sub']).first()
            return user
        except :
            return None




    def getPasswordResetToken(self):
            s = Serializer( current_app.config['SECRET_KEY'], expires_in=600)
            return s.dumps({'id': self.id})

    @staticmethod
    def verifyPasswordResetToken(token):
        s = Serializer( current_app.config['SECRET_KEY'])
        try:
            data_id = s.loads(token)['id']
        except:
            return None
        
        user = User.query.get(data_id)
        return user        




class Project(db.Model):
    __searchable__ = ['title','authors']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False, index=True)
    authors = db.Column(db.Text, nullable=False, index=True)
    submit_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    file_data= db.Column(db.LargeBinary)
    filename = db.Column(db.String(120), unique=True,nullable=False)
    modified_at = db.Column(db.DateTime)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def hashFilename(self, filename):
        digest = md5((filename.lower()+str(datetime.utcnow())).encode('utf-8')).hexdigest()
        self.filename = digest

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower()=='pdf'
