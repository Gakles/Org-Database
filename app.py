from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

# TODO: Change the secret key
app.secret_key = "The geopolitical consequences OPEC's latest announcement are far reaching. The mining of the Strait of Hormuz will strangle the flow of international tankers, while Russia's exclusion from price-matching meeting may lead to it's collapse."


#Functions

def keychecker(dic, key):
    if key in dic.keys():
        return True
    else: 
        return False

def addorghelper(request):
    tags = []
    if keychecker(request.form, "mental-health"):
        tags.append("mental-health")
    if keychecker(request.form, "housing"):
        tags.append("housing")
    if keychecker(request.form, "environment"):
        tags.append("environment")
    if keychecker(request.form, "addiction-recovery"):
        tags.append("addiction-recovery")
    if keychecker(request.form, "elder-care"):
        tags.append("elder-care")
    if keychecker(request.form, "food-security"):
        tags.append("food-security")
    if keychecker(request.form, "literacy"):
        tags.append("literacy")
    print(tags)
    orgname = request.form["organization-name"]
    orgdesc = request.form["organization-description"]
    time_commitment = request.form["time"]
    impact = request.form["impact"]
    rtndict = {
        #IMPORTANT tags is a list of strings
        "tags" : tags,
        "orgname" : orgname,
        "orgdesc" : orgdesc,
        "time_commitment" : time_commitment,
        "impact" : impact
    }
    return rtndict

def create_new_account(proposed_username, proposed_password):
    new_user = User(proposed_username, proposed_password)
    print(new_user)
    db_session.add(new_user)
    db_session.commit()

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
        print(username + " " + password)
        #TODO: do sqlalchemy to authenticate
        #fail
        flash("Invalid Login", "error")
        return redirect(url_for("home"))
        #success
        session["logged_in"] = True
        flash("Welcome " + session("username"), "welcome")
        return redirect(url_for("addorg"))

#signup
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        session["logged_in"] = False
        if session.get("logged_in") == True:
            flash("You are already logged in", "Logged in")
            return redirect(url_for("home"))
        elif session.get("logged_in") == False:
            return render_template("signup.html")
    if request.method == "POST":
        proposed_username = request.form["proposed_username"]
        proposed_password = request.form["proposed_password"]
        print(proposed_username + " " + proposed_password)
        #TODO: do sqlalchemy to check if the username and password combo exists
        if db_session.query(User).where((User.username == proposed_username) | (User.password == proposed_password)) is not None:
        #fail
            flash("Sorry, either this username or password already exists. Please try a different one", "Account already exists")
            print("User already exists")
            return redirect(url_for("signup"))
        #success
        #dbsession add new user
        create_new_account(proposed_username, proposed_password)
        flash("Account created! Login to continue", "Account created")
        return redirect(url_for("login"))


#addorg
@app.route("/addorg", methods = ["POST", "GET"])
def addorg():
    if request.method == "GET":
        #remember to get rid of this once login stuff starts working
        session["logged_in"] = True
        if session.get("logged_in"):
            return render_template("orgbuilder.html")
        else:
            flash("Please login", "Error")
            return redirect(url_for("login"))
    elif request.method == "POST":
        orgdict = addorghelper(request)
        #add the org to the database
        print(orgdict["orgname"])
        flash("Organization " + orgdict.get("orgname") + " created!", "Organization created")
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


    