import json

import requests

with open("final_data.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

with open(".credentials", "r", encoding="utf-8") as f:
    TMDB_API_KEY = json.load(f)["TMDB_API_KEY"]


def get__keywords_and_adult():
    for i in range(len(movies) - 1, -1, -1):
        response = requests.get("https://api.themoviedb.org/3/movie/" + str(
            movies[i]["imdb_id"]) + "?api_key=" + TMDB_API_KEY + "&language=en-US").json()
        movies[i].update({"adult": 1 if response["adult"] else 0})
        response = requests.get("https://api.themoviedb.org/3/movie/" + str(
            movies[i]["tmdb_id"]) + "/keywords?api_key=" + TMDB_API_KEY).json()
        if len(response["keywords"]) > 0:
            movies[i].update({"keywords": response["keywords"]})
        else:
            movies[i].update({"keywords": {}})
        if i % 100 == 0:
            print(i)
    with open('final_data2.json', 'w', encoding='utf-8') as f:
        json.dump(sorted(
            movies, key=lambda d: d["tmdb_id"]), f, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    get__keywords_and_adult()
