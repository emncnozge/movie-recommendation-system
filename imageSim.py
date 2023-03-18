import os
import numpy as np
import pickle
import tensorflow as tf

# Veri setinin bulunduğu klasör
data_dir = 'posters780'

# Veri setindeki görüntülerin boyutu
img_size = (300, 300)

# Özellik vektörlerini saklamak için bir NumPy dizisi oluşturun
features = np.zeros((len(os.listdir(data_dir)), 512))

# VGG19 modelini yükleyin
model = tf.keras.applications.VGG19(include_top=False, pooling='avg')

# Veri setindeki her görüntü için özellik vektörünü hesaplayın ve features dizisine kaydedin
i = 0
for filename in os.listdir(data_dir):
    # Görüntüyü yükle
    image_path = os.path.join(data_dir, filename)
    img = tf.keras.preprocessing.image.load_img(image_path, target_size=img_size)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.vgg19.preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    # Özellik vektörünü hesaplayın
    features[i] = model.predict(x)

    # İlerlemeyi yazdırın
    print(f'{i+1}/{len(os.listdir(data_dir))} - {filename}')

    i += 1

# Özellikleri bir dosyaya kaydedin
with open('features.pickle', 'wb') as f:
    pickle.dump(features, f)

