#import
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, RadioField, SelectField,SubmitField, ValidationError)
from wtforms.validators import DataRequired,Email
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import os
import hashlib
import datetime

dt_now = datetime.datetime.now()
# create the app
app = Flask(__name__)

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///c:/Users/user/sixchan4/blog/instance/SNS.db"

app.config['SECRET_KEY'] = os.urandom(24)
# initialize the app with the extension
db.init_app(app)


class UserInfo(UserMixin,db.Model):
    __tablename__ = 'user_info'
    UserID = db.Column(db.Integer, primary_key=True)
    User_Name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False)
    Password = db.Column(db.String, nullable=False)

class CommentInfo(db.Model):
    __tablename__ = 'comment_info'
    CommentID = db.Column(db.Integer, primary_key=True)
    Nickname = db.Column(db.String, nullable=True)
    Comment_Content = db.Column(db.String, nullable=False)
    Comment_Create_Date = db.Column(db.String, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)
    ThreadID = db.Column(db.Integer, nullable=False)

class ThreadInfo(db.Model):
    __tablename__ = 'thread_info'
    ThreadID = db.Column(db.Integer, primary_key=True)
    Thread_Name = db.Column(db.String, nullable=False)
    Thread_Content = db.Column(db.String, nullable=False)
    Thread_Create_Date = db.Column(db.String, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)

print("success")
