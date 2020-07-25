from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import BookSerializer, AuthorSerializer, NoteSerializer
from .models import Book, Author, Note



# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'books': reverse('book_list', request=request, format=format),
        'notes': reverse('notes_list', request=request, format=format),
        'authors': reverse('authors_list', request=request, format=format),
    })

class BooksList(APIView):
   
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class NotesList(APIView):
    pass

class AuthorsList(APIView):
    pass