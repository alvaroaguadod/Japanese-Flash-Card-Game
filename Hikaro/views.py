from .models import Flashcard, User, Match
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User as User_django
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
import json, os
from django.contrib import messages
from .forms import NewUserForm
import random, uuid



#Function that increments the score when the user chooses the correct option.
def game(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            match = Match.objects.get(user_id=user_id)
            user = match.user_id
        except Match.DoesNotExist:
            # create a new user with the given id
            match = Match.objects.create(user_id=user_id, username="Anonymous")
            user = match.user_id

        # retrieve score and round from the Match model for the current user
        try:
            score = match.score
            current_round = match.current_round
        except Match.DoesNotExist:
            # create a new Match object for the current user
            match = Match(user_id=user_id, username=user.username, score=0, current_round=0)
            score = 0
            current_round = 0


        l_err = []
        flashcards = ''
        l_words = ['は','が','を','も','に','へ', 'で', 'から', 'まで', 'と', 'や', 'の', 'ね', 'よ', 'none']
        used_indices = [] # keep track of used indices

        # generate the winning word
        wins = random.randint(0,len(l_words)-1)
        print(wins)
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
            current_round += 1 # increment the round  

        # update the score and round in the Match model for the current user
        match.score = score
        match.current_round = current_round
        match.save()

        # retrieve flashcards from database
        flashcards = Flashcard.objects.all()
        flashcards_data = []
        for flashcard in flashcards:
            flashcards_data.append({
                'japanese_sentence': flashcard.japanese_sentence,
                'particle': flashcard.particle,
                'english_meaning': flashcard.english_meaning,
                'image_name': flashcard.image
            })

        return render(request, 'game.html', {
            'message': 'New message from the view',
            'err1':l_err[0],
            'err2':l_err[1],
            'err3':l_err[2],
            'wins':obj_wins,
            'score': score,
            'current_round': current_round,
            'flashcards': flashcards
        })
        
#Function that reads the sentences from the JSON file and separates particle from sentences   (esta llega a funcionar?)
"""
def my_view(request):
    with open('sentences.json', 'r', encoding='utf-8') as f:
        sentences = json.load(f)
    
    sentence = sentences[0]['sentence']
    particle = sentences[0]['particle']
    
    context = {
        'sentence': sentence,
        'particle': particle,
    }
    
    return render(request, 'my_template.html', context)
"""

#Function to obtain card for the round.
"""
def get_flashcards(round):
    # Load flashcards from the JSON file
    with open('data.json') as f:
        flashcards_data = json.load(f)

    # Get flashcards for the current round
    flashcards = []
    # Query the database for flashcards for a specific round
    flashcards_data = Flashcard.objects.filter(round=round)
    for flashcard in flashcards_data:
        if flashcard['round'] == round:
            flashcards.append(Flashcard(flashcard["image"], flashcard["japanese"], flashcard["english"]))
    return flashcards
"""

#Pass the flashcards data to the template context 
def game_view(request):
    # Render the game.html template with the flashcards data
    return render(request, 'game.html', {'flashcard': Flashcard.objects.all(),
                                         'num_flashcard': Flashcard.objects.count()})


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

            # create a new session and store user data
            user_id = uuid.uuid4().int #normalmente es aconsejable que sea str
            request.session = SessionStore()
            request.session['user_id'] = user_id
            request.session.save()

            return redirect('game')    

        else:
            messages.success(request, 'Usuario o contraseña no validos')

    return render(request, 'index.html', {

    })

def logout_view(request):
    logout(request)
    messages.success(request, 'Session closed successfully')
    return redirect(reverse('login'))

def register(request):

    print('register')  
    if request.method == 'POST':
        print('metodo post')
        print(request.POST)
        form = NewUserForm(request.POST)
        print(form)
        if form.is_valid():
            print('Es valido')
            username = form.cleaned_data.get('username') #Diccionario
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

# Check password validity:
            if password == password2:
                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'User already exists')
                    return redirect('register')

                # Check if email already exists
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('register')

                else:
                #Create user
                    #user= User.objects.create_user(username=username, email=email, password=password)
                    user = User()
                    user.email = email
                    user.username = username
                    user.password = password
                    user.save()
                    user2 = User_django.objects.create_user(username,email,password)
                    user2.save()
                    messages.success(request, 'User successfully created')
                    login_url = reverse('login')
                    return redirect(login_url) 
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('register')

        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return redirect('register')
    else:
        form = NewUserForm()

        return render(request, 'register.html', {
            'form': form
        })

def forgot(request):
    return render(request, 'forgot.html', {
        'message': 'New message from the view'
    })


#removing CSRF protection can leave your site vulnerable to CSRF attacks, I decided to use it as there is no vulnerable information on this project
@csrf_exempt
def get_user(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email)
            data = {
                'email': user.email,
                'password': user.password,
            }
            return JsonResponse(data)
        except User.DoesNotExist:
            error = {'error': 'Sorry, the email you entered was not found in our database.'}
            return JsonResponse(error)
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        user = User.objects.get(email=email)
        user.password = new_password
        user.save()
        data = {'message': 'Password updated successfully!'}
        return JsonResponse(data)

def study(request):
    return render(request, 'study.html', {
        'message': 'New message from the view'
    })

def upload(request):
    if request.method == 'POST':
        # Get the user input from the POST request
        japanese_sentence = request.POST.get('japanese_sentence')
        english_meaning = request.POST.get('english_meaning')
        image_file = request.FILES.get('image_file')
        particle = request.POST.get('particle')

        print(japanese_sentence)
        print(english_meaning)
        print(image_file)
        print(particle)

        
        # Make sure all required fields are provided
        if not (japanese_sentence and english_meaning and image_file):
            return HttpResponseBadRequest('Missing required fields')
        
        # Save image file
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(BASE_DIR, './storedImages', image_file.name)
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Read existing JSON data from file
        with open('./static/json/data.json', 'r') as f:
            existing_data = json.load(f)

        # Create new flashcard object from user inputs
        new_flashcard = {
            'japanese': japanese_sentence,
            'english': english_meaning,
            'image': image_path,
            'particle': particle
        }
        
        #Create flashcard
        flashcard = Flashcard(
            japanese=new_flashcard['japanese'],
            english=new_flashcard['english'],
            image=new_flashcard['image'],
            particle=new_flashcard['particle']
        )
        flashcard.save()

        # Append new flashcard object to existing data
        existing_data['flashcards'].append(new_flashcard)

        print(existing_data['flashcards'])

        # Write combined data to file
        with open('./static/json/data.json', 'w') as f:
            json.dump(existing_data, f)
            f.close()

        #If POST request is successful, the JSON response will be shown before the upload.html template.
        json_response = JsonResponse({'success': True})
        html_response = render(request, 'upload.html')
        combined_response = HttpResponse(json_response.content + html_response.content)
        combined_response['content-type'] = 'text/html'
        return combined_response

    else:
        return render(request,'upload.html')

def home(request):
    return render(request, 'home.html', {
    'message': 'New message from the view'
})

def recover_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # If the user doesn't exist, show an error message
            error_message = "We couldn't find an account with that email address. Please try again."
            return render(request, 'recover_password.html', {'error_message': error_message})

        if request.POST.get('new_password'):
            # If the user has submitted a new password, update their password in the database
            new_password = request.POST['new_password']
            user.set_password(new_password)
            user.save()
            success_message = "Your password has been updated."
            return render(request, 'recover_password.html', {'success_message': success_message})

        # If the user exists, show their email address and a form to update their password
        return render(request, 'recover_password.html', {'email': email})

    return render(request, 'recover_password.html')