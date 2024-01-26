from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

def is_unique_group(user):
    groups = CustomGroup.objects.filter(members__id__contains=user.id)
    nb_of_groups = len(groups)
    if nb_of_groups == 1:
        return True
    else:
        return False

# Create your views here.
def add_recipe(request):
    form=AddRecipeForm()

    if request.method == "POST":
        form=AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe=form.save()
            recipe.save()
            return redirect('all-recipes')

    return render(request, "recettes/add-recipe.html", {'form':form})


    

def all_recipes(request):
    recipes = get_list_or_404(Recipe)

    context={
        'recipes':recipes
    }
    return render(request, "recettes/all-recipes.html", context=context)

def recipe_detail(request, slug):
    recipe=get_object_or_404(Recipe, slug=slug)

    context={
        'recipe':recipe,
    }
    
    return render(request, "recettes/recipe-detail.html", context=context)

def add_comment(request, slug):
    recipe=get_object_or_404(Recipe, slug=slug)
    form=AddCommentForm()

    if request.method=='POST':
        form=AddCommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.recipe=recipe
            comment.author=request.user
            comment.save()
            return redirect('recipe-detail', recipe.slug)

    return render(request, "recettes/add-comment.html", {'form':form})

@login_required
def add_menu(request):
    form=AddMenuForm()
    if is_unique_group(request.user):
        group = CustomGroup.objects.get(members__id__contains=request.user.id)
    if request.method == "POST":
        form=AddMenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu=form.save(commit=False)
            menu.group=group
            menu.save()
            if 'add-recipe' in request.POST:
                return redirect('add-recipe-to-menu', menu.slug)
            if 'create-menu' in request.POST:
                return redirect('all-menus')

    return render(request, "recettes/add-menu.html", {'form':form})

def add_recipe_to_menu(request, slug):
    menu = get_object_or_404(Menu, slug=slug)

    form=AddRecipeForm()

    if request.method == "POST":
        form=AddRecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe=form.save()
            recipe.save()
            menu.recipes.add(recipe)
            menu.save()
            return redirect('all-menus')

    return render(request, "recettes/add-recipe.html", {'form':form})

def add_music(request, slug):
    menu=get_object_or_404(Menu, slug=slug)
    form=AddMusicForm()
    if request.method =='POST':
        form=AddMusicForm(request.POST)
        if form.is_valid():
            music=form.save()
            music.menu.add(menu)
            music.save()
            return redirect('all-menus')

    return render(request, 'recettes/add-music.html', {'form':form})

def add_anecdote(request, slug):
    menu=get_object_or_404(Menu, slug=slug)
    form=AddAnecdoteForm()
    if request.method =='POST':
        form=AddAnecdoteForm(request.POST)
        if form.is_valid():
            anecdote=form.save()
            anecdote.menu.add(menu)
            anecdote.save()
            return redirect('all-menus')

    return render(request, 'recettes/add-anecdote.html', {'form':form})

@login_required
def all_menus(request):
    groups = CustomGroup.objects.filter(members__id__contains=request.user.id)
    nb_of_groups = len(groups)
    group = None
    if nb_of_groups == 1:
        group = CustomGroup.objects.get(members__id__contains=request.user.id)
    
    menus = Menu.objects.filter(group__members__id__contains = request.user.id).distinct()

    context={
        'menus':menus,
        'nb_of_groups':nb_of_groups,
        'groups':groups,
        'group':group,
    }

    return render(request, "recettes/all-menus.html", context=context )