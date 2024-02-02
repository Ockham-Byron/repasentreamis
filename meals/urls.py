from django.urls import path
from django.utils.translation import gettext as _
from .views import *



urlpatterns = [
    path(_('all-meals'), all_meals, name="all-meals"),
    path(_('add-meal'), add_meal, name="add-meal"),
    path(_('add-meal/<slug>'), add_meal_from_group, name="add-meal-from-group"),
    path(_('edit-meal/<slug>'), edit_meal, name="edit-meal"),
    path(_('delete-meal/<slug>'), delete_meal, name="delete-meal"),
    path(_('all-recipes'), all_recipes, name="all-recipes"),
    path(_('add-recipe'), add_recipe, name="add-recipe"),
    path(_('add-recipe-to-meal/<slug>'), add_recipe_to_meal, name="add-recipe-to-meal"),
    path(_('recipe/<slug>'), recipe_detail, name="recipe-detail"),

    #comments
    path(_('add-comment/<slug>'), add_comment, name="add-comment"),

    #musics
    path(_('add-music/<slug>'), add_music, name="add-music"),

    #anecdotes
    path(_('anecdote/<slug>'), add_anecdote, name="add-anecdote"),


]