from django.db import models

# Create your models here.

class Movie_Info(models.Model):

    movie_name = models.CharField(max_length=250)
    poster_url = models.CharField(max_length=1000)

    def __str__(self):

        return self.movie_name