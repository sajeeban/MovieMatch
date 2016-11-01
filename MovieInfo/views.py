from .models import Movie_Info
from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .movie_info import MovieInfo
from .forms import UserForm, LoginForm


class IndexView(generic.ListView):
    template_name = 'MovieInfo/index.html'
    context_object_name = 'all_movies'

    def get_queryset(self):
        return Movie_Info.objects.all()


class UserFormView(View):
    form_class = UserForm
    template_name = 'MovieInfo/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # cleaned data (correctly formatted)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # validations
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form})


def login_view(request):
    title = "Login"
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('index')

    return render(request, "MovieInfo/login.html", {"form": form, "title": title})


def logout_view(request):
    logout(request)
    return redirect('index')


def search(request):
    if request.method == 'GET':
        query = request.GET['search_box']
        movie_info = MovieInfo(query).get_movie_info()
        poster_url = movie_info['poster_url']
        backdrop_url = movie_info['backdrop_url']
        overview = movie_info['overview']
        revenue = movie_info['revenue']
        title = movie_info['title']
        tagline = movie_info['tagline']
        budget = movie_info['budget']
        release_date = movie_info['release_date']
        runtime = movie_info['runtime']

        context = {
            'poster_url': poster_url,
            'backdrop_url': backdrop_url,
            'overview': overview,
            'revenue': revenue,
            'title': title,
            'tagline': tagline,
            'release_date': release_date,
            'budget': budget,
            'runtime': runtime
        }
        return render(request, 'MovieInfo/detail.html', context)