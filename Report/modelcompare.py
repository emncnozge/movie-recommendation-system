import os
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn.metrics.pairwise import cosine_similarity

# Veri setinin bulunduğu klasör
data_dir = './posters780'

# İlk 50 görüntü için özellikleri yükleyin
with open('./featuresVGG16.pickle', 'rb') as f:
    features_vgg16 = pickle.load(f)

with open('./featuresResNet50.pickle', 'rb') as f:
    features_resnet50 = pickle.load(f)

with open('./featuresVGG19.pickle', 'rb') as f:
    features_vgg19 = pickle.load(f)

with open('./featuresResNet152V2.pickle', 'rb') as f:
    features_resnet152v2 = pickle.load(f)

with open('./featuresResNet152V2.pickle', 'rb') as f:
    features_resnet101v2 = pickle.load(f)

# VGG16 ve ResNet50 benzerliklerini hesaplayın
vgg16_similarities = cosine_similarity(features_vgg16)
resnet50_similarities = cosine_similarity(features_resnet50)
vgg19_similarities = cosine_similarity(features_vgg19)
resnet152v2_similarities = cosine_similarity(features_resnet152v2)
resnet101v2_similarities = cosine_similarity(features_resnet101v2)

# Örnekleme için adım değeri

# Benzerlikleri karşılaştıran grafik
plt.figure(figsize=(12, 6))
plt.plot(range(0, 25), vgg16_similarities[0][::320],
         marker='o', linestyle='solid', label='VGG16')
plt.plot(range(0, 25), vgg19_similarities[0][::320],
         marker='o', linestyle='solid', label='VGG19')
plt.plot(range(0, 25), resnet50_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet50')
plt.plot(range(0, 25), resnet101v2_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet101V2')
plt.plot(range(0, 25), resnet152v2_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet152V2')

plt.xlabel('Görüntü (320\'li Gruplar)')
plt.ylabel('Benzerlik')
plt.title('VGG16 - VGG16 - ResNet50 - ResNet101 - ResNet152 Benzerlik Performans Karşılaştırması')
plt.legend()
plt.grid(True)
plt.yticks(np.arange(0, 1.1, 0.03).round(2))
plt.ylim(0.15, 1)
plt.tight_layout()
plt.savefig('ModelComparison.png', dpi=900)
plt.show()
