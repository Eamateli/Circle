from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Noise
from .forms import NoiseForm, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


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
        
 
def unfollow(request, pk):
    if request.user.is_authenticated:
        # Get profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow user
        request.user.profile.follows.remove(profile)
        # Save our profile
        request.user.profile.save()
        messages.success(request, (f"You have successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
             
    else:
        messages.success(request, ("You must be logged in to View Page..."))
        return redirect('home')
    
    
def follow(request, pk):
    if request.user.is_authenticated:
        # Get profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # Unfollow user
        request.user.profile.follows.add(profile)
        # Save our profile
        request.user.profile.save()
        messages.success(request, (f"You have successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
             
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
    
    
    
def followers(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles":profiles} )
        else:
            messages.success(request, ("That's not your profile page..."))
            return redirect('home')
            
        
    else:
        messages.success(request, ("You must be logged in to View Page..."))
        return redirect('home')
    

def follows(request,pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles":profiles} )
        else:
            messages.success(request, ("That's not your profile page..."))
            return redirect('home')
            
        
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
 
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered ! Noisemaker... "))  
            return redirect('home')
    return render(request, "register.html", {'form':form})
    
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		profile_user = Profile.objects.get(user__id=request.user.id)
		# Get Forms
		user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
		profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			login(request, current_user)
			messages.success(request, ("Your Profile Has Been Updated!"))
			return redirect('home')

		return render(request, "update_user.html", {'user_form':user_form, 'profile_form':profile_form})
	else:
		messages.success(request, ("You Must Be Logged In To View That Page..."))
		return redirect('home')  


def noise_like(request, pk):
    if request.user.is_authenticated:
       noise = get_object_or_404(Noise,id=pk)
       if noise.likes.filter(id=request.user.id):
           noise.likes.remove(request.user)
       else:
           noise.likes.add(request.user)
    #    return redirect('home')    
       return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You Must Be Logged In To View That Page..."))
        return redirect('home') 
    
    
def noise_show(request, pk):
    noise = get_object_or_404(Noise,id=pk)
    if noise:
        return render(request, "show_noise.html", {'noise':noise})     
    else:
        messages.success(request, ("That Noise does not exist..."))
        return redirect('home') 
        
def delete_noise(request, pk):
    if request.user.is_authenticated:
       noise = get_object_or_404(Noise,id=pk)
       # Check to see if you own the noise
       if request.user.username == noise.user.username:
           noise.delete()
           messages.success(request, ("Your Noise has been Deleted!"))
           return redirect(request.META.get("HTTP_REFERER"))
       else:
           messages.success(request, ("You don't own that Noise..."))
           return redirect('home')             
    else:
        messages.success(request, ("Please Log In to continue..."))
        return redirect(request.META.get("HTTP_REFERER"))
        
def edit_noise(request, pk):
    if request.user.is_authenticated:
       noise = get_object_or_404(Noise,id=pk)
       if request.user.username == noise.user.username:
           form = NoiseForm(request.POST or None, instance=noise)
           if request.method == "POST":
                    if form.is_valid():
                        noise = form.save(commit=False)
                        noise.user = request.user
                        noise.save()
                        messages.success(request, ("Your Noise has been updated!"))
                        return redirect('home')

                    return render(request, "edit_noise.html", {'form':form , 'noise':noise})
           else:
               return render(request, "edit_noise.html", {'form':form , 'noise':noise})

       else:
           messages.success(request, ("You don't own that Noise..."))
           return redirect('home')             
    else:
        messages.success(request, ("Please Log In to continue..."))
        return redirect('home')
    
def search(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # search the DB
        searched = Noise.objects.filter(body__contains= search)
        return render(request, 'search.html', {'search':search, 'searched':searched})
    
    else:
        return render(request, 'search.html', {})
    
def search_user(request):
    if request.method == "POST":
        # Grab the form field input
        search = request.POST['search']
        # search the DB
        searched = User.objects.filter(username__contains= search)
        return render(request, 'search_user.html', {'search':search, 'searched':searched})
    
    else:
        return render(request, 'search_user.html', {})
    
        
        
    
        
        


    
        
        
        
        
