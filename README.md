# Penn Labs Server Challenge - Yuchen (Tessa) Fan

## Introduction
Welcome to my project! I've followed most of the specifications in the challenge to 
implement a  with bonus frontend (CSS Bootstrap) and database management
(SQLAlchemy w/ SQLite). Also, I'd already written everything using render & templates 
before I realized the specifications for the bonus oops. 

## Pages & Data
Home Page('/' or '/home' or '/api'): displays welcome!

REST API: 
Clubs_API('/api/clubs'): 'GET' -> basic implementation that displays current clubs in JSON format
		
		'POST' -> creates new club w/ info specified in request body
Favorite_API('/api/favorite'): 'POST' -> allows user to favorite a club! added column in 
		Club model to keep users that favorited it, no repeats
User_API: 'GET' -> shows basic user info (username & email)

Additional pages:  
Clubs('/clubs'): shows list of clubs, used FlaskForm to the create_club form, formatted using
		render_template & html
Club Info('/clubs/<clubname>'): shows specific club & form to update club's info (navigate by clicking)
All Users('/user'): shows list of users (can navigate to specific user's page by clicking)

## Documentation: 
Created User & Club models w/ SQLAlchemy to store info for users & clubs.
User_attr: username, email, password
Club_attr: name, description, tags

Scraping: Used Beautiful Soup, loaded info into list of CObj objects, and passed to index.py

Additional feature: 
Login/Logout/Register: 
- Uses Bcrypt to hash user's passwords
- Register user: uses form to get info, creates User object & stores in db
- Uses LoginManager 
- Will not be able to favorite, post, or update club unless loggedin

## Additional Packages
flask = "*"

beautifulsoup4 = "*"

flask-wtf = "*"

flask-sqlalchemy = "*"

requests = "*"

Flask = "*"

flask-bcrypt = "*"

flask-login = "*"

Install using 'pipenv install <name_of_package>'

## Running the Project
Call 'pipenv run python3 index.py' from the command line.
Navigate to 'localhost:5000' to view the page & go to different pages.



