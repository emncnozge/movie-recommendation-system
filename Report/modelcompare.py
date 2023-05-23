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

with open('./featuresResNet50V2.pickle', 'rb') as f:
    features_resnet50v2 = pickle.load(f)

with open('./featuresVGG19.pickle', 'rb') as f:
    features_vgg19 = pickle.load(f)

with open('./featuresResNet152V2.pickle', 'rb') as f:
    features_resnet152v2 = pickle.load(f)

with open('./featuresResNet101V2.pickle', 'rb') as f:
    features_resnet101v2 = pickle.load(f)

# VGG16 ve ResNet50 benzerliklerini hesaplayın
vgg16_similarities = cosine_similarity(features_vgg16)
resnet50_similarities = cosine_similarity(features_resnet50)
resnet50v2_similarities = cosine_similarity(features_resnet50v2)
vgg19_similarities = cosine_similarity(features_vgg19)
resnet152v2_similarities = cosine_similarity(features_resnet152v2)
resnet101v2_similarities = cosine_similarity(features_resnet101v2)


plt.figure(figsize=(16, 9))
plt.plot(range(0, 25), vgg16_similarities[0][::320],
         marker='o', linestyle='solid', label='VGG16')
plt.plot(range(0, 25), vgg19_similarities[0][::320],
         marker='o', linestyle='solid', label='VGG19')
plt.plot(range(0, 25), resnet50_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet50')
plt.plot(range(0, 25), resnet50v2_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet50V2')
plt.plot(range(0, 25), resnet101v2_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet101V2')
plt.plot(range(0, 25), resnet152v2_similarities[0][::320],
         marker='o', linestyle='solid', label='ResNet152V2')


vgg16_mean = np.mean(vgg16_similarities[0])
vgg19_mean = np.mean(vgg19_similarities[0])
resnet50_mean = np.mean(resnet50_similarities[0])
resnet50v2_mean = np.mean(resnet50v2_similarities[0])
resnet101v2_mean = np.mean(resnet101v2_similarities[0])
resnet152v2_mean = np.mean(resnet152v2_similarities[0])


plt.xlabel('Görüntü (320\'li Gruplar)')
plt.ylabel('Benzerlik Oranı')
plt.title('VGG16 - VGG19 - ResNet50 - ResNet50V2 - ResNet101V2 - ResNet152V2 Benzerlik Performans Karşılaştırması')
legend_text = [
    f'VGG16 (Ortalama: {vgg16_mean:.2f})',
    f'VGG19 (Ortalama: {vgg19_mean:.2f})',
    f'ResNet50 (Ortalama: {resnet50_mean:.2f})',
    f'ResNet50V2 (Ortalama: {resnet50v2_mean:.2f})',
    f'ResNet101V2 (Ortalama: {resnet101v2_mean:.2f})',
    f'ResNet152V2 (Ortalama: {resnet152v2_mean:.2f})'
]
plt.legend(legend_text)
plt.grid(True)
plt.yticks(np.arange(0.2, 1.1, 0.05).round(2))
plt.ylim(0.2, 1.049)
plt.tight_layout()
plt.savefig('ModelComparison.png', dpi=600)
plt.show()
