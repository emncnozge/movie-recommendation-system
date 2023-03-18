from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import tensorflow as tf
import numpy as np
import os
import time
import json

# ResNet50 modelini yükle
model = ResNet50(weights='imagenet', include_top=False)
start = time.time()
# Poster klasörünü tanımla
poster_klasoru = 'posters780'
poster_similarities = {}
# Poster dosyalarını oku ve özellik vektörleri oluştur
poster_dosyalari = os.listdir(poster_klasoru)
poster_ozellikleri = []
for dosya in poster_dosyalari:
    img_path = os.path.join(poster_klasoru, dosya)
    img = image.load_img(img_path, target_size=(300, 300))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    features = features.reshape((features.shape[0], 204800))
    poster_ozellikleri.append(features)

poster_ozellikleri = np.array(poster_ozellikleri)
nsamples, nx, ny = poster_ozellikleri.shape
poster_ozellikleri = poster_ozellikleri.reshape((nsamples, nx * ny))
# Posterler arasındaki benzerlikleri hesapla
from sklearn.metrics.pairwise import cosine_similarity
new_list = list()
for i in range(len(poster_ozellikleri)):
    benzerlik_skorlari = cosine_similarity(poster_ozellikleri[i].reshape(1, -1), poster_ozellikleri)
    benzerlik_skorlari = benzerlik_skorlari[0]
    en_yakin_posterler = np.argsort(benzerlik_skorlari)[-11:-1]
    new_list.clear()
    for j in reversed(en_yakin_posterler):
        new_list.append([poster_dosyalari[j][:-4], "{:.2f}".format(benzerlik_skorlari[j])])
    poster_similarities[poster_dosyalari[i][:-4]] = new_list
print("Elapsed time:", time.time() - start)

with open('poster_similarities.json', 'w', encoding='utf-8') as f:
    json.dump(poster_similarities, f, ensure_ascii=False, indent=4, sort_keys=False)
