import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
from flask import request, render_template, url_for, flash, redirect, jsonify
from scraper import CObj, get_club_objects
from forms import RegistrationForm, LoginForm, PostClub, FavoriteForm, UpdateForm

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "site.db"))

app.config['SECRET_KEY'] = '29a9627a4d03ea487535cb82d87e3387'
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), default="noemail@email.com")
    password = db.Column(db.String(60), default="password")

    def __repr__(self):
        return "<Username: {}>".format(self.username)

class Club(db.Model):
    __tablename__ = 'clubs'
    club_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text)
    num = db.Column(db.Integer, default=0)
    users = db.Column(db.Text, default="")
    def __repr__(self):
        return "name: " + self.name + ", description: " + self.description + ", tags: " + self.tags

db.create_all()
db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#class Tag(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(50), nullable=False)
 
clubs = get_club_objects()
for c in clubs: 
    str1 = ' | '.join(c.tags)
    print(str1)
    if Club.query.filter_by(name=c.name).first() is None:
        club_model = Club(name=c.name, description=c.description, tags=str1)
        db.session.add(club_model)
        db.session.commit()


if User.query.filter_by(username='jen').first() is None: 
    jen = User(username='jen', email='jen@seas.upenn.edu', password='password')
    db.session.add(jen)
    db.session.commit()

@app.route('/')
@app.route('/home')
@app.route('/api')
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            flash('You have been logged in!', 'success')
            return redirect(url_for('user', username=user.username))
        else: 
            flash('Incorrect email or password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/clubs", methods = ['GET', 'POST'])
def clubs():
    form = PostClub()
    if form.validate_on_submit():
        if current_user.is_authenticated: 
            club = Club(name=form.name.data, description=form.description.data, tags=form.tags.data)
            db.session.add(club)
            db.session.commit()
            flash('Club created! (scroll to bottom)', 'success')
            return redirect(url_for('clubs'))
        else: 
            flash('Login to post a club.', 'danger')
    clubs = Club.query.all()
    return render_template('clubs.html', title="Clubs", form=form, clubs=clubs)

@app.route("/clubs/<clubname>", methods = ['GET', 'POST'])
def club_info(clubname):
    club = Club.query.filter_by(name=clubname).first()

    form = UpdateForm()
    if form.validate_on_submit():
        if current_user.is_authenticated: 
            club.description = form.description.data
            club.tags = form.tags.data
            db.session.commit()
            flash('Club Updated!', 'success')
            return redirect(url_for('clubs'))
        else: 
            flash('Login to update a club.', 'danger')
    return render_template('club.html', title="Club Info", form=form, club=club)

@app.route('/api/clubs', methods = ['GET', 'POST'])
def clubs_api():
    name = request.args.get('name')
    description = request.args.get('description')
    tags = request.args.get('tags')
    if name and description and tags: 
        club = Club(name=name, description=description, tags=tags)
        db.session.add(club)
        db.session.commit()
        flash('Club created! (scroll to bottom', 'success')
        return redirect(url_for('clubs_api'))
    clubprint = []
    clubs = Club.query.all()
    for i in clubs:
        clubprint.append(i.__repr__())
    return jsonify(clubprint)

@app.route("/api/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template("user.html", title="User", user=user)

@app.route("/user")
def all_users():
    users = User.query.all()
    return render_template("all_users.html", title="All_Users", users=users)

@app.route("/favorite", methods=['GET', 'POST'])
def favorite():
    form = FavoriteForm()
    if form.validate_on_submit():
        if current_user.is_authenticated: 
            clubname = form.clubname.data
            club = Club.query.filter_by(name=clubname).first()
            usersLikes = club.users
            if current_user.username in usersLikes:
                flash('Already favorited club', 'danger')
            else: #didn't like club yet
                club.users = club.users + " " + current_user.username
                club.num = club.num+1
                db.session.commit()
                flash('Successfully favorited club!', 'success')
            return redirect(url_for('favorite'))
        else: 
            flash('Login to favorite a club', 'danger')
    return render_template('favorite.html', form=form)

@app.route("/api/favorite", methods=['GET', 'POST'])
def favorite_api():
    username = request.args.get('user')
    clubname = request.args.get('club')

    if username and clubname: 
        user = User.query.filter_by(username=username).first()
        club = Club.query.filter_by(name=clubname).first()
        usersLikes = club.users
        if username in usersLikes:
            flash('Already favorited club', 'danger')
        else:
            club.users = club.users + " " + username
            club.num = club.num+1
            db.session.commit()
            flash('Successfully favorited club!', 'success')
        return redirect(url_for('clubs'))
    return """
    <h1>Favorites API</h1>
    """


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

