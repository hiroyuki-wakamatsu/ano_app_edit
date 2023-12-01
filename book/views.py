
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Book
from .forms import BookSearchForm

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

class BookList(ListView):
    model = Book
    form_class = BookSearchForm
    context_object_name = 'booklists'
    template_name = 'book/book_lists.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            No = form.cleaned_data.get('No')
            title = form.cleaned_data.get('title')
            category = form.cleaned_data.get('category')
            author = form.cleaned_data.get('author')
            published_date = form.cleaned_data.get('published_date')
            price = form.cleaned_data.get('price')
            stock = form.cleaned_data.get('stock')
            
            if No:
                queryset = queryset.filter(No__gte=No)
            if title:
                queryset = queryset.filter(title__icontains=title)
            if category:
                queryset = queryset.filter(category__startswith=category)
            if author:
                queryset = queryset.filter(author__icontains=author)
            if published_date:
                queryset = queryset.filter(published_date__gte=published_date)
            if price:
                queryset = queryset.filter(price__gte=price) 
            if stock:
                queryset = queryset.filter(stock__startwith =stock)
                
            return queryset
        """        
            # Paginator
            paginator = Paginator(queryset, self.paginate_by)
            page = self.request.GET.get('page')
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            # テンプレートに変数を渡す
            messages.add_message(self.request, messages.INFO, page_obj)
        """
                

    #def paginate_queryset(self, queryset: _BaseQuerySet[Any], page_size: int) -> tuple[Paginator, int, QuerySet[Any], bool]:
    #    return super().paginate_queryset(queryset, page_size)

    def get_context_data(self,*args, **kwargs):
        self.HeadNameList = ['No','タイトル','分類','作者','出版日','価格','在庫','詳細']
        #self.DataUpdateTime = environ['add_opdatasmb_executime']
        context = super(BookList,self).get_context_data(*args,**kwargs)
        
        context.update(dict(form=self.form_class,
                    query_string=self.request.GET.urlencode()))
        
        context['hnl']= self.HeadNameList
        #context['data_update_time'] = self.DataUpdateTime
        context['form']= self.form_class(self.request.GET)
        return context



class BookDetail(DetailView):
    model = Book
    context_object_name = 'BookDetail'
    template_name = 'book/book_detail.html'

