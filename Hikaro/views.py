from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
import random

wins = ''


def game(request):
    global wins
    global score
    global current_round
    score = 0
    l_err = []
    flashcards = ''
    l_words = ['canario','jirafa','tiburon', 'serpiente','pulpo']
    used_indices = [] # keep track of used indices
    score = 0 # initialize the score
    current_round = 0 # initialize the rounds

    # generate the winning word
    wins = random.randint(0,len(l_words)-1)
    used_indices.append(wins)
    obj_wins = l_words[wins]
    print(obj_wins)

    # generate the incorrect words
    while len(l_err) != 3:
        num = random.randint(0,len(l_words)-1)
        if num != wins and num not in used_indices:
            l_err.append(l_words[num])
            used_indices.append(num)


    # check if the selected word matches the winning word
    if request.GET.get('selected_word') == obj_wins:
        score += 1 # increment the score
        current_round += 1
        flashcards = get_flashcards(current_round)


    return render(request, 'game.html', {
        'message': 'Nuevo mensaje desde la vista',
        'err1':l_err[0],
        'err2':l_err[1],
        'err3':l_err[2],
        'wins':obj_wins,
        'score': score,
        'flashcards': flashcards
    })


#funcion para obtener tarjeta para la ronda
def get_flashcards(round):
    # get flashcards for the current round
    flashcards = []
    # Query the database for flashcards for a specific round
    flashcards_data = Flashcard.objects.filter(round=round)
    for flashcard in flashcards_data:
        flashcards.append(Flashcard(flashcard["kanji"], flashcard["meaning"], flashcard["example"]))
    return flashcards


def login_view(request):
    if request.method == 'POST':
        username= request.POST.get('username')#diccionario
        password= request.POST.get('password')

        print(username)
        print(password)

        user= authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            print("Usuario autenticado")
            return redirect('game')    

        else:
            #print("Usuario no autenticado") donde saldrian a reflejar estas dos lineas?
            #return HttpResponse('TE HA MORDIDO UN ZOMBIE')
            messages.success(request, 'Usuario o contraseña no validos')

    return render(request, 'login.html', {

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Session closed successfully')
    return redirect(reverse('login'))

def register(request):
        form= RegisterForm(request.POST or None)
        
        if request.method == 'POST' and form.is_valid():
            username = form.cleaned_data.get('username') #Diccionario
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')


            print(username)            
            print(email)
            print(password)
   

            user= User.objects.create_user(username, email, password) 
            if user:
                login(request, user)
                messages.success(request, 'Usuario creado con éxito')
                return redirect('login')
   
        else:
            form=RegisterForm()
        return render(request, 'register.html', {
            'form': form
        })

def forgot(request):
    return render(request, 'forgot.html', {
        'message': 'Nuevo mensaje desde la vista'
    })

def study(request):
    return render(request, 'study.html', {
        'message': 'Nuevo mensaje desde la vista'
    })

def upload(request):
    return render(request, 'upload.html', {
        'message': 'Nuevo mensaje desde la vista'
    })

def register2(request):
    pass