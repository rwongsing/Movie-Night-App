from flask import Flask, render_template, redirect, url_for, request
from imdb import IMDb
import json

app = Flask(__name__)

def addMovie(movieTitle):
    ia = IMDb()
    movieList = ia.search_movie(movieTitle)

    if len(movieList) == 0:
        # add error msg
        return
    
    movieId = movieList[0].movieID
    movie = ia.get_movie(movieId)

    with open(r'C:\Users\rwong\Desktop\Coding\movie picker\movie.json', "r") as file:
        movies = json.load(file)
        
        newMovie = {}
        newMovie["id"] = movieId
        newMovie["name"] = movie['title']
        newMovie["rating"] = movie.get('rating')
        newMovie["duration"] = movie.get('runtimes')
        newMovie["genre"] = movie.get('genre')

        movies.append(newMovie)
    with open(r'C:\Users\rwong\Desktop\Coding\movie picker\movie.json', "w") as file:
        json.dump(movies, file, indent=4)
    # return success msg

def deleteMovie(delMovies):
    with open(r'C:\Users\rwong\Desktop\Coding\movie picker\movie.json') as file:
        movies = json.load(file)

    for movieName in delMovies:
        counter = 0
        for movie in movies:
            if movie['name'] == movieName:
                movies.pop(counter)
            counter += 1
            
    with open(r'C:\Users\rwong\Desktop\Coding\movie picker\movie.json', 'w') as file:
        json.dump(movies, file, indent=4)
    # return success msg

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'addMovie' in request.form:
            movieTitle = request.form.get("movieTitle")
            addMovie(movieTitle)
            #add return msg
            return redirect(request.url)
        elif 'deleteMovie' in request.form:
            delMovies = request.form.getlist("checkedMovies")
            deleteMovie(delMovies)
            # add return msg
            return redirect(request.url)

    with open(r'C:\Users\rwong\Desktop\Coding\movie picker\movie.json', "r") as file:
        movies = json.load(file)
        return render_template('home.html', movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
