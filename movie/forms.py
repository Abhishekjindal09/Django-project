
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
	from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})
