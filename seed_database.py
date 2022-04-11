import csv
import models
from flask import Flask 
# import crud
# import server
app = Flask(__name__)
models.connect_to_db(app)  

with open("haunted_places_3.csv", "r" ) as csv_file:
    reader = csv.DictReader(csv_file, delimiter=",")
    for line in reader:
        if line["location"] and line["city"] and line["description"] and line["state"] and line["longitude"] and line["latitude"]:
            location = models.Location(name=line["location"],
                description=line["description"],
                city = line["city"],
                state = line["state"],
                longitude = line["longitude"],
                latitude = line["latitude"]
            )

            models.db.session.add(location)

    models.db.session.commit()


if __name__ == "__main__":
    
    app = Flask(__name__)
    models.connect_to_db(app)  
    #db.create_all()
    #connect_to_db(flask_app)