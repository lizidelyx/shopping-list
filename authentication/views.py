from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import json

@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username', '')
        password = data.get('password', '')

        # Check if username and password are provided
        if not username or not password:
            return JsonResponse({
                'status': False,
                'message': 'Username and password are required fields.'
            }, status=400)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'status': False,
                'message': 'Username is already taken. Choose a different one.'
            }, status=400)

        # Create a new user
        user = User.objects.create_user(username=username, password=password)

        return JsonResponse({
            'status': True,
            'message': 'User registered successfully.',
            'username': user.username
        }, status=201)
    
    except Exception as e:
        return JsonResponse({
            'status': False,
            'message': f'Registration failed. Error: {str(e)}'
        }, status=500)


@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout gagal."
        }, status=401)
