from django.urls import path
from django.utils.translation import gettext as _
from .views import *



urlpatterns = [
    path(_('all-meals'), all_meals, name="all-meals"),
    path(_('add-meal'), add_meal, name="add-meal"),
    path(_('add-meal/<slug>'), add_meal_from_group, name="add-meal-from-group"),
    path(_('edit-meal/<slug>'), edit_meal, name="edit-meal"),
    path(_('delete-meal/<slug>'), delete_meal, name="delete-meal"),
    path(_('all-dishes'), all_dishes, name="all-dishes"),
    path(_('add-dish'), add_dish, name="add-dish"),
    path(_('add-dish-to-meal/<slug>'), add_dish_to_meal, name="add-dish-to-meal"),
    path(_('edit-dish/<slug>'), edit_dish, name="edit-dish"),
    path(_('delete-dish/<slug>'), delete_dish, name="delete-dish"),
    path(_('add-existing-dish/<slug>'), add_existing_dish_to_meal, name="add-existing-dish"),
    path(_('dish/<slug>'), dish_detail, name="dish-detail"),

    #comments
    path(_('add-comment/<slug>'), add_comment, name="add-comment"),
    path(_('edit-comment/<id>'), edit_comment, name="edit-comment"),
    path(_('delete-comment/<id>'), delete_comment, name="delete-comment"),

    #musics
    path(_('add-music/<slug>'), add_music, name="add-music"),

    #anecdotes
    path(_('anecdote/<slug>'), add_anecdote, name="add-anecdote"),


]