from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Noise
from .forms import NoiseForm

def home(request):
    if request.user.is_authenticated:
        form = NoiseForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                noise = form.save(commit=False)
                noise.user = request.user
                noise.save()
                messages.success(request, ("You made some Noise!"))
                return redirect('home')
            
        noises = Noise.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"noises":noises})
    else:
        noises = Noise.objects.all().order_by("-created_at")  
        return render(request, 'home.html', {"noises":noises})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles} )
        
    else:
        messages.success(request, ("You must be logged in to View Page..."))
        return redirect('home')
        
    
def profile(request,pk):
    if request.user.is_authenticated: 
        profile = Profile.objects.get(user_id=pk)
        noises = Noise.objects.filter(user_id=pk).order_by("-created_at")
        #Post form logic
        if request.method == "POST":
            #Get current user ID
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # Decide to follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # Save the profile
            current_user_profile.save() 
        return render(request, "profile.html", {"profile":profile, "noises":noises})
    else:
        messages.success(request, ("You must be logged in to View Page..."))
        return redirect('home')
        