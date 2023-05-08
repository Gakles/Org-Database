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
    return render_template("home.html")

#login
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        if session.get("logged_in") == True:
            flash("You are already logged in", "logged_in True")
            return redirect(url_for("home"))
        else:
            return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username + " " + password)
        #TODO: do sqlalchemy to authenticate
        if db_session.query(User).where((User.username == username) & (User.password == password)):
            session["logged_in"] = True
            flash("Welcome", "welcome")
            return redirect(url_for("addorg"))
        else:
            flash("Invalid Login", "error")
            return redirect(url_for("home"))

#signup
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "GET":
        if session.get("logged_in") == True:
            flash("You are already logged in", "Logged in")
            return redirect(url_for("home"))
        else:
            return render_template("signup.html")
    if request.method == "POST":
        proposed_username = request.form["proposed_username"]
        proposed_password = request.form["proposed_password"]
        print(proposed_username + " " + proposed_password)
        #Check if account already exists
        johns = db_session.query(User).where((User.username == proposed_username) | (User.password == proposed_password)).first()
        print(johns)
        if johns is not None:
            flash("Sorry, either this username or password already exists. Please try a different one", "Account already exists")
            print("User already exists")
            return redirect(url_for("signup"))
        #Add new user 
        else:
            create_new_account(proposed_username, proposed_password)
            flash("Account created! Login to continue", "Account created")
            return redirect(url_for("login"))


#addorg
@app.route("/addorg", methods = ["POST", "GET"])
def addorg():
    if request.method == "GET":
        if session.get("logged_in") == True:
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
        flash("NO Bad user D:<", "Sin")
        return redirect(url_for("home"))
    elif request.method == "POST":
        #TODO: Add search stuff
        return render_template("results.html")
    
#logout
@app.route("/logout")
def logout():
    if "logged_in" in session:
        session.pop("logged_in")
        flash("You have been logged out", "Logout")
        return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)


    