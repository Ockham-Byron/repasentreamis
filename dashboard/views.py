from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from groups.models import CustomGroup

User = get_user_model

# Create your views here.
def dashboard_view(request):
  if request.user.is_authenticated:
    user=request.user
    if CustomGroup.objects.filter(members__id__contains=user.id):
      context = {'user': user}
      return render(request, 'dashboard/dashboard.html', context=context)
    else:
      return redirect('all-groups')
  
  else:
    return redirect('login')