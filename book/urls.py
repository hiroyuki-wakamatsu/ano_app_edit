from django.urls import path
from .views import BookList,BookDetail
from .viewsDdt2 import FilterdBookList
from .viewsSd import BookListWithAjaxDT
from .viewsDt import DTBookList
from .viewsJson import book_json,jhome



#app_name = "Book"
urlpatterns = [
    #Bootstrap5 and CBV are used
    path('', BookList.as_view(), name='book-list'),
    
    #django-table2,django-filters packages are used
    path('ddt2/', FilterdBookList.as_view(), name='ddt2book-list'),
    
    #django-serverside-datatable is used
    #https://pypi.org/project/django-serverside-datatable/
    path('sd/', BookListWithAjaxDT.as_view(), name='sdbook-list'),
    
    #datatable is used
    path('dt/', DTBookList.as_view(), name='dtbook-list'),
    
    #JSON output for connection datatable with ajax  
    #JSON Response
    path('json/', jhome,name='jsbook-list'),
    #Json output
    path('json/source/', book_json, name='jsbook-source'),
    
    path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]