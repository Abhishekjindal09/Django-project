
from django import forms
from django.contrib.auth.models import User
from movie.models import userprofile
from .models import MovieList,song, video

class MovieCreate(forms.ModelForm):

	class Meta:
	    model = MovieList
	    fields = ['movie_name','movie_year' , 'movie_logo', 'is_favorite']

class AddVideo(forms.ModelForm):

    class Meta:
        model = video
        fields = ['video_name', 'genre', 'release_year', 'video_logo', 'video_song']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput)
    email = forms.EmailField(required= True)

    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = userprofile
        fields = ['phone_number', 'profile_photo', 'bio']