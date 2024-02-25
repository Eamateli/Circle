from profile import Profile
from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, 'profile_list.html', {"profiles":profiles} )
    
