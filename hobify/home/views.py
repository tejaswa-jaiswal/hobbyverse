from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import Community
from django.contrib.auth.hashers import make_password
from . models import User, Community, Channel
# Create your views here.
global com
def index(request):
    communities= Community.objects.all()
    return render(request, "index.html", {"communities":communities})

def login_user(request):
    if request.method=="POST":
        gmail = request.POST.get("gmail")
        passw = request.POST.get("passw")
        user = authenticate(request, email=gmail, password=passw)
        
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
    return render(request, "login.html")
def register(request):
    if request.method=="POST":
        name =request.POST.get("name")
        username =request.POST.get("username")
        gmail = request.POST.get("gmail")
        passw = request.POST.get("passw")
        if User.objects.filter(email=gmail).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

        # Create and save the new user
        user = User.objects.create(
            email=gmail,
            username=username,
            password=make_password(passw),
            first_name= name,
        )
        communities= Community.objects.all()
        user = authenticate(request, email=gmail, password=passw)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful. You are now logged in.')
            return render(request, "index.html", {"communities":communities})
        return render(request, "register.html")
        
    return render(request, "register.html")
def logout_user(request):
    logout(request)  # This logs out the user
    messages.success(request, 'You have been logged out.')
    return redirect('login_user')
def intrests(request):
    if request.method == 'POST':
        interests = request.POST.getlist('interests')  
        print(interests)
    return render(request, "intrest.html")
def add_community(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        img = request.FILES.get('image')
        com = Community(category=name , community_image=img)
        com.save()

    return render(request, "new_community.html")

def community_search(request):
    communities = Community.objects.all()
    com=None
    if request.method == 'POST':
        text = request.POST.get("text")
        com = Community.objects.filter(category=text)
        if not com.exists():
            messages.error(request, "Community not found    ")
        return render(request, "index.html", {"com":com,"communities": communities})
    return render(request  , "index.html")
