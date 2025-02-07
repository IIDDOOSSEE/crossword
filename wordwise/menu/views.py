from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    return render(request,"menu/index.html")

# def get_user_info(request):
#     username = request.session.get("username")
#     if username:
#         return JsonResponse({"username": username})
#     return JsonResponse({"error": "Not logged in"}, status=400)