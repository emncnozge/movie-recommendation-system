import json
import os
import pickle

import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity

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

    similar_indices = similarities.argsort()[::-1][:amount]
    total = list()
    title = ""
    for data in final_data:
        if data["imdb_id"] == image_path:
            title = data["title"]
            break
    try:
        for i, idx in enumerate(similar_indices):
            if i != 0:
                imdb_id = os.listdir(data_dir)[idx][:-4]
                for data in final_data:
                    if data["imdb_id"] == imdb_id and int(data["adult"]) == int(adult):
                        total.append({
                            "imdb_id": imdb_id,
                            "poster_path": data["poster_path"],
                            "title": data["title"],
                            "similarity": f'{similarities[idx]:.2f}'
                        })
                        break

    except Exception as e:
        print(e)
    return total, title


with open('../movie_info.json', 'r', encoding="utf-8") as f:
    final_data = json.load(f)


@api_view(["GET"])
def root_page(request):
    return Response("Root page")


@api_view(["POST"])
def get_similar_images(request):
    print(request.data)
    try:
        data = request.data
        if "movie_id" in data and "adult" in data:
            print(data)
            movie_id = data["movie_id"]
            adult = data["adult"]
            if "amount" in data:
                amount = int(data["amount"])
                similars, title = find_similar_images(image_path=movie_id, amount=amount + 1, adult=adult)

                return Response({
                    "status": True,
                    "data": similars,
                    "movie_name": title
                })
            else:
                similars, title = find_similar_images(image_path=movie_id, adult=1)
                return Response({
                    "status": True,
                    "data": similars,
                    "movie_name": title
                })

        else:
            return Response(False)
    except AttributeError:
        return Response({
            "status": False,
            "message": "Movie ID not provided."
        })
    except Exception:
        return Response({
            "status": False,
            "message": "Error occured."
        })


@api_view(["GET"])
def get_all_movies(request):
    print(request.query_params)
    try:
        start = int(request.query_params.get("start", 0))
        end = int(request.query_params.get("end", len(final_data)))
        data = final_data[start:end]
        return Response({
            "status": True,
            "data": data,
            "max": len(final_data)
        })
    except Exception:
        return Response({
            "status": False,
            "message": "Error occured."
        })


@api_view(["POST"])
def get_movie(request):
    try:
        if "movie_id" in request.data:
            imdb_id = request.data["movie_id"]
            for movie in final_data:
                if movie["imdb_id"] == imdb_id:
                    return Response({
                        "status": True,
                        "data": movie
                    })
        else:
            return Response({
                "status": False,
                "message": "'movie_id' not provided."
            })
    except Exception:
        return Response({
            "status": False,
            "message": "Error occured."
        })
