from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from movie.forms import ReviewForm
from movie.models import Movie, Category, Actor, Genre


class GenreYear:
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year").distinct()


class MovieView(GenreYear, ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movie/movie_list.html'
    context_object_name = 'movie_list'


class MovieDetailView(GenreYear, DetailView):
    """ Полное описание фильма """
    model = Movie
    template_name = 'movie/movie_detail.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'


class AddReview(View):
    """ Отзывы """
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актёрах"""
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'


class FilterMovieView(GenreYear, ListView):
    """Фильтр фильмов"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

