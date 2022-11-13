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

@app.route('/login', methods=["POST"])
def login():
    """Login in user"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    # Check to see if user exist with this email    
    user = crud.get_user_by_email(email)
    
    if not user or user.password != password:
        flash("The email or password you entered is incorrect")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")    
    
    return redirect('/')    
        
    
        
    

@app.route('/logout')
def logout():
    
    del session["email"]
    flash("Logged out")
    return redirect('/')
    
    

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user"""
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    
    if user:
        flash("Cannot create an account with that email. Please try again.")
    else:
        user = crud.create_user(email, password)   
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.") 
        
        return redirect('/')

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

@app.route('/movies/<movie_id>/ratings', methods=["POST"])
def create_rating(movie_id):
    """Create a new movie rating"""
    
    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")
    
    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you did not select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)
        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()
        
        flash(f"You rated this movie {rating_score} out of 5.")  
        
    return redirect(f"/movies/{movie_id}")       

@app.route("/update_rating", methods=["POST"])
def update_rating():
    """Update a rating"""
    
    rating_id = request.json["rating_id"]
    update_score = request.json["update_score"]
    crud.update_rating(rating_id, update_score)
    db.session.commit()
    
    return "Success!"      



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
