import os
# returns a string of the current directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = 'you-will-never-guess'
    # app.db in current directory
    # this variable defines the file location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = "587"
    MAIL_USE_TLS = True
    MAIL_USERNAME = "1537309753@qq.com"
    MAIL_PASSWORD = "xtafgnpwokcwbadh" 
    MAIL_DEFAULT_SENDER = "1537309753@qq.com"