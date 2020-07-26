from rest_framework import serializers
from .models import Author, Book, User, Note




class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True)
    class Meta:
        model = Author
        fields = [
            "last_name",
            "first_name",
            "books",
        ]

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

#need work here...need create and update defs for custom updates.  Need individual authors serializer...have it...does it circular reference?
# Can I check create for already in the DB?  If not, WFTN???
    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "status",
        ]


class NoteSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    class Meta:
        model = Note
        fields = [
            "book",
            "note",
        ]