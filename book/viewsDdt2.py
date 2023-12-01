from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
from .models import Book
from .tables import BookTable
from .filters import BookFilter


class FilterdBookList(SingleTableMixin,FilterView):
    model = Book
    table_class = BookTable
    template_name = 'book/ddt2/book_lists.html'
    filterset_class = BookFilter