from django.contrib.auth.models import User
from django.db import models

#Create your models here
class User(models.Model):
    username = models.CharField(max_length=50, null=False, blank=False, verbose_name="username")
    email = models.EmailField(max_length=50, null=False, blank=False, verbose_name="email")
    password = models.CharField(max_length=128, null=False, blank=False, verbose_name="password")

    class Meta:
        verbose_name= "User"
        verbose_name_plural= "Users"
        ordering= ["username"]

    def __str__(self) -> str:
        return self.username

class Flashcard(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True, null= False)
    question = models.TextField(max_length=250, null=False, blank=False)
    answer = models.TextField(max_length=250, null=False, blank=False)
    
    def __str__(self):
        return self.kanji  
