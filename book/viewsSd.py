from django_serverside_datatable.views import ServerSideDatatableView
from .models import Book

class BookListWithAjaxDT(ServerSideDatatableView):
    queryset = Book.objects.all()
    columns = ['No','title','category','author','published_date','price','stock']
#    columns = ['No','title']
#    template_name = 'book/ajax/book_lists.html'