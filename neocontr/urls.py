from django.urls import path
from .views import NeoContractList,NeoContractDetail

#app_name = "neocontract"
urlpatterns = [
    path('', NeoContractList.as_view(), name='ct-list'),
    path('ct/<str:pk>/', NeoContractDetail.as_view(), name='ct-detail'),
]