from django.shortcuts import render
from .models import Quote
import random


def index(request):
    return render(request, 'index.html')
