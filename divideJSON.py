import json


with open('final_data.json', 'r', encoding="utf-8") as f:
    data = json.load(f)


movieInfo = []
movieReviews = []


for movie in data:
    movieInfo.append({
        "imdb_id": movie["imdb_id"],
        "title": movie["title"],
        "poster_path": movie["poster_path"],
        "adult": movie["adult"],
        "genre": movie["genre"],
        "keywords": movie["keywords"],
    })

    movieReviews.append({
        "tmdb_id": movie["tmdb_id"],
        "imdb_id": movie["imdb_id"],
        "reviews": movie["reviews"]
    })


with open('movie_info.json', 'w') as f:
    json.dump(movieInfo, f, indent=4, sort_keys=False)


with open('movie_reviews.json', 'w') as f:
    json.dump(movieReviews, f, indent=4, sort_keys=False)
