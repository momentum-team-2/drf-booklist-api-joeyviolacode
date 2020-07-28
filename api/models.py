from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    show_timeline = models.BooleanField(default=True)


class Author(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if self.first_name:
            return f'{self.last_name}, {self.first_name}'
        return f'{self.last_name}'


class Book(models.Model):
    STATUS = [ ("to-read" , "to-read"), ("reading", "reading"), ("read", "read") ]

    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books", blank=True)
    status = models.CharField(choices=STATUS, max_length=25, default="to read")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f'{self.title}'


class Note(models.Model):
    note = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes")
    page = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")
    public = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Note on {self.book}, page {self.page}'