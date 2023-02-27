import json
import multiprocessing
from math import floor

import requests


def download_poster(start, end, movies):
    if end < -1:
        end = -1
    for i in range(start, end, -1):
        response = requests.get(movies[i]["poster_path"])
        open("./posters780/" + movies[i]["imdb_id"] + ".jpg", "wb").write(response.content)


if __name__ == "__main__":
    with open("final_data.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    processes = []
    size = len(movies) - 1
    remaining = size

    for i in range(multiprocessing.cpu_count()):
        process = multiprocessing.Process(
            target=download_poster, args=(remaining, floor(remaining - size / multiprocessing.cpu_count()), movies))
        remaining = floor(remaining - size / multiprocessing.cpu_count())
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
