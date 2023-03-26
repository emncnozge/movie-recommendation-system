from django.urls import path

from movieRecommendationAPI import views

urlpatterns = [
    path('', views.root_page),
    path('GetSimilarPosters', views.get_similar_images)
]
