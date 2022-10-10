from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createsong/', views.create_song, name="create_song"),
    path('song/', views.song, name='song'),
    path('song/<str:sid>/', views.song, name='song')
]