from django.urls import path
from .views import emotion_page, emotion_create, senior_page, add_comment

urlpatterns = [
    path('', emotion_page, name='emotion_page'),
    path('create/', emotion_create, name='emotion_create'),
    path('senior/', senior_page, name='senior_page'),
    path('comment/<int:emotion_id>/', add_comment, name='add_comment'),
]
