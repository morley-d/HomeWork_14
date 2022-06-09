from flask import Flask, jsonify
from utils import *

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/movie/<title>')
def get_movie_by_title(title):
    return jsonify(movie_by_title(title))


@app.route('/movie/<int:year1>/to/<int:year2>')
def get_movies_by_years(year1, year2):
    return jsonify(movies_by_years(year1, year2))


@app.route('/rating/<category>')
def get_movies_by_rating(category):
    return jsonify(movies_by_rating(category))


@app.route('/genre/<genre>')
def get_movies_by_genre(genre):
    return jsonify(movies_by_genre(genre))


if __name__ == "__main__":
    app.run(port=5005, debug=True)

print(app.config)
