from flask_debugtoolbar import DebugToolbarExtension
from flask import (Flask, render_template, request, flash, session, jsonify, redirect, make_response)
from models import (Users,Contacts,Favorites,Location,Comments,db,connect_to_db)
import json
from passlib.hash import argon2

# import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "ghostsecrets"
app.jinja_env.undefined = StrictUndefined
@app.route('/logout')
def logout():
    if "user_id" in session:
        del session["user_id"] 
    return redirect("/")

@app.route("/registration", methods=["POST", "GET"])
def registration():
    """Register a user"""
    user = None
    if request.method == "POST": 
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = argon2.hash(request.form["password"])
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
    favorites = request.args.get("favorites")
    print(user.contacts)
    return render_template("user_profile.html", user=user)
    
@app.route("/", methods=["POST", "GET"])  
def homepage_login():
    """Show homepage and log in user."""
    user = None
    if "user_id" in session:
        user = Users.query.filter_by(id = session["user_id"]).one()
    if request.method == "POST": 
        email = request.form.get("email")
        password = request.form.get("password")
        try: 
            user = Users.query.filter(Users.email == email).one()
        except: 
            flash("The email entered is not registered, please register to continue")
            return redirect("/")
        if not (user.password == password or argon2.verify(password, user.password)) or user.email != email: 
            flash("The email or password you entered was incorrect.")
        else:
            session["user_email"] = user.email
            session["user_id"] = user.id
            return redirect("/")
    print(user)
    return render_template("homepage.html", user=user)
    
#show homepage. if registered, log in will take you to profile page, if not, click here to register


@app.route('/locations')
def show_locations():
    """Show list of locations."""
    locations = Location.query.order_by("name")
    
    return render_template('locations.html',locations= locations)

@app.route('/search')
def search():
    """Return Search Results"""
    requestValue = request.args.get("location")
    like_query = f"%{requestValue}%"  
    response = Location.query.filter(Location.name.like(like_query)).all() 
    return jsonify(response)

@app.route('/comment_submit', methods=["POST", "GET"])
def comment_submit():
    """docstring"""
    user = None
    if "user_id" in session:
        user = Users.query.filter_by(id = session["user_id"]).one()
    
    if request.method == "POST": 
        id = request.form.get("id")
        comments = request.form.get("user_comments")
        comments = Comments(user_id= user.id, location_id = id, user_comments=comments)
        db.session.add(comments)
        db.session.commit()
        return redirect(f"/location/{id}")
    
    

@app.route('/location/<id>', methods=["POST", "GET"]) 
def get_location_by_id(id):
    """Return a location by primary key."""
    user = None
    if "user_id" in session:
        user = Users.query.filter_by(id = session["user_id"]).one()
        

    location = Location.query.get(id)
    return render_template("location_id.html", location=location, user= user)

@app.route("/favorites")
def show_favorites():
    """Show user's list of favorites"""
    if request.args.get("favorite"): #if the favorite button has been submitted on location_id.html
        favorite_id = request.args.get("favorite")

        if not Favorites.query.filter_by(user_id=session["user_id"], location_id=favorite_id).all(): #if the favorite is not in favorite table 
            favorite = Favorites(location_id= favorite_id, user_id= session["user_id"]) #add to favorites
            db.session.add(favorite)
            db.session.commit()
    
    return render_template("favorites.html", favorites= Favorites.query.filter_by(user_id=session["user_id"]).all())

if __name__ == "__main__":
    app.debug = True



    # Use the DebugToolbar
    #DebugToolbarExtension(app)
    connect_to_db(app)  
    app.run(host="0.0.0.0")
