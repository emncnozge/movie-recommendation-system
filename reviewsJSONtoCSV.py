import csv
import json

# Read the JSON file
with open('movie_reviews.json', 'r', encoding="utf-8") as f:
    data = json.load(f)

# Open the output CSV file for writing
with open('movie_reviews.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL, escapechar='\\')

    # Write the header row
    writer.writerow(['imdb_id', 'reviews'])

    # Write each review as a separate row
    for movie in data:
        for review in movie['reviews']:
            # Replace any line breaks, newlines, quotes, and semicolons with appropriate characters.
            review = review.replace('\n', ' ').replace('\r', '').replace('"', '\\"').replace(';', ',')
            writer.writerow([movie['imdb_id'], review])