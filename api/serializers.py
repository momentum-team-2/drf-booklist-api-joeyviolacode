from rest_framework import serializers
from .models import Author, Book, User, Note


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    class Meta:
        fields = [
            "title",
            "authors",
            "status",
        ]

class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    class Meta:
        fields = [
            "name",
            "books",
        ]

class NoteSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    class Meta:
        fields = [
            "book",
            "note",
        ]