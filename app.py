from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "The geopolitical consequences OPEC's latest announcement are far reaching. The mining of the Strait of Hormuz will strangle the flow of international tankers, while Russia's exclusion from price-matching meeting may lead to it's collapse."

# TODO: Fill in methods and routes



#home
@app.route("/")
def home():
    flash("john", "cena")
    return render_template("home.html")

#login
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        #TODO: do dbsession to authenticate
        #fail
        flash("Invalid Login", "error")
        return redirect(url_for("home"))
        #success
        session["logged_in"] = TRUE
        flash("Welcome " + session("username"), "welcome")
        return redirect(url_for("addorg"))

#signup
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

#addorg
@app.route("/addorg", methods = ["POST", "GET"])
def addorg():
    #remember to get rid of this once login stuff starts working
    if request.method == "GET":
        session["logged_in"] = True
        if session.get("logged_in"):
            return render_template("orgbuilder.html")
        else:
            flash("Please login", "Error")
            return redirect(url_for("login"))
    elif request.method == "POST":
        orgname = request.form["organization-name"]
        orgdesc = request.form["organization-description"]
        print(orgname + " " + orgdesc)
        return render_template("orgbuilder.html")

#results
@app.route("/results", methods = ["GET", "POST"])
def results():
    if request.method == "GET":
        #flash("NO", "Bad user D:<")
        #return redirect(url_for("home"))
        return render_template("results.html")
    elif request.method == "POST":
        #TODO: Add search stuff
        return render_template("results.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
