from django.urls import path
from .views import OpportunityList,OpportunityDetail
#from os import environ
#app_name="opportunities"

urlpatterns = [
    path('', OpportunityList.as_view(), name='op-list'),
    path('op/<int:pk>/', OpportunityDetail.as_view(), name='op-detail'),
]