from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import opportunity
from .forms import OPsearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
#from os import environ


# Create your views here.

#@method_decorator(decorators, name="dispatch")
class OpportunityList(LoginRequiredMixin, ListView):
    model = opportunity
    form_class = OPsearchForm
    context_object_name = 'oplist'
    template_name = 'op/op_list.html'
    paginate_by = 20
    ordering =  ['-CaseID','-OccurDate']

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            CaseID = form.cleaned_data.get('CaseID')
            CaseName = form.cleaned_data.get('CaseName')
            Representative = form.cleaned_data.get('Representative')
            Category = form.cleaned_data.get('Category')
            CustomerName = form.cleaned_data.get('CustomerName')
            Creator = form.cleaned_data.get('Creator')
            OccurDate = form.cleaned_data.get('OccurDate')
            ExpectedOrderDate = form.cleaned_data.get('ExpectedOrderDate')
            ExpectedRevenueDate = form.cleaned_data.get('ExpectedRevenueDate')
            CreatedDate = form.cleaned_data.get('CreatedDate')
            UpdatedDate = form.cleaned_data.get('UpdatedDate')                        
            Updater = form.cleaned_data.get('Updater')
            
            if CaseID:
                queryset = queryset.filter(CaseID__gte=CaseID)
            if CaseName:
                queryset = queryset.filter(CaseName__icontains=CaseName)
            if Representative:
                queryset = queryset.filter(Representative__icontains=Representative)
            if Category:
                queryset = queryset.filter(Category__icontains=Category)
            if CustomerName:
                queryset = queryset.filter(CustomerName__icontains=CustomerName)
            if Creator:
                queryset = queryset.filter(Creator__icontains=Creator) 
            if OccurDate:
                queryset = queryset.filter(OccurDate__gte=OccurDate)
            if ExpectedOrderDate:
                queryset = queryset.filter(OccurDate__gte=ExpectedOrderDate)
            if ExpectedRevenueDate:
                queryset = queryset.filter(OccurDate__gte=ExpectedRevenueDate)
            if CreatedDate:
                queryset = queryset.filter(OccurDate__gte=CreatedDate)
            if UpdatedDate:
                queryset = queryset.filter(OccurDate__gte=UpdatedDate)
            if Updater:
                queryset = queryset.filter(Creator__icontains=Updater)                 

            return queryset

    def get_context_data(self,*args, **kwargs):
        self.HeadNameList = ['案件ID','案件名','当社担当者','分類','顧客名','作成者','発生日','受注予定日','売上予定日','作成日','更新日','更新者','SFAサイトリンク']
        #self.DataUpdateTime = environ['add_opdatasmb_executime']
        #DataUpdatedTime = kwargs['UpdatedTime']
        context = super(OpportunityList,self).get_context_data(*args,**kwargs)
        context.update(dict(form=self.form_class,query_string=self.request.GET.urlencode()))
        context['hnl']= self.HeadNameList
        #context['DataUpdatedTime'] = DataUpdatedTime
        context['form']= self.form_class(self.request.GET)
        return context

class OpportunityDetail(LoginRequiredMixin, DetailView):
    model = opportunity
    context_object_name = 'opdetail'
    template_name = 'op/op_detail.html'
