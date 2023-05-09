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
    orgname = ""
    if keychecker(request.form, "organization-name"):
        orgname = request.form["organization-name"]
    orgdesc = ""
    if keychecker(request.form, "organization-description"):
        orgdesc = request.form["organization-description"]
    time_commitment = ""
    if keychecker(request.form, "time"):
        time_commitment = request.form["time"]
    impact = ""
    if keychecker(request.form, "impact"):
        impact = request.form["impact"]
    rtndict = {
        #IMPORTANT tags is a list of strings
        "tags" : tags,
        "orgname" : orgname,
        "orgdesc" : orgdesc,
        "time-commitment" : time_commitment,
        "impact" : impact
    }
    return rtndict

def org_tag_applier_helper(taglist, org, tag_string):
    if org_tag_checker(taglist, tag_string):
        #get the correct tag
        tag = db_session.query(Tags).where(Tags.name == tag_string).first()
        print(tag)
        #append it to the organization list -> it should back populate to tags?
        #org.tags.append(tag)
        #create Org_Tags object, the constructor takes the objects and gets their ids
        new_Org_Tags = Org_Tags(org, tag)
        #add it
        db_session.add(new_Org_Tags)
        #commit it
        db_session.commit()

def org_tag_applier(taglist, org):
    tagstrings = ["mental-health", "housing", "environment", "addiction-recovery", "elder-care", "food-security", "literacy"]
    for string in tagstrings:
        org_tag_applier_helper(taglist, org, string)
#helper method for org_tag_applier
def org_tag_checker(tags, checkstr):
    if checkstr in tags:
        return True
    else:
        return False

def create_new_account(proposed_username, proposed_password):
    new_user = User(proposed_username, proposed_password)
    db_session.add(new_user)
    db_session.commit()

def orgsearcher(orgdict):
    results = db_session.query(Organization).all()
    for org in results:
        print(org)
        for tag in org.tags:
            print(tag)
    if len(orgdict["tags"]) >= 0:
        for org in results:
            for tag in org.tags:
                print(tag)

# TODO: Fill in methods and routes



#home
@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        #TODO: Add search stuff
        
        return render_template("results.html")

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
        #Create the organization object
        #print(orgdict.get("orgname"), orgdict.get("orgdesc"))
        potential_org = Organization(orgdict["orgname"], orgdict["orgdesc"], orgdict["time-commitment"], orgdict["impact"])
        #Check if it already exists
        if db_session.query(Organization).where(Organization.name == potential_org.name).first() is not None:
            flash("Organization already exists", "Org already exists")
        else: 
            #Add the org
            db_session.add(potential_org)
            db_session.commit()
            #Add the tags
            neworg = db_session.query(Organization).where(Organization.name == potential_org.name).first()
            org_tag_applier(orgdict["tags"], neworg)
            flash("Organization: " + str(neworg) + " successfully created/nIt has tags: " + str(neworg.tags))


        return render_template("orgbuilder.html")
        
#results
@app.route("/results", methods = ["GET", "POST"])
def results():
    if request.method == "GET":
        #Search through all the requirements
        orgdict = addorghelper(request)
        results = orgsearcher(orgdict)
        return render_template("home.html")
    
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
    #printstatement = db_session.query(Organization).where(Organization.name == "")


    