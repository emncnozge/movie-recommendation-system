import os
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import tensorflow as tf

# Veri setinin bulunduğu klasör
data_dir = 'posters780'

# Veri setindeki görüntülerin boyutu
img_size = (300, 300)

# Özellikleri yükleyin
with open('features.pickle', 'rb') as f:
    features = pickle.load(f)

# VGG19 modelini yükleyin
model = tf.keras.applications.VGG19(include_top=False, pooling='avg')

# Benzer görüntüleri bulmak için bir fonksiyon yazın
def find_similar_images(image_path, n=20):
    # Görüntüyü yükle
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.vgg19.preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    # Özellik vektörünü hesaplayın
    query_feature = model.predict(x)

    # Benzerlikleri hesaplayın
    similarities = cosine_similarity(query_feature, features)[0]

    # En benzer görüntülerin dizinlerini alın
    similar_indices = similarities.argsort()[::-1][:n]

    # En benzer görüntülerin dosya adlarını yazdırın
    for i, idx in enumerate(similar_indices):
        filename = os.listdir(data_dir)[idx]
        print(f'{i+1}. {filename} - similarity: {similarities[idx]}')


find_similar_images('deneme/tt0024216.jpg')

