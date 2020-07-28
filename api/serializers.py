from rest_framework import serializers
from .models import Author, Book, User, Note


class AuthorSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(many=True, required=False, read_only=True)
    # books = serializers.PrimaryKeyRelatedField(many=True, required=False)
    class Meta:
        model = Author
        fields = [
            "last_name",
            "first_name",
            "books",
        ]


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    book = serializers.StringRelatedField(required=False, read_only=True)
    # book = serializers.PrimaryKeyRelatedField(required=False)

    class Meta:
        model = Note
        fields = [
            "url",
            "book",
            "page",
            "note",
            "public",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "show_timeline"
        ]



class BookSerializer(serializers.HyperlinkedModelSerializer):
    authors = AuthorSerializer(many=True, required=False)
    notes = NoteSerializer(many=True, required=False)

#need work here...need create and update defs for custom updates.  Need individual authors serializer...have it...does it circular reference?
# Can I check create for already in the DB?  If not, WFTN???
    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        notes = validated_data.pop('notes', [])
        book = Book.objects.create(**validated_data)
        for author in authors:
            book.authors.create(**author)
        for note in notes:
            book.notes.create(owner=book.owner, **note)
        return book

    def update(self, instance, validated_data):
        book = instance
        authors = validated_data.pop('authors', [])
        notes = validated_data.pop('notes', [])
        for key, value in validated_data.items():
            setattr(book, key, value)
        book.save()

        book.authors.all().delete()
        book.notes.all().delete()
        for author in authors:
            book.authors.create(**author)
        for note in notes:
            book.notes.create(owner=book.owner, **note)
        return book
    
    class Meta:
        model = Book
        fields = [
            "url",
            "title",
            "authors",
            "status",
            "notes",
        ]