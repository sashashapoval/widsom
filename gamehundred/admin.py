from django.contrib import admin

# Register your models here.

from .models import Game

#admin.site.register(Game)

# Define the admin class
class GameAdmin(admin.ModelAdmin):
    list_display = ('goal', 'number_init')

# Register the admin class with the associated model
admin.site.register(Game, GameAdmin)

