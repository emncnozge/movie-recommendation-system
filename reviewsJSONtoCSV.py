import csv
import json

with open('movie_reviews.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

with open('movie_reviews.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar='\\')

    writer.writerow(['imdb_id', 'reviews'])

    for movie in data:
        for review in movie['reviews']:
            review = review.replace('\n', ' ').replace(
                '\r', '').replace('"', '\\"').replace(';', ',')
            writer.writerow([movie['imdb_id'], review])
