from django.views import generic
from .models import MovieList,song, video
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm, UserProfileForm, MovieCreate, AddVideo
from django.db.models import Q

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        movies = MovieList.objects.filter(user=request.user)
        song_results = song.objects.all()
        query = request.GET.get("q")
        if query:
            movies = movies.filter(
                Q(movie_name__icontains=query) |
                Q(movie_year__icontains=query)
            ).distinct()
            song_results = song_results.filter(
                Q(song_name__icontains=query)
            ).distinct()
            return render(request, 'movie/index.html', {
                'movies': movies,
                'songs': song_results,
            })
        else:
            return render(request, 'movie/index.html', {'movies': movies})


def detail(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        user = request.user
        movie = get_object_or_404(MovieList, pk=pk)
        return render(request, 'movie/detail.html', {'movie': movie, 'user': user})


def create_movie(request):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        form = MovieCreate(request.POST or None, request.FILES or None)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.movie_logo = request.FILES['movie_logo']

            movie.save()
            return render(request, 'movie/detail.html', {'movie': movie})

        context = {
            "form": form,
        }
        return render(request, 'movie/movielist_form.html', context)


class MovieUpdate(UpdateView):
    model = MovieList
    fields = ['movie_name', 'movie_year', 'movie_logo','is_favorite']
    
class MovieDelete(DeleteView):
    model = MovieList
    success_url = reverse_lazy('movie:index')

class SongCreate(CreateView):
    model = song
    fields = ['movie','song_name','song_type','song_audio','is_favorite']


def delete_song(request, movie_id, song_id):
    movie = get_object_or_404(MovieList, pk=movie_id)
    songs = song.objects.get(pk=song_id)
    songs.delete()
    return render(request, 'movie/detail.html', {'movie': movie})

#--------------------------------favorite--------------------------------------
def favorite(request, song_id):
    songs = get_object_or_404(song, pk=song_id)
    try:
        if songs.is_favorite:
            songs.is_favorite = False
        else:
            songs.is_favorite = True
        songs.save()
    except (KeyError, song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_movie(request, movie_id):
    movies = get_object_or_404(MovieList, pk=movie_id)
    try:
        if movies.is_favorite:
            movies.is_favorite = False
        else:
            movies.is_favorite = True
        movies.save()
    except (KeyError, movie.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

#---------------------------------video section-------------------------------------

def Video(request):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        videos = video.objects.filter(user=request.user)
    return render(request, 'movie/video.html', {'all_videos': videos})


def detail(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        user = request.user
        movie = get_object_or_404(MovieList, pk=pk)
        return render(request, 'movie/detail.html', {'movie': movie, 'user': user})

def Videopage(request, pk):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        user = request.user
        videos = get_object_or_404(video, pk=pk)
        return render(request, 'movie/videopage.html', {'video': videos, 'user': user})

def create_movie(request):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        form = MovieCreate(request.POST or None, request.FILES or None)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.movie_logo = request.FILES['movie_logo']

            movie.save()
            return render(request, 'movie/detail.html', {'movie': movie})

        context = {
            "form": form,
        }
        return render(request, 'movie/movielist_form.html', context)

def create_video(request):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        form = AddVideo(request.POST or None, request.FILES or None)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.video_logo = request.FILES['video_logo']
            video.video_song = request.FILES['video_song']

            video.save()
            return render(request, 'movie/videopage.html', {'video': video})

        context = {
            "form": form,
        }
        return render(request, 'movie/video_form.html', context)
    
class DeleteVideo(DeleteView):
    model = video
    success_url = reverse_lazy('movie:video')

#-------------------------------------song section-------------------------------------
def songs(request, filter_by):
    if not request.user.is_authenticated:
        return render(request, 'movie/login.html')
    else:
        try:
            song_ids = []
            for movie in MovieList.objects.filter(user=request.user):
                for songs in movie.song_set.all():
                    song_ids.append(songs.pk)
            users_songs = song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except MovieList.DoesNotExist:
            users_songs = []
        return render(request, 'movie/song_list.html', {
            'all_songs': users_songs,
            'filter_by': filter_by,
        })


#------------------user register and login----------------------------------------------


def Signup(request):
    form = UserForm(request.POST or None)
    profile_form = UserProfileForm(request.POST, request.FILES)
    
    if form.is_valid() and profile_form.is_valid():
        user = form.save(commit=False)
        profile = profile_form.save(commit= False)
        profile.user = user

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        profile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                movies = MovieList.objects.filter(user=request.user)
                return render(request, 'movie/index.html', {'movies': movies})
    context = {
        "form": form,
        "profile_form":profile_form,
    }
    return render(request, 'movie/signup.html', context)

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                movies = MovieList.objects.filter(user=request.user)
                return render(request, 'movie/index.html', {'movies': movies})
            else:
                return render(request, 'movie/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'movie/login.html', {'error_message': 'Invalid login'})
    return render(request, 'movie/login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'movie/login.html' , context)


from django.contrib.auth.models import User

class Profile(generic.DetailView):
    model = User
    template_name = 'movie/profile.html'

    context_object_name = 'user'
    queryset = User.objects.all()