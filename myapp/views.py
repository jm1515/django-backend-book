from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from .models import Book
from .serializers import BookSerializer

# Create your views here.

def index(request):
    return HttpResponse("Hello world. You're at the 'myapp' index.")

class BookList(APIView):
    """
    List all books, or create a new book.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """ List all books """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        """ Create new book """
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

class BookDetail(APIView):
    """
    Retrieve, update or delete a book instance.
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """ Retrieve a book instance """
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, safe=False)
    
    def put(self, request, pk, format=None):
        """ Update a book instance """
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """ Delete a book instance """
        book = self.get_object(pk)
        book.delete()
        return JsonResponse({}, safe=False, status=status.HTTP_204_NO_CONTENT)
        