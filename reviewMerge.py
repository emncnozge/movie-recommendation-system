import pandas as pd

# CSV dosyasını yükleyin
df = pd.read_csv('movie_reviews.csv')

# imdb_id'ye göre gruplayın ve review sütunlarındaki değerleri birleştirin
df_grouped = df.groupby('imdb_id')['reviews'].apply(lambda x: ' '.join(x)).reset_index()

# Gruplanmış verileri bir CSV dosyasına yazdırın
df_grouped.to_csv('yeni_dosya_adı.csv', index=False)
