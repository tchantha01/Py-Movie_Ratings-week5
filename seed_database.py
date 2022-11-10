"""Script to seed database"""

#import statements
import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

#script to re-create database
os.system("dropdb ratings")
os.system("createdb ratings")

#connect to the database and call db.create_all()
model.connect_to_db(server.app)
model.db.create_all()

#load data from json file and set to a variable
with open("data/movies.json") as f:
    movie_data = json.loads(f.read())
    
#create movies, store them in list so we can use them to create fake ratings later
movies_in_db = []
for movie in movie_data: 
    title, overview, poster_path = (
        movie["title"],
        movie["overview"],
        movie["poster_path"],
    )
    
    release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")
    
    db_movie = crud.create_movie(title, overview, release_date, poster_path)
    
model.db.session.add_all(movies_in_db)
model.db.session.commit()    