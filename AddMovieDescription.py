import json

import requests

with open("movie_info.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

with open(".credentials", "r", encoding="utf-8") as f:
    TMDB_API_KEY = json.load(f)["TMDB_API_KEY"]


def add_movie_description():
    for i in range(len(movies) - 1, -1, -1):
        response = requests.get("https://api.themoviedb.org/3/movie/" + str(
            movies[i]["imdb_id"]) + "?api_key=" + TMDB_API_KEY + "&language=en-US").json()
        movies[i].update({"overview": response["overview"]})
        if i % 100 == 0:
            print(i)
            print(movies[i])
    with open('movie_info.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    add_movie_description()
