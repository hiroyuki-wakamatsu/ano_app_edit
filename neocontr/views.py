from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import NeoContract
from .forms import CTsearchForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#@method_decorator(decorators, name="dispatch")
class NeoContractList(LoginRequiredMixin, ListView):
    model = NeoContract
    fields = ['ExtID','OrdDe','OrdNo','OrdBrNo','CustPoNo','OurRep','OrdProdName','OrdRemarks','SIdn','MainUnitSN','MainUnitShipDe','MaintStartDe',
              'MaintEndDe','PoNo','PoBranchNo','PoProdNo','ArrivalDe','ShipDe','DelivDe','SalesMonth','OrdCode','OrdCoName','DelDestCode','DelDestCoName',
              'BillDestCode','BillDestCoName','EUCode','EUCoName','ResellerCode','ResellerCoName','InstCode','InstCoName','InstContName','MaintInfoCode',
              'MaintInfoCoName','MaintInfoContName','EstimateNo','MaintRemarks']
    form_class = CTsearchForm
    context_object_name = 'ctlist'
    template_name = 'ct/ct_list.html'
    paginate_by = 20
    ordering =  ['-OrdDe','-ExtID']

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.form_class(self.request.GET)
        if form.is_valid():
            ExtID = form.cleaned_data.get('ExtID')
            OrdDe = form.cleaned_data.get('OrdDe')
            OrdNo = form.cleaned_data.get('OrdNo')
            OrdBrNo = form.cleaned_data.get('OrdBrNo')
            CustPoNo = form.cleaned_data.get('CustPoNo')
            OurRep = form.cleaned_data.get('OurRep')
            OrdProdName = form.cleaned_data.get('OrdProdName')
            OrdRemarks = form.cleaned_data.get('OrdRemarks')
            SIdn = form.cleaned_data.get('SIdn')
            MainUnitSN = form.cleaned_data.get('MainUnitSN')
            MainUnitShipDe = form.cleaned_data.get('MainUnitShipDe')
            MaintStartDe = form.cleaned_data.get('MaintStartDe')
            MaintEndDe = form.cleaned_data.get('MaintEndDe')
            PoNo = form.cleaned_data.get('PoNo')
            PoBranchNo = form.cleaned_data.get('PoBranchNo')
            PoProdNo = form.cleaned_data.get('PoProdNo')
            ArrivalDe = form.cleaned_data.get('ArrivalDe')
            ShipDe = form.cleaned_data.get('ShipDe')
            DelivDe = form.cleaned_data.get('DelivDe')
            SalesMonth = form.cleaned_data.get('SalesMonth')
            OrdCode = form.cleaned_data.get('OrdCode')
            OrdCoName = form.cleaned_data.get('OrdCoName')
            DelDestCode = form.cleaned_data.get('DelDestCode')
            DelDestCoName = form.cleaned_data.get('DelDestCoName')
            BillDestCode = form.cleaned_data.get('BillDestCode')
            BillDestCoName = form.cleaned_data.get('BillDestCoName')
            EUCode = form.cleaned_data.get('EUCode')
            EUCoName = form.cleaned_data.get('EUCoName')
            ResellerCode = form.cleaned_data.get('ResellerCode')
            ResellerCoName = form.cleaned_data.get('ResellerCoName')
            InstCode = form.cleaned_data.get('InstCode')
            InstCoName = form.cleaned_data.get('InstCoName')
            InstContName = form.cleaned_data.get('InstContName')
            MaintInfoCode = form.cleaned_data.get('MaintInfoCode')
            MaintInfoCoName = form.cleaned_data.get('MaintInfoCoName')
            MaintInfoContName = form.cleaned_data.get('MaintInfoContName')
            EstimateNo = form.cleaned_data.get('EstimateNo')
            MaintRemarks = form.cleaned_data.get('MaintRemarks')
            
            if ExtID:
                queryset = queryset.filter(ExtID__icontains=ExtID)
            if OrdDe:
                queryset = queryset.filter(OrdDe__gte=OrdDe).order_by('-OrdDe')
            if OrdNo:
                queryset = queryset.filter(OrdNo__icontains=OrdNo)
            if OrdBrNo:
                queryset = queryset.filter(OrdBrNo__icontains=OrdBrNo)
            if CustPoNo:
                queryset = queryset.filter(CustPoNo__icontains=CustPoNo)
            if OurRep:
                queryset = queryset.filter(OurRep__icontains=OurRep)
            if OrdProdName:
                queryset = queryset.filter(OrdProdName__icontains=OrdProdName)
            if OrdRemarks:
                queryset = queryset.filter(OrdRemarks__icontains=OrdRemarks)
            if SIdn:
                queryset = queryset.filter(SIdn__icontains=SIdn)
            if MainUnitSN:
                queryset = queryset.filter(MainUnitSN__icontains=MainUnitSN)
            if MainUnitShipDe:
                queryset = queryset.filter(MainUnitShipDe__gte=MainUnitShipDe)
            if MaintStartDe:
                queryset = queryset.filter(MaintStartDe__gte=MaintStartDe)
            if MaintEndDe:
                queryset = queryset.filter(MaintEndDe__gte=MaintEndDe)
            if PoNo:
                queryset = queryset.filter(PoNo__icontains=PoNo)
            if PoBranchNo:
                queryset = queryset.filter(PoBranchNo__icontains=PoBranchNo)
            if PoProdNo:
                queryset = queryset.filter(PoProdNo__icontains=PoProdNo)
            if ArrivalDe:
                queryset = queryset.filter(ArrivalDe__gte=ArrivalDe)
            if ShipDe:
                queryset = queryset.filter(ShipDe__gte=ShipDe)
            if DelivDe:
                queryset = queryset.filter(DelivDe__gte=DelivDe)
            if SalesMonth:
                queryset = queryset.filter(SalesMonth__gte=SalesMonth)
            if OrdCode:
                queryset = queryset.filter(OrdCode__icontains=OrdCode)
            if OrdCoName:
                queryset = queryset.filter(OrdCoName__icontains=OrdCoName)
            if DelDestCode:
                queryset = queryset.filter(DelDestCode__icontains=DelDestCode)
            if DelDestCoName:
                queryset = queryset.filter(DelDestCoName__icontains=DelDestCoName)
            if BillDestCode:
                queryset = queryset.filter(BillDestCode__icontains=BillDestCode)
            if BillDestCoName:
                queryset = queryset.filter(BillDestCoName__icontains=BillDestCoName)
            if EUCode:
                queryset = queryset.filter(EUCode__icontains=EUCode)
            if EUCoName:
                queryset = queryset.filter(EUCoName__icontains=EUCoName)
            if ResellerCode:
                queryset = queryset.filter(ResellerCode__icontains=ResellerCode)
            if ResellerCoName:
                queryset = queryset.filter(ResellerCoName__icontains=ResellerCoName)
            if InstCode:
                queryset = queryset.filter(InstCode__icontains=InstCode)
            if InstCoName:
                queryset = queryset.filter(InstCoName__icontains=InstCoName)
            if InstContName:
                queryset = queryset.filter(InstContName__icontains=InstContName)
            if MaintInfoCode:
                queryset = queryset.filter(MaintInfoCode__icontains=MaintInfoCode)
            if MaintInfoCoName:
                queryset = queryset.filter(MaintInfoCoName__icontains=MaintInfoCoName)
            if MaintInfoContName:
                queryset = queryset.filter(MaintInfoContName__icontains=MaintInfoContName)
            if EstimateNo:
                queryset = queryset.filter(EstimateNo__icontains=EstimateNo)
            if MaintRemarks:
                queryset = queryset.filter(MaintRemarks__icontains=MaintRemarks)
                
            return queryset
            
    def get_context_data(self,*args, **kwargs):
        self.HeadNameList = ['外部ＩＤ','受注日付','受注番号','受注枝番','客先注文番号','当社担当者','受注品名','受注備考','SID','本体SN','本体出荷日','保守開始日','保守終了日','仕入番号','仕入枝番','仕入品番','入荷日','出荷日','納品日','売上 月','発注元コード','発注元会社名','納品先コード','納品先会社名','請求先コード','請求先会社名','EUコード','EU会社名','リセラーコー ド','リセラー会社名','設置先コード','設置先会社名','設置先担当者名','保守案内先コード','保守案内先会社名','保守案内先担当者名','見積番号','保守備考']
        context = super(NeoContractList,self).get_context_data(*args,**kwargs)
        context.update(dict(form=self.form_class,query_string=self.request.GET.urlencode()))
        context['hnl']= self.HeadNameList
        context['form']= self.form_class(self.request.GET)
        return context

#@method_decorator(decorators, name="dispatch")
class NeoContractDetail(LoginRequiredMixin, DetailView):
    model = NeoContract
    context_object_name = 'ctdetail'
    template_name = 'ct/ct_detail.html'
