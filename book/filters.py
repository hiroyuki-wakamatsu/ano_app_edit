from django_filters import FilterSet
from .models import Book

class BookFilter(FilterSet):
    class Meta:
        model = Book
        fields = {"No":["gte"],"title": ["contains"], "category": ["exact"], "author": ["contains"], "published_date":["gte"],"price": ["gte"]}