
from django.urls import path
from . import views

app_name = 'movie'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:pk>/', views.detail, name = 'detail'),
    path('movie_add/', views.create_movie, name = 'movie-add'),
    path('<int:pk>/update/', views.MovieUpdate.as_view(), name='movie-update'),
    path('<int:pk>/delete/', views.MovieDelete.as_view(), name='movie-delete'),

    #-------------song section-----------------------
    path('song_list/<str:filter_by>/', views.songs, name='song-list'),
    path('<int:pk>/song_add/', views.SongCreate.as_view(), name='song-add'),
    path('<int:movie_id>/song_delete/<int:song_id>/', views.delete_song, name='song-delete'),

    #-----------------------favorite------------------
    path('<int:song_id>/favorite/', views.favorite, name='favorite'),
    path('<int:movie_id>/favorite_movie/', views.favorite_movie, name='favorite_movie'),


    #--------------video section----------------------
    path('video/', views.Video, name='video'),
    path('video/add_video/', views.create_video, name='add_video'),
    path('video/<int:pk>/', views.Videopage, name = 'videopage'),
    path('video/<int:pk>/delete', views.DeleteVideo.as_view(), name='delete_video'),

    #----------------User signup and login------------
    path('signup/', views.Signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),

]