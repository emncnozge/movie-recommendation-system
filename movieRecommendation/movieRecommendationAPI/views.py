import os
import pickle

import numpy as np
import tensorflow as tf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


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
        if "movie_id" in data:
            movie_id = data["movie_id"]
            if "amount" in data:
                amount = int(data["amount"])
                return Response(find_similar_images(movie_id, amount + 1))
            else:
                return Response(find_similar_images(movie_id))
        else:
            return Response(False)
    except AttributeError:
        return Response("Movie ID not provided.")
    except Exception:
        return Response("Error occured.")


data_dir = '../posters780'

img_size = (300, 300)

with open('../features.pickle', 'rb') as f:
    features = pickle.load(f)

model = tf.keras.applications.VGG19(include_top=False, pooling='avg')


def find_similar_images(image_path, amount=5):
    img = tf.keras.preprocessing.image.load_img("../posters780/" + image_path + ".jpg", target_size=img_size)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.vgg19.preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    query_feature = model.predict(x)

    similarities = cosine_similarity(query_feature, features)[0]

    similar_indices = similarities.argsort()[::-1][:amount]

    res = list()
    for i, idx in enumerate(similar_indices):
        if i != 0:
            filename = os.listdir(data_dir)[idx]
            res.append({"filename": filename, "similarity": f'{similarities[idx]:.2f}'})
    return res
