import django_tables2 as tables
from .models import Book

class BookTable(tables.Table):
    class Meta:
        model = Book
        template_name= "django_tables2/bootstrap.html"
        fields = ("No","title","category","author","published_date","price","stock" )