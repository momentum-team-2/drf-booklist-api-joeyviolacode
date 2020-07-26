from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import BookSerializer, AuthorSerializer, NoteSerializer
from .models import Book, Author, Note
from rest_framework import generics, permissions, status



# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'books': reverse('books', request=request, format=format),
        # 'notes': reverse('notes_list', request=request, format=format),
        'authors': reverse('authors_list', request=request, format=format),
    })

class BooksList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.user.is_authenticated:
            books = Book.objects.all().filter(owner=request.user)
        else:
            books = []
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotesList(APIView):
    pass

class AuthorsList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]