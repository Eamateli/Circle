from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Noise
from .forms import NoiseForm
from django.contrib.auth import authenticate, login, logout

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
        return render(request, 'home.html', {"noises":noises, "form":form})
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
    
    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been Logged In! Make some Noise!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error loggin in. Please Try Again..."))
            return redirect('login')     
    else:
        return render(request, "login.html", {})
    

def logout_user(request):
     logout(request)
     messages.success(request, ("You have been Logged Out. Noise back soon..."))
     return redirect('home')
     