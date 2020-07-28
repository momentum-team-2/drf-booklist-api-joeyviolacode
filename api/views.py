from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import BookSerializer, AuthorSerializer, NoteSerializer, UserSerializer
from .models import Book, Author, Note, User
from rest_framework import generics, permissions, status
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.query import QuerySet
from django.contrib.postgres.search import SearchVector




# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    """
    Testing text on API root?
    """
    return Response({
        'books': reverse('books', request=request, format=format),
        'notes': reverse('all-notes', request=request, format=format),
        'authors': reverse('authors', request=request, format=format),
    })
    

class BooksList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['status']
    serializer_class = BookSerializer

    # def get_queryset(self):
    #     queryset = Book.objects.filter(owner=self.request.user)
    #     return queryset

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Book.objects.all().filter(owner=self.request.user)
        else: 
            queryset = Book.objects.none()
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AllNotesList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]


class NotesList(APIView):
    """
    This endpoint shows all notes belonging to a single book.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        notes = book.notes.all().filter(owner=request.user).order_by("-time_created")
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = NoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user, book=book)


class AuthorsList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserTimeline(APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        notes = user.notes.all().order_by("-time_created")
        serializer = NoteSerializer(notes, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class TimelineSetting(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Search(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwner, permissions.IsAuthenticated]
    serializer_class = BookSerializer
    
    def get(self, request, query):
        if request.user.is_authenticated:
            if query is not None:
                books = Book.objects.annotate(search=SearchVector(
                    "title", "notes__note", "authors__first_name", "authors__last_name")).filter(
                        search=query, owner=request.user).distinct("id").order_by("-pk")
            else:
                books = None
        else: 
            queryset = Book.objects.none()
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



# class BooksList(APIView):
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     # filter_backends = (DjangoFilterBackend,)
#     # serializer_class = BookSerializer
#     # queryset = Book.objects.all()

#     # def filter_queryset(self, queryset):
#     #     for backend in list(self.filter_backends):
#     #         queryset = backend().filter_queryset(self.request, queryset, self)
#     #     return queryset

#     # def get_queryset(self):
#     #     assert self.queryset is not None, (
#     #         "'%s' should either include a `queryset` attribute, "
#     #         "or override the `get_queryset()` method."
#     #         % self.__class__.__name__
#     #     )
#     #     queryset = self.queryset
#     #     if isinstance(queryset, QuerySet):
#     #         # Ensure queryset is re-evaluated on each request.
#     #         queryset = queryset.all().filter(owner=self.request.user)
#     #     return queryset

#     def get(self, request):
#         if request.user.is_authenticated:
#             books = Book.objects.all().filter(owner=request.user)
#         else:
#             books = []
#         # books = self.filter_queryset(self.queryset)
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = BookSerializer(data=request.data, context={'request': request})
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BookDetail(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request, pk):
#         book = get_object_or_404(Book, pk=pk)
#         serializer = BookSerializer(book, context={'request': request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
