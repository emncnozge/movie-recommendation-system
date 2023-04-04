import os
import pickle

import numpy as np
import json
import tensorflow as tf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

with open('../final_data.json', 'r', encoding="utf-8") as f:
    final_data = json.load(f)


@api_view(["GET"])
def root_page(request):
    return Response("Root page")


# @api_view(["GET"])
# def get_similar_images(request):
#     movie_id = request.GET.get("movie_id")
#     amount = int(request.GET.get("amount"))
#     if movie_id is None:
#         return Response()
#     if amount is None:
#         amount = 10
#     return Response(find_similar_images(movie_id, amount + 1))


@api_view(["POST"])
def get_similar_images(request):
    try:
        data = request.data.dict()
        if "movie_id" in data and "adult" in data:
            movie_id = data["movie_id"]
            adult = data["adult"]
            if "amount" in data:
                amount = int(data["amount"])
                return Response(find_similar_images(image_path=movie_id, amount=amount + 1, adult=adult))
            else:
                return Response(find_similar_images(image_path=movie_id, adult=1))

        else:
            return Response(False)
    except AttributeError:
        return Response("Movie ID not provided.")
    except Exception:
        return Response("Error occured.")


data_dir = '../posters780'

img_size = (300, 300)

with open('../featuresResNet50.pickle', 'rb') as f:
    features = pickle.load(f)

model = tf.keras.applications.ResNet50(include_top=False, pooling='avg')


def find_similar_images(image_path, amount=5, adult=1):
    img = tf.keras.preprocessing.image.load_img("../posters780/" + image_path + ".jpg", target_size=img_size)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    query_feature = model.predict(x)

    similarities = cosine_similarity(query_feature, features)[0]

    similar_indices = similarities.argsort()[::-1][:50]
    total = list()
    try:
        for i, idx in enumerate(similar_indices):
            if i != 0:
                filename = os.listdir(data_dir)[idx][:-4]
                for data in final_data:
                    if data["imdb_id"] == filename and int(data["adult"]) == int(adult):
                        total.append({"filename": filename, "similarity": f'{similarities[idx]:.2f}'})
                        break

    except Exception as e:
        print(e)
    return total
