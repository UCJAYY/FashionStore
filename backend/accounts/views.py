from django.shortcuts import render

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.conf import settings
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth import login, logout, authenticate

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('my_recommendations')
        else:
            # Temporary debug output
            print("Form errors:", form.errors.as_json())
    else:
        form = CustomUserCreationForm()
    
    return render(request, "signup.html", {"form": form})




# accounts/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings  # To access LOGIN_REDIRECT_URL

def login_view(request):
    # If the user is already authenticated, redirect immediately.
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    
    if request.method == "POST":
        # Retrieve email (from the "username" field) and password from POST data.
        email = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            messages.error(request, "Invalid email or password. Please try again.")
    
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('itemsdisplay')