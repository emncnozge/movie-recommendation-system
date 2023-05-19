from django.urls import path

from movieRecommendationAPI import views

urlpatterns = [
    path('', views.root_page),
    path('GetSimilarPosters', views.get_similar_images),
    path('GetAllMovies', views.get_all_movies),
    path('GetMovie', views.get_movie),
    path('GetTextRecommendation', views.get_text_recommendation),
    path('Search', views.search),
]
