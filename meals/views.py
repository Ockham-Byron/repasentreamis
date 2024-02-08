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
def add_dish(request):
    groups = get_groups(request.user)
    is_group = False
    no_meal = True
    if len(groups) == 1:
        is_group = True
        group = groups[0]
    if groups is None:
        return redirect('all-groups')
    
    if is_group:
        print("group unique")
        form = AddDishForm(group)
        if request.method == "POST":
            form=AddDishForm(group, request.POST, request.FILES)
            chefs = request.POST.getlist('chef')
            meal = request.POST.get('meal')
            meal = Meal.objects.get(id=meal)
            if form.is_valid():
                dish=form.save(commit=False)
                dish.group = group
                dish.save()
                if chefs:
                    for chef in chefs:
                        user = User.objects.get(id=chef)
                        dish.chef.add(user)
                dish.save()
                meal.dishes.add(dish)
                meal.save()
                
                return redirect('all-dishes')

        return render(request, "meals/add-dish.html", {'form':form, 'is_group':is_group, 'groups':groups, 'group':group, 'no_meal':no_meal})


    
@login_required
def all_dishes(request):
    groups = get_groups(request.user)
    if groups is None:
        return redirect('all-groups')
    else:
        for group in groups:
            dishes = Dish.objects.filter(group=group)

        context={
            'dishes':dishes
        }
        return render(request, "meals/all-dishes.html", context=context)

@login_required
def dish_detail(request, slug):
    dish=get_object_or_404(Dish, slug=slug)

    context={
        'dish':dish,
    }
    
    return render(request, "meals/dish-detail.html", context=context)

@login_required
def add_comment(request, slug):
    dish=get_object_or_404(Dish, slug=slug)
    form=AddCommentForm()

    if request.method=='POST':
        form=AddCommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.dish=dish
            comment.author=request.user
            comment.save()
            return redirect('dish-detail', dish.slug)

    return render(request, "meals/add-comment.html", {'form':form})

@login_required
def add_meal(request):
    form=AddMealForm(request.user)
    group = get_groups(request.user)
    is_group = False
    if len(group) == 1:
                is_group = True
    if group is None:
        return redirect('all-groups')
    
    else:
        
        if request.method == "POST":
            form=AddMealForm(request.user, request.POST, request.FILES)
            if len(group) == 1:
                group = CustomGroup.objects.get(uuid=group[0].uuid)
                is_group = True
            else:
                group = request.POST.get('group')
                group = CustomGroup.objects.get(uuid=group)

            if form.is_valid() or group is not None:
                eaten_at = request.POST.get('eaten_at')
                picture = request.FILES.get('picture')
                dishes = request.POST.getlist('dishes')
                
                
                meal = Meal(eaten_at=eaten_at,picture=picture, group=group)
                meal.save()
                if dishes:
                    for i in dishes:
                        dish = Dish.objects.get(id=i)
                        meal.dishes.add(dish)
                    meal.save()
                    

                if 'add-dish' in request.POST:
                    return redirect('add-dish-to-meal', meal.slug)
                if 'create-meal' in request.POST:
                    return redirect('all-meals')
            
            else:
                print(form.errors.as_data())
                

        return render(request, "meals/add-meal.html", {'form':form, 'is_group':is_group})

@login_required
def add_meal_from_group(request, slug):
    form=AddMealForm(request.user)
    group = CustomGroup.objects.get(slug=slug)
    is_group = True

    if request.method == "POST":
        form=AddMealForm(request.user, request.POST, request.FILES)
        print(group)
        if form.is_valid() or is_group :
            eaten_at = request.POST.get('eaten_at')
            picture = request.FILES.get('picture')
            dishes = request.POST.get('dishes')
            if dishes is not None:
                meal = Meal(eaten_at=eaten_at,picture=picture,dishes=dishes.set(), group=group)
            else:
                meal = Meal(eaten_at=eaten_at,picture=picture, group=group)
            meal.save()
            if 'add-dish' in request.POST:
                return redirect('add-dish-to-meal', meal.slug)
            if 'create-meal' in request.POST:
                return redirect('all-meals')
            
        else:
            print(form.errors)

    return render(request, "meals/add-meal.html", {'form':form, 'is_group':is_group})

@login_required
def edit_meal(request, slug):
    meal = get_object_or_404(Meal, slug=slug)
    form = AddMealForm(request.user, instance = meal)
    is_group = True
    group = meal.group

    if request.method == 'POST':
        form = AddMealForm(request.user, request.POST, request.FILES, instance=meal)
        if form.is_valid() or is_group:
                eaten_at = request.POST.get('eaten_at')
                picture = request.FILES.get('picture')
                dishes = request.POST.getlist('dishes')
                
                # meal.dishes.through.objects.all().delete()
                
                meal.eaten_at = eaten_at
                meal.picture = picture
                meal.group = group
                meal.save()
                if dishes:
                    for i in dishes:
                        dish = Dish.objects.get(id=i)
                        if dish not in meal.dishes.all():
                            meal.dishes.add(dish)
                    meal.save()
                    

                if 'add-dish' in request.POST:
                    return redirect('add-dish-to-meal', meal.slug)
                if 'create-meal' in request.POST:
                    return redirect('all-meals')
            
        else:
            print(form.errors)
     

    return render(request, 'meals/add-meal.html', {'form': form, 'meal': meal, 'is_group': is_group})

@login_required
def delete_meal(request, slug):
    meal = get_object_or_404(Meal, slug=slug)
    os.remove(meal.picture.path)
    meal.picture.delete()
    meal.delete()
    return redirect('all-meals')

@login_required
def add_dish_to_meal(request, slug):
    meal = get_object_or_404(Meal, slug=slug)
    group = meal.group
    is_group = True
    
    form=AddDishForm(group)

    if request.method == "POST":
        form=AddDishForm(group, request.POST, request.FILES)
        chefs = request.POST.getlist('chef')
        print(chefs)
        if form.is_valid():
            dish=form.save(commit=False)
            dish.group=group
            dish.save()
            if chefs:
                for chef in chefs:
                    user = User.objects.get(id=chef)
                    dish.chef.add(user)
            dish.save()
            meal.dishes.add(dish)
            meal.save()
            return redirect('all-meals')
        
    else:
        print("Nothing")

    return render(request, "meals/add-dish.html", {'form':form, 'is_group':is_group, 'meal':meal})

@login_required
def add_existing_dish_to_meal(request, slug):
    meal = get_object_or_404(Meal, slug=slug)
    
    
    dishes = Dish.objects.filter(group= meal.group)
    print(dishes)

    if request.method == "POST":
        if 'create-dish' in request.POST:
            return redirect('add-dish-to-meal', meal.slug)
        if 'add-dish' in request.POST:
            dish=request.POST.get('dish')
            print(dish)
            meal.dishes.add(dish)
            meal.save()
            return redirect('all-meals')
        
    else:
        print("Nothing")

    return render(request, "meals/add-existing-dish.html", {'meal':meal, 'dishes':dishes})

@login_required
def add_music(request, slug):
    meal=get_object_or_404(Meal, slug=slug)
    form=AddMusicForm()
    if request.method =='POST':
        form=AddMusicForm(request.POST)
        if form.is_valid():
            music=form.save()
            music.meal.add(meal)
            music.save()
            return redirect('all-meals')

    return render(request, 'meals/add-music.html', {'form':form})

@login_required
def add_anecdote(request, slug):
    meal=get_object_or_404(Meal, slug=slug)
    form=AddAnecdoteForm()
    if request.method =='POST':
        form=AddAnecdoteForm(request.POST)
        if form.is_valid():
            anecdote=form.save()
            anecdote.meal.add(meal)
            anecdote.save()
            return redirect('all-meals')

    return render(request, 'meals/add-anecdote.html', {'form':form})

@login_required
def all_meals(request):
    group = get_groups(request.user)
    if group is None: 
        return redirect('all-groups')
    else:
        groups = CustomGroup.objects.filter(members__id__contains=request.user.id)
        for group in groups:
            meals = Meal.objects.filter(group__members__id__contains = request.user.id).distinct()
    
    


        context={
            'meals':meals,
            'groups':groups,
        }

        return render(request, "meals/all-meals.html", context=context )
    
