import hashlib
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import Account
from django.contrib.auth.hashers import make_password,check_password
from django.urls import reverse

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if Account.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            
            hashed_password = make_password(password)
            
            Account.objects.create(username=username, password=hashed_password)

            return JsonResponse({"message": "User registered successfully!"})
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return render(request, "user/register.html")

@csrf_exempt  # 🔹 Disable CSRF from django.contrib.auth.hashers import check_password
def login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = Account.objects.filter(username=username).first()
            if user and check_password(password,user.password):  # 🔹 Verify hashed password
                request.session["username"] = user.username  # Store username in session
                return JsonResponse({"message": "Login successful"})
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return render(request, "user/login.html")

@csrf_exempt  # Disable CSRF for now (optional, but recommended to use CSRF token)
def logout(request):
    if request.method == "POST":
        request.session.flush()
        return redirect(reverse('menu:index'))
    return redirect(reverse('menu:index'))

def get_user_info(request):
    username = request.session.get("username")
    if username:
        return JsonResponse({"username": username})
    return JsonResponse({"error": "Not logged in"}, status=400)
