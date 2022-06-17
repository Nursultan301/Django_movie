from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, View

from movie.forms import ReviewForm
from movie.models import Movie


class MovieView(ListView):
    """ Список фильмов """
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movie/movie_list.html'
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    """ Полное описание фильма """
    model = Movie
    template_name = 'movie/movie_detail.html'
    context_object_name = 'movie'


class AddReview(View):
    """ Отзывы """

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.save()
        else:
            form = ReviewForm()
        return redirect(movie.get_absolute_url())
