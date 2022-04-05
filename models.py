from datetime import datetime
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="", echo=True):
    """Connect to database"""
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ghost:casper@localhost/ghost_project"
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

#create classes that represet tables in the database
#class will have attributes that represent the table 
#establish relationships between tables
@dataclass #use to make it possible to return as json 
class Location(db.Model): 
    """Create db table for haunted location information"""
    name:str
    description:str
    state:str
    id:int
    city_longitude:float
    city_latitude:float
    
    __tablename__ = "location"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.Text(), nullable = False)
    description = db.Column(db.Text())
    city = db.Column(db.String(254), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    city_longitude = db.Column(db.Float())
    city_latitude = db.Column(db.Float())    
    favorites = db.relationship("Favorites", back_populates="location")
    comments = db.relationship("Comments", back_populates="location")
    
    def __repr__(self):
        return f'<Location name={self.name}>'

class Users(db.Model): 
    """Create db table"""
   
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(25), nullable = False)
    zipcode = db.Column(db.Integer, nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    
    contacts = db.relationship("Contacts", uselist=False, back_populates= "users")
    comments = db.relationship("Comments", back_populates="users")
    favorites = db.relationship("Favorites", back_populates="users")

    def __repr__(self):
        return f'<Users user={self.first_name, self.last_name}>'
    
class Contacts(db.Model):   
    """Create db table"""
   
    __tablename__ = "contacts"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    website = db.Column(db.String(100))
    social_media_link = db.Column(db.String(100))
    
    users = db.relationship("Users", uselist=False, back_populates= "contacts")

    def __repr__(self):
        return f'<Contacts contact_info={self.user_id, self.website, self.social_media_link}>'

class Favorites(db.Model): 
    """Create db table"""
    
    __tablename__ = "favorites"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    
    users = db.relationship("Users", back_populates="favorites")#may not be used
    location = db.relationship("Location", back_populates="favorites")#may not be used

    def __repr__(self):
        return f'<Favorites favorites={self.user_id, self.location_id}>'

class Comments(db.Model): 
    """Create db table"""
    
    __tablename__ = "comments"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    user_comments = db.Column(db.Text())
    date_created = db.Column(db.DateTime, default=datetime.now)

    users = db.relationship("Users", back_populates="comments")
    location = db.relationship("Location", back_populates="comments")

    def __repr__(self):
        return f'<Comments comment_info={self.user_id, self.location_id}>'

if __name__ == "__main__":
    
    app = Flask(__name__)
    connect_to_db(app)  
    db.create_all()
    
    