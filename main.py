from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


MOVIE_API_KEY = 'ecd118040b987ede4e895eb1338fb069'
MOVIE_ENDPOINT = f"https://api.themoviedb.org/3/search/movie"

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
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

# db.create_all()


class EditForm(FlaskForm):
    edit_rating = StringField('Your rating out of 10', validators=[DataRequired()])
    edit_review = StringField('Your review', validators=[DataRequired()])
    submit = SubmitField(label="Update")


class Addmovie(FlaskForm):
    movie_name = StringField('Movie name', validators=[DataRequired()])
    submit = SubmitField(label="Add")

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
        response = requests.get(MOVIE_ENDPOINT, params={"api_key": MOVIE_API_KEY, "query": new_movie})
        # data = response.json()['results'][0]['original_title']
        data = response.json()['results']
        return render_template('select.html', data=data)
    else:
        return render_template('add.html', form=movieform)


@app.route('/get_details/<id>')
def get_details(id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{id}", params={"api_key": MOVIE_API_KEY}).json()
    title = response['original_title']
    year = response['release_date'].split('-')[0]
    desc = response['overview']
    rating = response['vote_average']
    img = response['poster_path']
    img_url = f'https://image.tmdb.org/t/p/original{img}'
    new_movie = Movie(
        title=title,
        year=year,
        description=desc,
        rating=rating,
        img_url=img_url
    )
    db.session.add(new_movie)
    db.session.commit()
    movie = Movie.query.filter_by(title=title).first()
    id = movie.id
    movie.ranking = id
    db.session.commit()
    return redirect(url_for('edit', id=id))


if __name__ == '__main__':
    app.run(debug=True)
