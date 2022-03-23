from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, request, flash, session, redirect)
from models import (Users,Contacts,Favorites,Location,Comments,db,connect_to_db)
# import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "ghostsecrets"
app.jinja_env.undefined = StrictUndefined


@app.route("/registration", methods=["POST", "GET"])
def registration():
    """Register a user"""
    user = None
    if request.method == "POST": 
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        city = request.form["city"]
        state = request.form["state"]
        zipcode = request.form["zipcode"]
        email = request.form["email"]
        user = Users(first_name=first_name, last_name=last_name, password=password,
        city=city, state=state, zipcode=zipcode, email=email) 

        db.session.add(user)
        db.session.commit()
        
        website = request.form["website"]
        social_media_link = request.form["social_media_link"]
        contacts = Contacts(website=website, social_media_link= social_media_link)
        user.contacts = contacts
        
        db.session.add(contacts)
        db.session.commit()
        
        # session["user_id"] =  user.id #Store user in session 
        # db.session.flush() 
        
        return redirect("/")
            
    else:
        user = Users()
        contacts = Contacts()
        user.contacts = contacts    
    return render_template("user_registration.html", user=user)

@app.route("/user_profile") 
def profile():
    """User profile page""" 
    user = Users.query.get(session["user_id"])
    return render_template("user_profile.html", user=user)

   #get info from url?
    #create favorite 
    #db commit and save
    

    

@app.route("/", methods=["POST", "GET"])  
def homepage_login():
    """Show homepage and log in user."""
    email = request.form.get("email")
    password = request.form.get("password")
    
    if request.method == "POST": 
        try: 
            user = Users.query.filter(Users.email == email).one()
        except: 
            flash("The email entered is not registered, please register to continue")
            return redirect("/")
        if user.password != password or user.email != email: 
            flash("The email or password you entered was incorrect.")
        else:
            session["user_email"] = user.email
            return redirect("/user_profile")

    return render_template("homepage.html")
    
#show homepage. if registered, log in will take you to profile page, if not, click here to register
   

   




#        
    
#     else:
#        return render_template('homepage.html')
# @app.route('/search')
# def search():
    #get locations
    #lookup post or get params that's value of input
    #search locations object with value probably with *wildcards
    #return JSON
    

@app.route('/locations')
def show_locations():
    """Show list of locations."""
    locations = Location.query.order_by("name")[0:100]
    
    return render_template('locations.html',locations= locations)

@app.route('/location/<id>') 
def get_location_by_id(id):
    """Return a location by primary key."""

    location = Location.query.get(id)

    return render_template("location_id.html", location=location)
    


if __name__ == "__main__":
    app.debug = True



    # Use the DebugToolbar
    #DebugToolbarExtension(app)
    connect_to_db(app)  
    app.run(host="0.0.0.0")
