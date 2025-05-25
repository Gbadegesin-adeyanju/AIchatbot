from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Chat

from django.utils import timezone
from .utils import ask_gemini
import re
from django.utils.safestring import mark_safe


@login_required
def index(request):
    chats = Chat.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_gemini(message) # called the function from utils.py to send message to Gemini and return response 
        response = mark_safe(re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', response))

        # Replace * text with <li>text</li> and wrap in <ul>
        response_lines = response.splitlines()  # Split by new lines
        bullet_list = [line.strip() for line in response_lines if line.strip().startswith('*')]
        if bullet_list:  # If there are any bullet points
            response = '<ul>' + ''.join(f'<li>{line[1:].strip()}</li>' for line in bullet_list) + '</ul>'


        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot/index.html', {'chats': chats})

def signup(request):
    # clean data
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # confirm if password1 and password2 match before saving user data and authenticate user
        if password1 == password2:
            user = User.objects.create_user(username, email, password1)
            user.save()
            auth.login(request, user)
            return render(request, 'chatbot/index.html')
        else:
            error_message = 'Password does not match'
            return render(request, 'chatbot/signup.html', {'error_message': error_message})
    return render(request, 'chatbot/signup.html')

def logout_view(request):
    logout(request) #logout user
    return render(request, 'chatbot/logged_out.html')



