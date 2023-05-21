from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response
from rest_framework.decorators import api_view
import tensorflow as tf
import json
import os
import pickle
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import layers
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import string
import re
import joblib
import os
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

data_dir = '../posters780'

img_size = (300, 300)

with open('../featuresResNet50.pickle', 'rb') as f:
    features = pickle.load(f)

model = tf.keras.applications.ResNet50(include_top=False, pooling='avg')

# Load model
directory = "saved_model"
file_path = os.path.join(directory, "nearest_neighbors.joblib")
if os.path.exists(directory):
    nn = joblib.load(file_path)


def find_similar_images(image_path, amount=5, adult=1):
    img = tf.keras.preprocessing.image.load_img(
        "../posters780/" + image_path + ".jpg", target_size=img_size)
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    x = np.expand_dims(x, axis=0)

    query_feature = model.predict(x)

    similarities = cosine_similarity(query_feature, features)[0]

    similar_indices = similarities.argsort()[::-1]
    total = list()
    title = ""
    original_genre = []
    for data in final_data:
        if data["imdb_id"] == image_path:
            title = data["title"],
            original_genre = data["genre"]
            break
    try:
        for i, idx in enumerate(similar_indices):
            if i != 0:
                imdb_id = os.listdir(data_dir)[idx][:-4]
                for data in final_data:
                    if (len(total) > amount):
                        return total[:amount], title
                    if data["imdb_id"] == imdb_id and int(data["adult"]) == int(adult):
                        for genre in original_genre:
                            if genre in data["genre"]:
                                total.append({
                                    "imdb_id": imdb_id,
                                    "poster_path": data["poster_path"],
                                    "title": data["title"],
                                    "similarity": f'{similarities[idx]:.2f}'
                                })
                                break
                        break

    except Exception as e:
        print(e)
    return total[:amount], title


with open('../movie_info.json', 'r', encoding="utf-8") as f:
    final_data = json.load(f)


@api_view(["GET"])
def root_page(request):
    return Response("Root page")


@api_view(["GET"])
def search(request):
    try:
        search_term = str(request.GET.get("search")).strip()
        movies = []
        exact = []
        partial = []
        for movie in final_data:
            if len(exact) >= 5:
                return Response({
                    "status": True,
                    "data": exact,
                })
            for word in str(movie["title"]).split():
                if str(word).lower() == search_term.lower():
                    exact.append(movie)
            if search_term.lower() in str(movie["title"]).lower():
                partial.append(movie)
        # Exact içindeki filmleri partial'dan çıkar
        exact = [movie for movie in exact if movie not in partial]
        movies = exact[:5]

        if len(movies) < 5:
            remaining = 5 - len(movies)
            movies += partial[:remaining]

        return Response({
            "status": True,
            "data": movies,
        })
    except Exception as e:
        return Response({
            "status": False,
            "message": "Error occured: " + str(e)
        })


@api_view(["POST"])
def get_similar_images(request):
    try:
        data = request.data
        if "movie_id" in data and "adult" in data:
            movie_id = data["movie_id"]
            adult = data["adult"]
            if "amount" in data:
                amount = int(data["amount"])
                similars, title = find_similar_images(
                    image_path=movie_id, amount=amount + 1, adult=adult)

                return Response({
                    "status": True,
                    "data": similars,
                    "movie_name": title
                })
            else:
                similars, title = find_similar_images(
                    image_path=movie_id, adult=1)
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


max_vocab_length = 10000
max_length = 6063
embedding = layers.Embedding(input_dim=max_vocab_length,
                             output_dim=64,
                             input_length=max_length)
text_vectorizer = TextVectorization(max_tokens=max_vocab_length,
                                    output_mode="int",
                                    output_sequence_length=max_length,
                                    pad_to_max_tokens=True)
translator = str.maketrans('', '', string.punctuation)
# Remove whitespace
reviews = pd.read_csv("./reviewsClean.csv")
if os.path.isfile("reviews.pickle"):
    with open('reviews.pkl', 'rb') as f:
        reviews = pickle.load(f)
else:
    for i in range(len(reviews)):
        reviews["reviews"][i] = reviews["reviews"][i].lower()
        reviews["reviews"][i] = re.sub(r'\d+', '', reviews["reviews"][i])
        reviews["reviews"][i] = reviews["reviews"][i].translate(translator)
        reviews["reviews"][i] = " ".join(reviews["reviews"][i].split())
    with open('reviews.pkl', 'wb') as f:
        pickle.dump(reviews, f)

text_vectorizer.adapt(reviews["reviews"])


@api_view(["POST"])
def get_text_recommendation(request):
    try:
        data = request.data

        if "searched" in data:
            searched = data["searched"].lower()
            text = embedding(text_vectorizer(searched))
            neighbours = nn.kneighbors(text, return_distance=False)
            similars = []
            for index in neighbours[0]:
                movie_id = reviews.iloc[index]["imdb_id"]
                for movie in final_data:
                    if movie["imdb_id"] == movie_id:
                        similars.append(
                            {"imdb_id": movie_id, "poster_path": movie["poster_path"], "title": movie["title"]})

            return Response({
                "status": True,
                "data": similars
            })

        else:
            return Response(False)
    except AttributeError:
        return Response({
            "status": False,
            "message": "Movie ID not provided."
        })
    except Exception as e:
        return Response({
            "status": False,
            "message": "Error occured"
        })


@api_view(["GET"])
def get_all_movies(request):
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
