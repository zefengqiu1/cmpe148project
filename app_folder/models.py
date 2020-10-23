from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import time
import datetime
from calendar import calendar
import pandas as pd

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Available(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time(), index=True)
    end_time = db.Column(db.Time(), index=True)
    meeting_length=db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        '''
        this function define the output when print function
        is called on an object of this class

        args:
            none
            
        return:
            A string of message include this meeting's starttime and endtime
        '''
        return 'starttime {}{}'.format(self.start_time,self.end_time)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.Date, index=True)
    name = db.Column(db.String(64), index=True)
    start_time = db.Column(db.Time, index=True)
    end_time = db.Column(db.Time, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(64), index=True)

    def __repr__(self):
        '''
        this function define the output when print function
        is called on an object of this class

        args:
            none
            
        return:
            A string of message include all infomation of this appointment
        '''
        return 'Appointment With {} Date:{} Start Time:{} End Time:{} Description:{}'.format(self.name,self.Date,self.start_time,self.end_time,self.description)
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    mailconfirm=db.Column(db.Boolean,index=True)
    available = db.relationship('Available', cascade='all,delete', backref='User')
    appointment = db.relationship("Appointment", cascade='all,delete', backref='User')

    # def search_user_id(name):
    #     user=User.query.filter_by(username=name).first()
    #     return user.id
    def set_password(self, password):
        '''
        this function is to hashcode the password

        args:
            password(int):password given by user
        
        '''
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        '''
        this function is to check password is same as saved

        args:
            password(int):password given by user
        return:
            boolean whether password is correct
        '''
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        '''
        this function define the output when print function
        is called on an object of this class

        args:
            none
            
        return:
            the username
        '''
        return 'User {}'.format(self.username)


