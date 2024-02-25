from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    return render(request, 'profile_list.html')
    
