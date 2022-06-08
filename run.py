from flask import Flask
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>')
def get_by_movie_title(title):
    return get_by_title(title)


if __name__ == "__main__":
    app.run(port=5005, debug=True)
