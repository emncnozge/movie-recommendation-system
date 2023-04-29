import tensorflow as tf
import random
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import layers
import pandas as pd
from sklearn.neighbors import NearestNeighbors

reviews = pd.read_csv("movieReviews.csv")

#print(len(reviews["reviews"][0].split()))
#print(round(sum([len(i.split())for i in reviews["reviews"]])/len(reviews["reviews"])))

max_vocab_length = 10000
max_length = 257

text_vectorizer = TextVectorization(max_tokens=max_vocab_length,
                                    output_mode="int",
                                    output_sequence_length=max_length)

text_vectorizer.adapt(reviews["reviews"])


#random_sentence = random.choice(reviews["reviews"])
#print(random_sentence)
#print(text_vectorizer(random_sentence))

#words_in_vocab = text_vectorizer.get_vocabulary()
#top_5_words = words_in_vocab[:5]
#bottom_5_words = words_in_vocab[-5:]
#print(top_5_words,bottom_5_words)

embedding = layers.Embedding(input_dim=max_vocab_length,
                             output_dim=64,
                             input_length=max_length)

#print(embedding(text_vectorizer(random_sentence)))

pooling_layer = layers.GlobalAveragePooling1D()

nn = NearestNeighbors(n_neighbors=5)
x = text_vectorizer(reviews["reviews"])
x = embedding(x)
x = pooling_layer(x)
nn.fit(x)

text = embedding(text_vectorizer("love"))
neighbours = nn.kneighbors(text, return_distance=False)
print(neighbours,neighbours.shape)