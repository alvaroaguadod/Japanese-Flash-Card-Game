# 'models.py' contains the flashcard model and the logic to interact with the database

from sqlalchemy import Column, Integer, String


class Flashcard(Base):
    __tablename__ = 'flashcards'
    id = Column(Integer, primary_key= True)
    japanese = Column(String)
    english = Column(String)

