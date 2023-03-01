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
    japanese_sentence = models.CharField(max_length=200)
    english_meaning = models.CharField(max_length=200)
    image = models.ImageField(upload_to='storedImages', null=True, blank=True)

    def __str__(self):
        return f"{self.japanese_sentence} - {self.english_meaning} ({self.image.url if self.image else 'No image'})"