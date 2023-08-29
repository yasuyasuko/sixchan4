from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# テーブルを定義
class UserInfo(db.Model):
  UserID = db.Column(db.Integer, primary_key=True)
  User_Name = db.Column(db.String, nullable=False)
  Email = db.Column(db.String, nullable=False)
  Password = db.Column(db.String, nullable=False)


class CommentInfo(db.Model):
  CommentID = db.Column(db.Integer, primary_key=True)
  Comment_Content = db.Column(db.String, nullable=False)
  Comment_Create_Date = db.Column(db.String, nullable=False)

class ThreadInfo(db.Model):
  ThreadID = db.Column(db.Integer, primary_key=True)
  Thread_Name = db.Column(db.String, nullable=False)
  Thread_Content = db.Column(db.String, nullable=False)
  Thread_Create_Date = db.Column(db.String, nullable=False)
