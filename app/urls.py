from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('top/', views.top_quotes, name='top_quotes'),
    path('add/', views.add_quote, name='add_quote')
]
