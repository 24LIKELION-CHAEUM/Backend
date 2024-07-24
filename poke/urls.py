from django.urls import path
from . import views

urlpatterns = [
    path('', views.poke_page, name='poke_page'),
    path('poke/<int:user_id>/', views.poke_user, name='poke_user'),
]
