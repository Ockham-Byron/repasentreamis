from django.contrib import admin
from .models import *

# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
  list_display=('name', 'created_at', 'updated_at')
  

admin.site.register(Recipe, RecipeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('recipe', 'author', 'rating')

admin.site.register(Comment, CommentAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display=('created_at',)

admin.site.register(Menu, MenuAdmin)

admin.site.register(Music)
admin.site.register(Anecdote)
