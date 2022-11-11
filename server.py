"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db

import crud

#make throw errors for undefined variables
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "shhh"
app.jinja_env.undefined = StrictUndefined



# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """view homepage"""
    
    return render_template("homepage.html")

@app.route('/users')
def get_users():
    """view all users"""
    
    users = crud.get_users()
    
    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """show user profile"""
    
    user = crud.get_user_by_id(user_id)
    
    return render_template("user_details.html", user=user)

@app.route('/movies')
def get_movies():
    """view all movies"""
    
    movies = crud.get_movies()
    
    return render_template("all_movies.html", movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    """show overview of a movie"""
    
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template("movie_details.html", movie=movie)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
