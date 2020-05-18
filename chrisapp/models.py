from django.db import models

# Create your models (class representing a database table which can be also be a form on screen) here.


class Joke(models.Model):
    joke_text = models.CharField(max_length=200)
    punchline_text = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.joke_text
