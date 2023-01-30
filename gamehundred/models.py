from django.db import models
from gamehundred.game_of_hundred import game_of_one_hundred as goh
from django.urls import reverse # Used to generate URLs by reversing the URL patterns

# Create your models here.

class Game(models.Model):
    """Model representing a game of one hundred"""
    goal = models.IntegerField(help_text='Enter the number the players must reach', default=100)
    rules = models.TextField(max_length=10000, help_text='Enter a brief description of the game', blank=True)
    number_init = models.IntegerField(help_text='The number at which the players start', default=0)
    max_avail = models.IntegerField(help_text='Maximal available integer', default=10)
    #user = models.ManyToManyField('User', help_text='User')

    def __str__(self):
        """String for representing the Model object."""
        return f'Who attains {self.goal} earlier'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('game-detail', args=[str(self.id)])

class User(models.Model):

    def __str__(self):
        """String for representing the Model object."""
        return self.name

