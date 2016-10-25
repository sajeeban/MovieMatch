from .models import Movie_Info
from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render
from .movie_info import MovieInfo


class IndexView(generic.ListView):
    template_name = 'MovieInfo/index.html'
    context_object_name = 'all_movies'

    def get_queryset(self):
        return Movie_Info.objects.all()


def search(request):
    if request.method == 'GET':
        query = request.GET['search_box']
        poster_url = MovieInfo(query).get_movie_poster()
        backdrop_url = MovieInfo(query).get_movie_backdrop()
        context = {
            'poster_url': poster_url,
            'backdrop_url': backdrop_url
        }
        return render(request, 'MovieInfo/detail.html', context)