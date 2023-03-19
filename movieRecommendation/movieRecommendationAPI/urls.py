from django.contrib import admin
from django.urls import path

from movieRecommendationAPI import views

urlpatterns = [
    path("", views.get_similar_images)
]