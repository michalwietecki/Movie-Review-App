from django.shortcuts import render
from account.models import Account
from reviews.models import Movie
# Create your views here.

def base_screen_view(request):

    context = {}

    top_movies = Movie.objects.order_by('-rating')[:3]
    context['top_movies'] = top_movies

    return render(request, "general/home.html", context)
