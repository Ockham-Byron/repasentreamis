from django.urls import path
from django.utils.translation import gettext as _
from .views import *



urlpatterns = [
    path(_('all-menus'), all_menus, name="all-menus"),
    path(_('add-menu'), add_menu, name="add-menu"),
    path(_('all-recipes'), all_recipes, name="all-recipes"),
    path(_('add-recipe'), add_recipe, name="add-recipe"),
    path(_('add-recipe-to-menu/<slug>'), add_recipe_to_menu, name="add-recipe-to-menu"),
    path(_('recipe/<slug>'), recipe_detail, name="recipe-detail"),

    #comments
    path(_('add-comment/<slug>'), add_comment, name="add-comment"),

    #musics
    path(_('add-music/<slug>'), add_music, name="add-music"),

    #anecdotes
    path(_('anecdote/<slug>'), add_anecdote, name="add-anecdote"),


]