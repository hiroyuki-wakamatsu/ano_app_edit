from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Book


# Create your views here.

#@method_decorator(decorators, name="dispatch")
#class BookList(ListView):

#Functions to render
#def home(request):
#    book_list = Book.objects.all()
#    return render(request,"book/book_list.html",{'books':book_list})

class DTBookList(ListView):
    template_name = "book/dt/book_list.html"
    model = Book
    context_object_name = "dtbooks"