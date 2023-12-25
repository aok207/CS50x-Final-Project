# Recommendation.py
"""Recommendation.py contains functions to get datas from TMDb api."""

# Import needed libraries
import os
from dotenv import load_dotenv
import requests
import random
from datetime import datetime

load_dotenv()

# TMDb api key and url to get posters
tmdb_api_key = os.environ.get("TMDB_API_KEY")
poster_base_url = "https://image.tmdb.org/t/p/w500"
youtube_base_url = "https://www.youtube.com/embed/"

print(tmdb_api_key)

# Get the current date and time
current_time = datetime.now()

# Dict for the movie genres and their ids
movie_genres_map = {
    28 : "Action",
    12 : "Adventure",
    16 : "Animation",
    35 : "Comedy",
    80 : "Crime",
    99 : "Documentary",
    18 : "Drama",
    10751 : "Family",
    14 : "Fantasy",
    36 : "History",
    27 : "Horror",
    10402 : "Music",
    9648 : "Mystery",
    10749 : "Romance",
    878 : "Sci-Fi",
    10770 : "TV Movie",
    53 : "Thriller",
    10752 : "War",
    37 : "Western"
}

# Dict for the series genres and their ids 
series_genres_map = {
    10759 : "Action & Adventure",    
    16 : "Animation",
    35 : "Comedy",
    80 : "Crime",
    99 : "Documentary",
    18 : "Drama",
    10751 : "Family",
    10762 : "Kids",
    9648 : "Mystery",
    10763 : "News",
    10764 : "Reality",
    10765 : "Sci-Fi & Fantasy",
    10766 : "Soap",
    10767 : "Talk",
    10768 : "War & Politics",
    37 : "Western"
}


# Function to get movie titles from TMDb
def get_movie_data(genres, release_year):
    # URL to get the movies informations
    url = f"https://api.themoviedb.org/3/discover/movie"
    # Parameters to add to the url
    if '99' in genres or '36' in genres or '37' in genres or "10402" in genres:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": 1
        } 
    elif len(genres) > 1:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": random.randint(1, 2)
        }
    elif release_year == 20 or release_year == 10:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": random.randint(1, 4)
        }
    elif release_year == 5:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": random.randint(1, 3)
        }
    elif release_year == 3:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": random.randint(1, 2)
        }
    elif release_year == 13:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31",
            "page": random.randint(1, 5)
        }
    else:
        params = {
            "api_key": tmdb_api_key,
            "with_genres": ",".join(map(str, genres)),
            "vote_count.gte": 500,
            "vote_average.gte": 7,
            "primary_release_date.gte": f"{str(int(current_time.year) - release_year)}-01-01",  
            "primary_release_date.lte": "2023-12-31"
        }

    # Make the api request
    response = requests.get(url, params=params)
    # If the request is succesful
    if response.status_code == 200:
        # Get the data and return the data
        data = response.json() 
        return data["results"]
    # If the request is not successful
    else:
        return None


# Function to get the currently trending movies or series.
# Take in a parameter called type, which the value should be ("movie" or "tv")
def get_trending_data(type):
    # URL to get the trening datas
    url = f"https://api.themoviedb.org/3/trending/{type.lower()}/day?api_key={tmdb_api_key}"

    # Make the api request
    response = requests.get(url)

    # if successful
    if response.status_code == 200:
        # Store the json in a variable
        trending_data = response.json()

        # Extract information from the response
        trending_results = trending_data["results"]
        
        # If the parameter is 'movie'
        if type.lower() == "movie":
            # Loop through the results, get the genre_ids of each of the movies
            for item in trending_results:
                for i in range(len(item["genre_ids"])):
                    # Use the movie genres dict to replace the ids with their corresponding genres
                    if item["genre_ids"][i] in movie_genres_map:
                        item["genre_ids"][i] = movie_genres_map[item["genre_ids"][i]]
        # If the parameter is "tv"
        elif type.lower() == "tv":
            # Same process as above but with series genres dict
            for item in trending_results:
                for i in range(len(item["genre_ids"])):
                    if item["genre_ids"][i] in series_genres_map:
                        item["genre_ids"][i] = series_genres_map[item["genre_ids"][i]]

        # Finally return the changed results               
        return trending_results
    # If not successful, return none
    else:
        return None


# Function to get the trailer of the movie with TMDb api.
# Takes in one parameter, and that is id of the movie.
def get_trailer(movie_id):
    # A list to store all of the filtered videos' urls
    trailer_list = []
    # URL to get the trailers of the movie
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={tmdb_api_key}'

    # Make an api reqest
    response = requests.get(url)
    # If successful
    if response.status_code == 200:
        # Get the data
        data = response.json()
        # Store the results of the data in a variable
        trailers = data["results"]
        
        # Filter the videos
        # Only stores the video url to the list, if the video contains official or main trailer and doesn't contain the word audio described
        for trailer in trailers:
            if "main" in trailer["name"].lower() and "trailer" in trailer["name"].lower() and not "audio described" in trailer["name"].lower():
                trailer_list.append(trailer["key"])
            elif "official" in trailer["name"].lower() and "trailer" in trailer["name"].lower() and not "audio described" in trailer["name"].lower():
                trailer_list.append(trailer["key"])

        # Only return the last url in the last
        if len(trailer_list) > 0:
            return trailer_list[-1]
        else:
            return "None"
        
    return "None"
