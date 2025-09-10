from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('top/', views.top_quotes, name='top_quotes')
]
