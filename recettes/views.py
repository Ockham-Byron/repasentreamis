from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

    
def get_groups(user):
    groups = CustomGroup.objects.filter(members__id__contains=user.id)
    nb_of_groups = len(groups)
    if nb_of_groups == 0:
        group = None
    elif nb_of_groups >= 1:
        group = groups
        

    return group

# Create your views here.
@login_required
def add_recipe(request):
    group = get_groups(request.user)
    if group is None:
        return redirect('all-groups')
    else:
        form=AddRecipeForm(group)

        if request.method == "POST":
            form=AddRecipeForm(group, request.POST, request.FILES)
            if form.is_valid():
                recipe=form.save()
                recipe.save()
                return redirect('all-recipes')

        return render(request, "recettes/add-recipe.html", {'form':form})


    
@login_required
def all_recipes(request):
    groups = get_groups(request.user)
    if groups is None:
        return redirect('all-groups')
    else:
        for group in groups:
            recipes = Recipe.objects.filter(group=group)

        context={
            'recipes':recipes
        }
        return render(request, "recettes/all-recipes.html", context=context)

@login_required
def recipe_detail(request, slug):
    recipe=get_object_or_404(Recipe, slug=slug)

    context={
        'recipe':recipe,
    }
    
    return render(request, "recettes/recipe-detail.html", context=context)

@login_required
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
    form=AddMenuForm(request.user)
    group = get_groups(request.user)
    is_group = False
    if len(group) == 1:
                is_group = True
    if group is None:
        return redirect('all-groups')
    
    else:
        
        if request.method == "POST":
            form=AddMenuForm(request.user, request.POST, request.FILES)
            if len(group) == 1:
                group = CustomGroup.objects.get(uuid=group[0].uuid)
                is_group = True
            else:
                group = request.POST.get('group')
                group = CustomGroup.objects.get(uuid=group)
                
            if form.is_valid() or group is not None:
                eaten_at = request.POST.get('eaten_at')
                picture = request.POST.get('picture')
                recipes = request.POST.get('recipes')
                print(recipes)
                
                menu = Menu(eaten_at=eaten_at,picture=picture, group=group)
                menu.save()
                    

                if 'add-recipe' in request.POST:
                    return redirect('add-recipe-to-menu', menu.slug)
                if 'create-menu' in request.POST:
                    return redirect('all-menus')
            
            else:
                print(form.errors.as_data())
                

        return render(request, "recettes/add-menu.html", {'form':form, 'is_group':is_group})

@login_required
def add_menu_from_group(request, slug):
    form=AddMenuForm(request.user)
    group = CustomGroup.objects.get(slug=slug)
    is_group = True

    if request.method == "POST":
        form=AddMenuForm(request.user, request.POST, request.FILES)
        print(group)
        if form.is_valid() or is_group :
            eaten_at = request.POST.get('eaten_at')
            picture = request.POST.get('picture')
            recipes = request.POST.get('recipes')
            if recipes is not None:
                menu = Menu(eaten_at=eaten_at,picture=picture,recipes=recipes.set(), group=group)
            else:
                menu = Menu(eaten_at=eaten_at,picture=picture, group=group)
            menu.save()
            if 'add-recipe' in request.POST:
                return redirect('add-recipe-to-menu', menu.slug)
            if 'create-menu' in request.POST:
                return redirect('all-menus')
            
        else:
            print(form.errors)

    return render(request, "recettes/add-menu.html", {'form':form, 'is_group':is_group})

@login_required
def add_recipe_to_menu(request, slug):
    menu = get_object_or_404(Menu, slug=slug)
    group = menu.group
    
    form=AddRecipeForm(group)

    

    if request.method == "POST":
        form=AddRecipeForm(group, request.POST, request.FILES)
        chef = request.POST.get("chef")
        print(chef)
        if form.is_valid():
            recipe=form.save(commit=False)
            recipe.group=group
            recipe.save()
            menu.recipes.add(recipe)
            menu.save()
            return redirect('all-menus')

    return render(request, "recettes/add-recipe.html", {'form':form})

@login_required
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

@login_required
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
    group = get_groups(request.user)
    if group is None: 
        return redirect('all-groups')
    else:
        groups = CustomGroup.objects.filter(members__id__contains=request.user.id)
        for group in groups:
            menus = Menu.objects.filter(group__members__id__contains = request.user.id).distinct()
    
    


        context={
            'menus':menus,
            'groups':groups,
        }

        return render(request, "recettes/all-menus.html", context=context )