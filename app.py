# app.py
from flask import Flask, render_template, request, redirect, jsonify
from random import choice
from recommendation import get_movie_data, poster_base_url, get_trending_data, youtube_base_url, get_trailer

app = Flask(__name__)

# Configuration
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "verysecretkey"

# Global variables to store user answers and filtered movies
user_answers = {}
filtered_movies = []

# This function is executed before each request
@app.before_request
def before_request():
    if 'localhost' in request.host_url or '0.0.0.0' in request.host_url:
        app.jinja_env.cache = {}

# Route to the home page
@app.route("/")
def index():
    global user_answers, filtered_movies
    user_answers = {}  # Clear user answers
    filtered_movies = []  # Clear recommended movies
    return render_template("index.html")

# Route to the questions page
@app.route("/questions")
def next_question():
    return render_template("questions.html")

# Route to process user answers
@app.route("/process_answers", methods=["POST"])
def process_answers():
    question_number = int(request.form["question_number"])
    answers = request.form.getlist("answer")

    # Store the answer in the data structure
    if question_number == 3:
        user_answers[question_number] = []
        for answer in answers:
            if answer == "doesn't-matter":
                user_answers[question_number].append(answer)
            else:
                user_answers[question_number].append(int(answer))
    else:
        user_answers[question_number] = answers

    # Determine the next question
    next_question = question_number + 1

    # Check if there is a next question
    if next_question <= 4:
        return jsonify({"status": "success", "next_question": next_question})
    else:
        return jsonify({"status": "completed"})

# Route to get movie recommendations
@app.route("/recommendation")
def recommendation():
    global filtered_movies
    if len(user_answers) == 4:
        if user_answers[3][0] == "doesn't-matter":
            release_year = 13
        else:
            release_year = int(user_answers[3][0])

        genres = user_answers[2]
    
        movie_list = get_movie_data(genres, release_year)

        if movie_list:
            filtered_movies = movie_list

            if filtered_movies:
                movie = choice(filtered_movies)

                # remove the recommended movie from the filtered list
                for i in range(len(filtered_movies)):
                    if filtered_movies[i]["title"] == movie["title"]:
                        del filtered_movies[i]
                        break
                
                # get movie trailer
                trailer_url = get_trailer(movie['id'])
                if trailer_url == 'None':
                    return render_template("recommendation.html", title=movie["title"], poster=f"{poster_base_url}{movie['poster_path']}", overview=movie["overview"], trailer=trailer_url)
                
                trailer_full_url = f"{youtube_base_url}{trailer_url}"
                    
                return render_template("recommendation.html", title=movie["title"], poster=f"{poster_base_url}{movie['poster_path']}", overview=movie["overview"], trailer=trailer_full_url)

    return redirect("/error")

# Route to regenerate a recommended movie
@app.route("/regenerate_movie")
def regenerate_movie():
    global filtered_movies
    if len(filtered_movies) != 0:
        movie = choice(filtered_movies)

        # remove the recommended movie from the filtered list
        for i in range(len(filtered_movies)):
            if filtered_movies[i]["title"] == movie["title"]:
                del filtered_movies[i]
                break

        # get movie trailer
        trailer_url = get_trailer(movie['id'])
        if trailer_url == 'None':
            return jsonify({"status": "success", "title": movie["title"], "poster": f"{poster_base_url}{movie['poster_path']}", "overview": movie["overview"], "trailer": trailer_url})
        
        trailer_full_url = f"{youtube_base_url}{trailer_url}"

        return jsonify({"status": "success", "title": movie["title"], "poster": f"{poster_base_url}{movie['poster_path']}", "overview": movie["overview"], "trailer": trailer_full_url})

    return jsonify({"status": "no_movies"})

# Route to get trending movies
@app.route("/movies")
def movies():
    movies = get_trending_data("movie")
    return render_template("movies.html", movies=movies, poster_base_url=poster_base_url)

# Route to get trending series
@app.route("/series")
def series():
    series = get_trending_data("tv")
    return render_template("series.html", series=series, poster_base_url=poster_base_url)

# Route for error page
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run()