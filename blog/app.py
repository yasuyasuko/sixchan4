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

#ユーザログイン機能関連###################

#/loginで確認

#インスタンス化
login_manager = LoginManager()
#アプリをログイン機能を紐付ける
login_manager.init_app(app)
#未ログインユーザーを転送する(ここでは'login'ビュー関数を指定)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#   #パスワードチェックする関数を追記
# def check_password(self, password):
#     return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ログイン')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #フォーム入力したアドレスがDB内にあるか検索
        user = UserInfo.query.filter_by(Email=form.email.data).first()
        print(form.email.data)
        print(user)
        if user is not None:
            #check_passwordはUserモデル内の関数
            # if check_password_hash(user.Password, form.password.data):
            hashpass=hashlib.sha256(form.password.data)
            if hashpass == user.Password:#TypeError: Strings must be encoded before hashing
                #ログイン処理。ログイン状態として扱われる。
                login_user(user)
                print("Success login")
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('user_maintenance')
                return redirect(next)
                
            else:
                print(user.Password)
                print(form.password.data)
                print(check_password_hash(user.Password, form.password.data))
                print('パスワードが一致しません')
        else:
            print('入力されたユーザーは存在しません')

    return render_template('login.html', form=form)

# テーブルを定義####################################################

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


#Routing##########################################################

@app.route('/')
def homepage():
    return render_template('homepage.html', \
        homepage = True, \
        title = 'homepage.html')

@app.route('/threadpage/<id>/', methods=['GET', 'POST'])#0=id
def threadpage(id):
    comment_info_all = CommentInfo.query.filter(CommentInfo.ThreadID == id).all()
    if request.method == 'POST':
        comment_info = CommentInfo(
            Nickname = request.form['Nickname'],
            Comment_Content = request.form['Comment_Content'],
            Comment_Create_Date =dt_now,
            UserID  = request.form['UserID'],
            ThreadID = request.form['ThreadID'],
        )
        db.session.add(comment_info)
        db.session.commit()
        return redirect(url_for('threadpage',id=request.form['ThreadID']))
    else:
        return render_template('threadpage.html', comment_info_all = comment_info_all, \
            threadpage = True, \
            title = 'スレッドページ（ID='+ id +')')

@app.route('/threadcreate/', methods=['GET', 'POST'])
def threadcreate():
    if request.method == 'POST':
        thread_info = ThreadInfo(
            Thread_Name = request.form['Thread_Name'],
            Thread_Content = request.form['Thread_Content'],
            Thread_Create_Date =dt_now,
            UserID  = request.form['UserID']
        )
        db.session.add(thread_info)
        db.session.commit()
        return redirect('/')#redirect(url_for('user_detail', id=user_info.id))
    else:
        return render_template('thread_create.html', \
            thread_create = True, \
            title = 'thread_create.html')

# ユーザー情報をDBに登録
@app.route('/userlogin/', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        user_info = UserInfo(
            User_Name = request.form['User_Name'],
            Email = request.form['Email'],
            Password =hashlib.sha256(bytes(request.form['Password'], encoding = "utf-8")).hexdigest()
        )
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_detail', id=user_info.UserID))
    else:
        return render_template('user_login.html', \
            user_login = True, \
            title = 'user_login.html')

# IDからDBのユーザー情報を取得して表示
@app.route("/user_<int:id>")
def user_detail(id):
        user_info = db.get_or_404(UserInfo, id)
        return render_template("user_detail.html", user_info=user_info)

@app.route('/userpage/')
def userpage():
    return render_template('userpage.html', \
        userpage = True, \
        title = 'userpage.html')


#おまじない###############################################################
if __name__ == "__main__":
        app.run(debug=True)
