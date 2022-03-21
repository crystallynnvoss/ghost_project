from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, request, flash, session, redirect)
from models import (Users,Contacts,Favorites,Location,Comments,db,connect_to_db)
# import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'ghostsecrets'
app.jinja_env.undefined = StrictUndefined


@app.route('/registration', methods=["POST", "GET"])
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
        user = Users(first_name=first_name, last_name=last_name, password=password,
        city=city, state=state, zipcode=zipcode) 

        db.session.add(user)
        db.session.commit()
        
        email = request.form["email"]
        website = request.form["website"]
        social_media_link = request.form["social_media_link"]
        contacts = Contacts(email=email, website=website, social_media_link= social_media_link)
        user.contacts = contacts
        
        db.session.add(contacts)
        db.session.commit()
        db.session.flush()
        print(user.id)
        session["user_id"] =  user.id
        return redirect('/dashboard')
            
    else:
        user = Users()
        contacts = Contacts()
        user.contacts = contacts    
    return render_template('user_registration.html', user=user)

@app.route('/dashboard') #, methods=["POST", "GET"])
def dashboard():
    print(session)
    user = Users.query.get(session["user_id"])

    return f"Your daskboard goes here! Logged in User is {session['user_id']} <br> Name is {user.first_name}"


@app.route('/') #, methods=["POST", "GET"])
def homepage():
    """Show homepage."""
    
    return render_template('homepage.html')
#     if request.method == "POST": 
#         fname = request.form["first_name"] 
#         lname = request.form["last_name"] 
#         password = request.form["password"]
        
#         if Users.query.filter_by(first_name= fname) == 
#          last_name= lname, password= password) == :
#             return redirect ("/user_profile.html")
    
#     else:
#        return render_template('homepage.html')
@app.route('/search')
def search():
    #get locations
    #lookup post or get params that's value of input
    #search locations object with value probably with *wildcards
    #return JSON
    pass

@app.route('/locations')
def show_locations():
    """Show list of locations."""
    locations = Location.query.all()[0:10]
    
    return render_template('locations.html',locations= locations)

@app.route('/location/<id>') 
def get_location_by_id(id):
    """Return a location by primary key."""

    location = Location.query.get(id)

    return render_template("location_id.html", location=location)
    

# @app.route('/user/:profile')
# def something_else():
#     """Show single user profile."""
 
    
#     return render_template("")

if __name__ == "__main__":
    app.debug = True



    # Use the DebugToolbar
    #DebugToolbarExtension(app)
    connect_to_db(app)  
    app.run(host="0.0.0.0")
