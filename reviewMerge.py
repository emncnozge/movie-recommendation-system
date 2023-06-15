import pandas as pd

df = pd.read_csv('movie_reviews.csv')

df_grouped = df.groupby('imdb_id')['reviews'].apply(
    lambda x: ' '.join(x)).reset_index()

df_grouped.to_csv('yeni_dosya_adı.csv', index=False)
