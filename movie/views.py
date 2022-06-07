from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from movie.models import Movie


class MovieView(ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)


class MovieDetailView(DetailView):
    """ Полное описание фильма """
    model = Movie
