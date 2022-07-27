from django.urls import path

from movie.views import MovieView, MovieDetailView, AddReview, ActorView

urlpatterns = [
    path('', MovieView.as_view()),
    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', ActorView.as_view(), name='actor_detail')
]