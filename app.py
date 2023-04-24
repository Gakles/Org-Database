from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "Change Me"

# TODO: Fill in methods and routes

@app.before_first_request
def setup():
    init_db()

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #TODO: do dbsession to authenticate
        return redirect(url_for("home"))

@app.route("/addorg")
def addorg():
    admin = 
    return render_template("vets.html", admin = admin)
if __name__ == "__main__":
    app.run(debug=True)
