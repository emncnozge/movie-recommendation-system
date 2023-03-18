from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input
import tensorflow as tf
import numpy as np
import os

# ResNet50 modelini yükle
model = ResNet50(weights='imagenet', include_top=False)

# Poster klasörünü tanımla
poster_klasoru = 'deneme'

# Poster dosyalarını oku ve özellik vektörleri oluştur
poster_dosyalari = os.listdir(poster_klasoru)
poster_ozellikleri = []
for dosya in poster_dosyalari:
    img_path = os.path.join(poster_klasoru, dosya)
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    features = features.reshape((features.shape[0], 7 * 7 * 2048))
    poster_ozellikleri.append(features)

poster_ozellikleri = np.array(poster_ozellikleri)
nsamples, nx, ny = poster_ozellikleri.shape
poster_ozellikleri = poster_ozellikleri.reshape((nsamples,nx*ny))
# Posterler arasındaki benzerlikleri hesapla
from sklearn.metrics.pairwise import cosine_similarity

for i in range(len(poster_ozellikleri)):
    benzerlik_skorlari = cosine_similarity(poster_ozellikleri[i].reshape(1,-1), poster_ozellikleri)
    benzerlik_skorlari = benzerlik_skorlari[0]
    en_yakin_posterler = np.argsort(benzerlik_skorlari)[-6:-1]
    print("'%s' adlı poster için en benzer 5 poster:" % poster_dosyalari[i])
    for j in reversed(en_yakin_posterler):
        print("    '%s' (%.2f)" % (poster_dosyalari[j], benzerlik_skorlari[j]))
