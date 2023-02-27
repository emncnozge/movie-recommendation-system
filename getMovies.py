import json

import requests

with open("raw_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

with open(".credentials", "r", encoding="utf-8") as f:
    TMDB_API_KEY = json.load(f)["TMDB_API_KEY"]

final_data = []

for i in range(len(raw_data) - 1, -1, -1):
    if raw_data[i]["original_language"] == "en" and len(str(raw_data[i]["id"])) > 0:
        r = requests.get("https://api.themoviedb.org/3/movie/" + str(
            raw_data[i]["id"]) + "?api_key=" + TMDB_API_KEY + "&language=en-US").json()
        if "poster_path" in r and r["poster_path"] is not None:
            poster_url = ("https://image.tmdb.org/t/p/w780" + r["poster_path"])
            raw_data[i].update({"poster_url": poster_url})
        if "imdb_id" in r and r["imdb_id"] is not None:
            raw_data[i].update({"imdb_id": r["imdb_id"]})

    if raw_data[i]["original_language"] == "en" and len(str(raw_data[i]["id"])) > 0 and "id" in raw_data[
        i] and "imdb_id" in raw_data[i] and "original_title" in raw_data[i] and "poster_url" in raw_data[
        i] and "genre" in raw_data[i]:
        final_data.append(
            {"tmdb_id": raw_data[i]["id"], "imdb_id": raw_data[i]["imdb_id"], "title": raw_data[i]["original_title"],
             "poster_path": raw_data[i]["poster_url"], "genre": raw_data[i]["genre"]})

with open('final_data.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(final_data, key=lambda d: d["tmdb_id"]),
              f, ensure_ascii=False, indent=4, sort_keys=False)
