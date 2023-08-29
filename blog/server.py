#import
from flask import Flask,render_template

#Creating Flask Objects
app = Flask(__name__)


#Routing 
@app.route("/")
def hello():
    return "Hello World"


@app.route("/index")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
