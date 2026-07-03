#render shows html page while render redirects to another page
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from datetime import date

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'registration/login.html', {'form': form})

#signup view
def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error creating account. Please try again.')
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    # Retrieve tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'home.html', {'tasks': tasks, 'today': date.today()})


@login_required
def add_task(request):
    if request.method == 'POST':
        #getting the name and time from the form
        name = request.POST.get('name')
        time = request.POST.get('time')
        due_date = request.POST.get('due_date')

        #prevented the creation of tasks with empty name or time
        if name and time:
            #creating a new task for the logged-in user
            Task.objects.create(user=request.user, name=name, time=time, due_date=due_date)
    return redirect('home')
#edit task view
@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        time = request.POST.get('time')
        due_date = request.POST.get('due_date')
        if name and time and due_date:
            task.name = name
            task.time = time
            task.due_date = due_date
            task.save()
            return redirect('home')
    return render(request, 'edit_task.html', {'task': task})

#delete task view
@login_required
def delete_task(request, task_id):
    #prevents crash if task with given id does not exist or does not belong to the user
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    task.delete()
    return redirect('home')

#mark task as completed
@login_required
def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    #undo completed status if task is already completed
    task.completed = not task.completed
    task.save()
    return redirect('home')

def index(request):
    return render(request, 'index.html')


#task ai view
#importing the openai library to use the openai api for ai features
from openai import OpenAI
#lets backend send data back to frontend in json format for ai features
from django.http import JsonResponse
#allows us to exempt the ai view from csrf protection since it will be called
#  from the frontend using javascript fetch api
from django.views.decorators.csrf import csrf_exempt
#converts json(from frontend) to python dictionary(backend) and vice versa
import json

 #connects app to openai api using the api key          
client = OpenAI(api_key="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")
#defines the ai chat view which will handle the ai chat requests from the frontend
@csrf_exempt
def ai_chat(request):
    if request.method == 'POST':
        #gets the user input from the frontend and converts it to a python dictionary
        data = json.loads(request.body)
        user_message = data.get('message')

        #sends the user input to the openai api and gets the response
        # sends user message to the ai model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for managing and planningtasks."},
                #sends the actual user message to the ai model
                {"role": "user", "content": user_message}
            ]
        )

        #extracts the ai response from the openai api response
        ai_response = response.choices[0].message.content

        #sends the ai response back to the frontend in json format
        return JsonResponse({'reply': ai_response})
    
def chat_page(request):
    return render(request, 'chat.html')