from django.db import models
import uuid

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
    japanese_sentence = models.CharField(max_length=200,default=None)
    english_meaning = models.CharField(max_length=200, default=None)
    image = models.ImageField(upload_to='./storedImages', null=True, blank=True, default= './storedImages/default.png', verbose_name='picture')
    particle = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return f"{self.japanese_sentence} - {self.english_meaning} ({self.image.url if self.image else 'No image'})"
    
class Match(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, null=False, blank=False, verbose_name="username")
    score = models.IntegerField(default=0)
    current_round = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self._get_user_id_from_session()
        super().save(*args, **kwargs)

    def _get_user_id_from_session(self):
        # Retrieve the value of the 'user_id' session variable
        return getattr(self._meta.model, 'user_id', None)