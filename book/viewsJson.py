from django.shortcuts import render
from .models import Book
from django.http import JsonResponse


#Functions to render

def jhome(request):
    book_list = Book.objects.all()
    return render(request,"book/json/book_list.html")

#JSON
def book_json(request):
    books = Book.objects.all()
    data = [Book.get_data(book) for book in books]
    response ={'data':data}
    return JsonResponse(response)