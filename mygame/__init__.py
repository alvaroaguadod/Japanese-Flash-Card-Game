# '__init__.py' file is used to create the Flask application instance and configure it. It also imports 
# other modules and blueprints that are part of the package. It could include code to create SQLAlchemy 
# session, import the flashcard model and set up any other package-level configurations.

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists
from config import Config
from .models import Base, Flashcard

Base = declarative_base()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    #Create a connection to the database
    engine = create_engine("sqlite:///flashcards.db")
    Base.metadata.bind = engine

    #Check if the database already exists, and create it if it doesn't
    if not database_exists(engine.url):
        Base.metadata.create_all(engine)

    #Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    #Add a session to interact with the database
    app.session = session

    return app

#Create a list of flashcards
flashcards = [
    {'japanese': '日本', 'english': 'Japan'},
    {'japanese': '人', 'english': 'Person'},
    {'japanese': '国', 'english': 'Country'},
    {'japanese': '大学', 'english': 'University'},
    {'japanese': '今', 'english': 'Now'},
    {'japanese': '前', 'english': 'Before'},
    {'japanese': '大学', 'english': 'University'},
    {'japanese': '駅', 'english': 'Train Station'},    
#Add more flashcards here
]



