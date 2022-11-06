from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from movie.forms import ReviewForm, RatingForm
from movie.models import Movie, Category, Actor, Genre, Rating


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


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


class AddStarRating(View):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, reqeust):
        form = RatingForm(reqeust.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(reqeust),
                movie_id=int(reqeust.POST.get("movie")),
                defaults={"star_id": int(reqeust.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
