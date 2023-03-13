import json

import requests

with open("final_data.json", "r", encoding="utf-8") as f:
    movies = json.load(f)


def get_reviews():
    for i in range(len(movies) - 1, -1, -1):
        response = requests.get(
            "http://localhost:3000/reviews/" + movies[i]["imdb_id"]).json()
        if len(response["reviews"]) > 0:
            reviews = []
            for review in response["reviews"]:
                reviews.append(review["content"])
            movies[i].update({"reviews": reviews})
            if len(movies[i]["genre"]) > 0:
                movies[i]["genre"] = movies[i]["genre"][1:-
                1].replace("'", "").split(", ")
        else:
            del movies[i]
        if i % 100 == 0:
            print(i)
    with open('final_data2.json', 'w', encoding='utf-8') as f:
        json.dump(sorted(
            movies, key=lambda d: d["tmdb_id"]), f, ensure_ascii=False, indent=4, sort_keys=False)


if __name__ == "__main__":
    get_reviews()
