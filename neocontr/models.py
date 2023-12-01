from django.db import models

# Create your models here.
class NeoContract(models.Model):
    ExtID = models.CharField(max_length=64, primary_key=True)
    OrdDe = models.DateField()
    OrdNo = models.CharField(max_length=32)
    #OrdBrNo = models.PositiveIntegerField()
    OrdBrNo = models.CharField(max_length=32)
    CustPoNo = models.CharField(max_length=128)
    OurRep = models.CharField(max_length=32 )
    OrdProdNo = models.CharField(max_length=128 )
    OrdProdName = models.CharField(max_length=128 )
    OrdUnitPrice = models.BigIntegerField() 
    OrdRemarks = models.CharField(max_length=256 )
    SIdn = models.CharField(max_length=64 )
    MainUnitGrID = models.CharField(max_length=64 )
    TELKeyNo = models.CharField(max_length=32)
    #SubKeyNo = models.PositiveSmallIntegerField()
    SubKeyNo = models.CharField(max_length=8)
    CID = models.CharField(max_length=64 )
    MainUnitSN = models.CharField(max_length=64 )
    MainUnitShipVer = models.CharField(max_length=128 )
    MainUnitShipDe = models.DateField()
    MainUnitFlag = models.BooleanField()
    MainUnitExcHist = models.CharField(max_length=256 )
    MaintStartDe = models.DateField()
    MaintEndDe = models.DateField()
    UpdateFlag = models.BooleanField()
    SalStatus = models.BooleanField()
    ProvisionalOrd = models.BooleanField()
    CancelFlag = models.BooleanField()
    PoNo = models.CharField(max_length=64)
    #PoBranchNo = models.PositiveIntegerField()
    PoBranchNo = models.CharField(max_length=32)
    PoProdNo = models.CharField(max_length=128)
    ContNo = models.CharField(max_length=128 )
    ExpDe = models.DateField()
    PoCreatDe = models.DateField()
    ArrivalDe = models.DateField()
    ShipDe = models.DateField()
    DelivDe = models.DateField()
    GuidebookCreatDe = models.DateField()
    ReqFormCreatDe = models.DateField()
    SalesMonth = models.DateField()
    InvoiceCreatDe = models.DateField()
    ExpectedPayDe = models.DateField()
    ModelName = models.CharField(max_length=128)
    #ProdClassCode = models.PositiveIntegerField()
    ProdClassCode = models.CharField(max_length=16)
    ProdClassSymbol = models.CharField(max_length=32 )
    MaintType = models.CharField(max_length=32 )
    #LicensePeriod = models.SmallIntegerField()
    LicensePeriod = models.CharField(max_length=16)
    NoticeProdNo = models.CharField(max_length=128 )
    NoticeProdName = models.CharField(max_length=256 )
    OrdCode = models.CharField(max_length= 64)
    OrdCoName = models.CharField(max_length=128 )
    DelDestCode = models.CharField(max_length=64 )
    DelDestCoName = models.CharField(max_length=128 )
    DelDestDtName = models.CharField(max_length=128 )
    DelDestPic = models.CharField(max_length=64 )
    DelDestTEL = models.CharField(max_length=32 )
    DelDestPostalCode = models.CharField(max_length=16 )
    DelDestAdd = models.CharField(max_length=128 )
    BillDestCode = models.CharField(max_length=64 )
    BillDestCoName = models.CharField(max_length=128 )
    BillDestDtName = models.CharField(max_length=128 )
    BillDestPic = models.CharField(max_length=64 )
    BillDestTEL = models.CharField(max_length=32 )
    BillDestPostalCode = models.CharField(max_length=16 )
    BillDestAdd = models.CharField(max_length=128 )
    EUCode = models.CharField(max_length=64 )
    EUSalesDist = models.BooleanField()
    EUTechDist = models.BooleanField()
    EUCoName = models.CharField(max_length=128 )
    EUDtName = models.CharField(max_length=128 )
    EUContName = models.CharField(max_length=64 )
    EUEmailAdd = models.CharField(max_length=128 )
    ResellerCode = models.CharField(max_length=64 )
    ResellerSalesDist = models.BooleanField()
    ResellerTechDist = models.BooleanField()
    ResellerCoName = models.CharField(max_length=128 )
    ResellerDtName = models.CharField(max_length=128 )
    ResellerContName = models.CharField(max_length=64 )
    ResellerEmailAdd = models.CharField(max_length=128 )
    InstCode = models.CharField(max_length=64 )
    InstCoName = models.CharField(max_length=128 )
    InstDtName = models.CharField(max_length=128 )
    InstContName = models.CharField(max_length=64 )
    InstEmailAdd = models.CharField(max_length=128 )
    InstTEL = models.CharField(max_length=32 )
    InstPostalCode = models.CharField(max_length=16 )
    InstAdd = models.CharField(max_length=128 )
    MaintInfoCode = models.CharField(max_length=64 )
    MaintInfoCoName = models.CharField(max_length=128 )
    MaintInfoDtName = models.CharField(max_length=128 )
    MaintInfoContName = models.CharField(max_length=64 )
    MaintInfoEmailAdd = models.CharField(max_length=128 )
    MaintInfoTEL = models.CharField(max_length=32 )
    MaintInfoPostalCode = models.CharField(max_length=16 )
    MaintInfoAdd = models.CharField(max_length=128 )
    DirectSupportFlag = models.BooleanField()
    MainUnitOrdNo = models.CharField(max_length=64 )
    MainUnitOrdProdNo = models.CharField(max_length=64 )
    MainUnitPoProdNo = models.CharField(max_length=64 )
    IPAdd = models.CharField(max_length=64 )
    StPartNo = models.CharField(max_length=64 )
    EstimateNo = models.CharField(max_length=256 )
    RegRemarks = models.CharField(max_length=256 )
    MaintRemarks = models.CharField(max_length=256 )
    FortiCareType = models.CharField(max_length=128 )

    class Meta:
        ordering= ['-OrdDe','-ExtID']
        db_table= 'neo_contract'