#import
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# create the app
app = Flask(__name__)

# create the extension
db = SQLAlchemy()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)


# テーブルを定義####################################################

class UserInfo(db.Model):
    __tablename__ = 'user_info'
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


#Routing##########################################################

@app.route('/')
def homepage():
    return render_template('homepage.html', \
        homepage = True, \
        title = 'homepage.html')

@app.route('/threadpage/')
def threadpage():
    return render_template('threadpage.html', \
        threadpage = True, \
        title = 'threadpage.html')

@app.route('/threadcreate/')
def threadcreate():
    return render_template('thread_create.html', \
        thread_create = True, \
        title = 'thread_create.html')

# ユーザー情報をDBに登録
@app.route('/userlogin/', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        user_info = UserInfo(
            User_Name = "a",#request.form['User_Name'],
            Email = "b", #request.form['Email'],
            Password = "c", #request.form['Password']
        )
        db.session.add(user_info)
        db.session.commit()
        return redirect('/')#redirect(url_for('user_detail', id=user_info.id))
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
