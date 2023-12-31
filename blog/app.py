#import
from flask import Flask ,render_template ,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
# from werkzeug.security import check_password_hash, generate_password_hash
import hashlib
import datetime
from wtforms import (StringField, PasswordField, BooleanField, 
                     RadioField, SelectField,SubmitField, ValidationError)
from wtforms.validators import DataRequired,Email
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
import os

dt_now = datetime.datetime.now()

# create the app
app = Flask(__name__)

#インスタンス化
login_manager = LoginManager()
#アプリをログイン機能を紐付ける
login_manager.init_app(app)
#未ログインユーザーを転送する(ここでは'login'ビュー関数を指定)
login_manager.login_view = 'login'
# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///c:/Users/user/sixchan4/blog/instance/SNSdb.db"

app.config['SECRET_KEY'] = os.urandom(24)
# initialize the app with the extension
db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(user_id)

#   #パスワードチェックする関数を追記
# def check_password(self, password):
#     return check_password_hash(self.password_hash, password)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ログイン')

# テーブルを定義####################################################

class UserInfo(UserMixin,db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
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
            hashpass =hashlib.sha256(bytes(form.password.data, encoding = "utf-8")).hexdigest()
            if hashpass == user.Password:
                #ログイン処理。ログイン状態として扱われる。
                login_user(user)#DB内のUserIDをidにしないといけない？
                # print("Success login")
                next = request.args.get('next')
                if next == None or not next[0] == '/':
                    next = url_for('userpage')
                return redirect(next)
                
            else:
                # print(user.Password)
                # print(form.password.data)
                # print(check_password_hash(user.Password, form.password.data))
                print('パスワードが一致しません')
        else:
            print('入力されたユーザーは存在しません')

    return render_template('login.html', form=form)


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
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_info = UserInfo(
            User_Name = request.form['User_Name'],
            Email = request.form['Email'],
            Password =hashlib.sha256(bytes(request.form['Password'], encoding = "utf-8")).hexdigest()
        )
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('user_detail', id=user_info.id))
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
@login_required
def userpage():
    id = UserInfo.get_id(current_user)
    user_info = db.get_or_404(UserInfo, id)
    print("ID is "+id)
    return render_template('userpage.html', user_info = user_info ,\
        userpage = True, \
        title = 'userpage.html')

# logoutページのルーティング
@app.route('/logout')
def logout():
  # logout_user関数を呼び出し
  logout_user()
  # トップページにリダイレクト
  return redirect(url_for('homepage'))

#おまじない###############################################################
if __name__ == "__main__":
        app.run(debug=True)
