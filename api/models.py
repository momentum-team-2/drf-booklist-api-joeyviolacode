from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    pass


class Author(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        if first_name:
            return f'{last_name}, {first_name}'
        return f'{last_name}'


class Book(models.Model):
    STATUS = [ (1 , "to read"), (2, "reading"), (3, "read") ]

    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name="books", blank=True)
    status = models.CharField(choices=STATUS, max_length=25, default="to read")

    def __str__(self):
        return f'{title}'



class Note(models.Model):
    note = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="notes")
    page = models.IntegerField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return f'Note on {book}, page {page}'