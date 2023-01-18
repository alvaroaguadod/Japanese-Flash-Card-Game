# The 'app.py' file is where the main logic of the game is defined, such as the routes, views, and functions.
# This is also where you import the Flask application instance created in '__init__.py' and configurates
# the game's routes, views and the logic of the flashcard game.

from flask import render_template, request
import random
from mygame import create_app
from models import Flashcard

app = create_app()


@app.route('/')
def index():
    #Select a random flashcard
    flashcards = app.session.query(Flashcard).all()
    flashcard = random.choice(flashcards)
    return render_template('index.html', flashcard=flashcard)

@app.route('/check', methods= ['POST'])
def check():
    #Get the user's guess
    guess = request.form['guess'] 
    #Compare the guess to the correct translation
    if guess == flashcards['english']:
        correct_flashcards.append(flashcard) #I have to create the orrect_flashcards list 
        flashcards.remove(flashcard)
        message= "Correct!"
    else:
        message= "Incorrect. Try again."
    return render_template('index.html', flashcard = flashcard, message= message)

@app.teardown_request
def teardown_request(exception):
    app.session.close()

if __name__== '__main__':
    app.run()