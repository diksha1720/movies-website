from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)

# db.create_all()


class EditForm(FlaskForm):
    edit_rating = StringField('Your rating out of 10', validators=[DataRequired()])
    edit_review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField(label="Update")


class Addmovie(FlaskForm):
    movie_name = StringField('Movie name', validators=[DataRequired()])
    submit = SubmitField(label="Add")

## After adding the new_movie the code needs to be commented out/deleted.
## So you are not trying to add the same movie twice.
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/")
def home():
    all_movies = Movie.query.all()
    num = len(all_movies)
    # return f"{all_movies}"
    return render_template("index.html", movies=all_movies, num=num)


@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    movie = Movie.query.get(id)
    editform = EditForm()
    if editform.validate_on_submit():
        movie.rating = editform.edit_rating.data
        movie.review = editform.edit_review.data
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', form=editform)


@app.route('/delete/<ide>')
def delete(ide):
    movie = Movie.query.get(ide)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    movieform = Addmovie()
    if movieform.validate_on_submit():
        new_movie = movieform.movie_name.data

    return render_template('add.html', form=movieform)


if __name__ == '__main__':
    app.run(debug=True)
