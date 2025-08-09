from django.shortcuts import render
from . import models
from django.http import JsonResponse

# Create your views here.

def watchlist(request):
    movies = models.Movie.objects.all()
    data = {
        'movies': list(movies.values())
    }
    return JsonResponse(data)

