from datetime import date, timedelta
from django import forms
#from django.core.validators import MaxLengthValidator,RegexValidator,MaxValueValidator

class CTsearchForm(forms.Form):
    
    ExtID = forms.CharField(
         label='外部ＩＤ', required=False,
         widget=forms.TextInput(attrs={'style':'max-width: 5em'} ),
         help_text='入力文字列を含む',
         )
    OrdDe = forms.DateField(
        label='受注日付', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8','style':'max-width: 5em' } ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    OrdNo = forms.CharField(
        label='受注番号', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 4em' } ),
        help_text='入力文字列を含む',
        )
    OrdBrNo = forms.CharField(
        label='受注枝番', required=False,
        widget=forms.NumberInput(attrs={'style':'max-width: 3em' } ),
        help_text='入力文字列を含む',
        )
    CustPoNo = forms.CharField(
        label='客先注文番号', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 3em'}),
        help_text='入力文字列を含む',
        )
    OurRep = forms.CharField(
        label='当社担当者', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em' } ),
        help_text='入力文字列を含む',
        )
    OrdProdName = forms.CharField (
        label='受注品名', required=False,
        widget=forms.TextInput(attrs={'placeholder':'Fortigate', 'style':'max-width: 16em'} ),
        help_text='入力文字列を含む',
        )
    OrdRemarks = forms.CharField (
        label='受注備考', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    SIdn = forms.CharField(
        label='SID', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 8em'}),
        help_text='入力文字列を含む',
        )
    MainUnitSN = forms.CharField(
        label='本体SN', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 8em'}),
        help_text='入力文字列を含む',
        )
    MainUnitShipDe = forms.DateField(
        label='本体出荷日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'}),
        help_text='入力文字列を含む',
        )
    MaintStartDe = forms.DateField(
        label='保守開始日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'} ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    MaintEndDe = forms.DateField(
        label='保守終了日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'} ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    PoNo = forms.CharField(
        label='仕入番号', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    PoBranchNo = forms.CharField(
        label='仕入枝番', required=False,
        widget=forms.NumberInput(attrs={'style':'max-width: 4em'} ),
        help_text='入力文字列を含む',
        )
    PoProdNo = forms.CharField(
        label='仕入品番', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 10em'}),
        help_text='入力文字列を含む',
        )
    ArrivalDe = forms.DateField(
        label='入荷日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'} ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    ShipDe = forms.DateField(
        label='出荷日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8','style':'max-width: 5em' } ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    DelivDe = forms.DateField(
        label='納品日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'} ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    SalesMonth = forms.DateField(
        label='売上月', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-7-8', 'style':'max-width: 5em'} ),
        help_text='入力日付(yyyy-mm-dd形式)より新しい日',
        )
    OrdCode = forms.CharField(
        label='発注元コード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    OrdCoName = forms.CharField(
        label='発注元会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 10em'}),
        help_text='入力文字列を含む',
        )
    DelDestCode = forms.CharField(
        label='納品先コード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    DelDestCoName = forms.CharField(
        label='納品先会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    BillDestCode = forms.CharField(
        label='請求先コード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    BillDestCoName = forms.CharField(
        label='請求先会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    EUCode = forms.CharField(
        label='EUコード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    EUCoName = forms.CharField(
        label='EU会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    ResellerCode = forms.CharField(
        label='リセラーコー ド', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    ResellerCoName = forms.CharField(
        label='リセラー会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    InstCode = forms.CharField(
        label='設置先コード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 4em'}),
        help_text='入力文字列を含む',
        )
    InstCoName = forms.CharField(
        label='設置先会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    InstContName = forms.CharField(
        label='設置先担当者名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    MaintInfoCode = forms.CharField(
        label='保守案内先コード', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    MaintInfoCoName = forms.CharField(
        label='保守案内先会社名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 12em'}),
        help_text='入力文字列を含む',
        )
    MaintInfoContName = forms.CharField(
        label='保守案内先担当者名', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 6em'}),
        help_text='入力文字列を含む',
        )
    EstimateNo = forms.CharField(
        label='見積番号', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 10em'}),
        help_text='入力文字列を含む',
        )
    MaintRemarks = forms.CharField(
        label='保守備考', required=False,
        widget=forms.TextInput(attrs={'style':'max-width: 10em'}),
        help_text='入力文字列を含む',
        )
    
    def clean_ExtID(self):
        ExtID = self.cleaned_data['ExtID']
        if ExtID is not None:
            if len(ExtID) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return ExtID
    def clean_OrdDe(self):
        OrdDe = self.cleaned_data['OrdDe']
        if OrdDe is not None:
            if not OrdDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return OrdDe
    def clean_OrdNo(self):
        OrdNo = self.cleaned_data['OrdNo']
        if OrdNo is not None:
            if len(OrdNo) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OrdNo
    def clean_OrdBrNo(self):
        OrdBrNo = self.cleaned_data['OrdBrNo']
        if OrdBrNo is not None:
            if len(OrdBrNo) > 20:
                raise forms.ValidationError('5桁以内数字入力してください')
        return OrdBrNo
    def clean_CustPoNo(self):
        CustPoNo = self.cleaned_data['CustPoNo']
        if CustPoNo is not None:
            if len(CustPoNo) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return CustPoNo
    def clean_OurRep(self):
        OurRep = self.cleaned_data['OurRep']
        if OurRep is not None:
            if len(OurRep) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OurRep
    def clean_OrdProdName(self):
        OrdProdName = self.cleaned_data['OrdProdName']
        if OrdProdName is not None:
            if len(OrdProdName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OrdProdName
    def clean_OrdRemarks(self):
        OrdRemarks = self.cleaned_data['OrdRemarks']
        if OrdRemarks is not None:
            if len(OrdRemarks) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OrdRemarks
    def clean_SIdn(self):
        SIdn = self.cleaned_data['SIdn']
        if SIdn is not None:
            if len(SIdn) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return SIdn
    def clean_MainUnitSN(self):
        MainUnitSN = self.cleaned_data['MainUnitSN']
        if MainUnitSN is not None:
            if len(MainUnitSN) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return MainUnitSN
    def clean_MainUnitShipDe(self):
        MainUnitShipDe = self.cleaned_data['MainUnitShipDe']
        if MainUnitShipDe is not None:
           if not MainUnitShipDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return MainUnitShipDe
    def clean_MaintStartDe(self):
        MaintStartDe = self.cleaned_data['MaintStartDe']
        if MaintStartDe is not None:
            if not MaintStartDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return MaintStartDe
    def clean_MaintEndDe(self):
        MaintEndDe = self.cleaned_data['MaintEndDe']
        if MaintEndDe is not None:
            if not MaintEndDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return MaintEndDe
    def clean_PoNo(self):
        PoNo = self.cleaned_data['PoNo']
        if PoNo is not None:
            if len(PoNo) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return PoNo
    def clean_PoBranchNo(self):
        PoBranchNo = self.cleaned_data['PoBranchNo']
        if PoBranchNo is not None:
               if len(PoBranchNo) > 20:
                   raise forms.ValidationError('5桁以内の数字を入力してください')
        return PoBranchNo
    
    def clean_PoProdNo(self):
        PoProdNo = self.cleaned_data['PoProdNo']
        if PoProdNo is not None:
            if len(PoProdNo) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return PoProdNo
    def clean_ArrivalDe(self):
        ArrivalDe = self.cleaned_data['ArrivalDe']
        if ArrivalDe is not None:
           if not ArrivalDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return ArrivalDe
    def clean_ShipDe(self):
        ShipDe = self.cleaned_data['ShipDe']
        if ShipDe is not None:
            if not ShipDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return ShipDe
    def clean_DelivDe(self):
        DelivDe = self.cleaned_data['DelivDe']
        if DelivDe is not None:
            if not DelivDe.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return DelivDe
    def clean_SalesMonth(self):
        SalesMonth = self.cleaned_data['SalesMonth']
        if SalesMonth is not None:
            if not SalesMonth.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return SalesMonth
    def clean_OrdCode(self):
        OrdCode = self.cleaned_data['OrdCode']
        if OrdCode is not None:
            if len(OrdCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OrdCode
    def clean_OrdCoName(self):
        OrdCoName = self.cleaned_data['OrdCoName']
        if OrdCoName is not None:
            if len(OrdCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return OrdCoName
    def clean_DelDestCode(self):
        DelDestCode = self.cleaned_data['DelDestCode']
        if DelDestCode is not None:
            if len(DelDestCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return DelDestCode
    def clean_DelDestCoName(self):
        DelDestCoName = self.cleaned_data['DelDestCoName']
        if DelDestCoName is not None:
            if len(DelDestCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return DelDestCoName
    def clean_BillDestCode(self):
        BillDestCode = self.cleaned_data['BillDestCode']
        if BillDestCode is not None:
            if len(BillDestCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return BillDestCode
    def clean_BillDestCoName(self):
        BillDestCoName = self.cleaned_data['BillDestCoName']
        if BillDestCoName is not None:
            if len(BillDestCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return BillDestCoName
    def clean_EUCode(self):
        EUCode = self.cleaned_data['EUCode']
        if EUCode is not None:
            if len(EUCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return EUCode
    def clean_EUCoName(self):
        EUCoName = self.cleaned_data['EUCoName']
        if EUCoName is not None:
            if len(EUCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return EUCoName
    def clean_ResellerCode(self):
        ResellerCode = self.cleaned_data['ResellerCode']
        if ResellerCode is not None:
            if len(ResellerCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return ResellerCode
    def clean_ResellerCoName(self):
        ResellerCoName = self.cleaned_data['ResellerCoName']
        if ResellerCoName is not None:
            if len(ResellerCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return ResellerCoName
    def clean_InstCode(self):
        InstCode = self.cleaned_data['InstCode']
        if InstCode is not None:
            if len(InstCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return InstCode
    def clean_InstCoName(self):
        InstCoName = self.cleaned_data['InstCoName']
        if InstCoName is not None:
            if len(InstCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return InstCoName
    def clean_InstContName(self):
        InstContName = self.cleaned_data['InstContName']
        if InstContName is not None:
            if len(InstContName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return InstContName
    def clean_MaintInfoCode(self):
        MaintInfoCode = self.cleaned_data['MaintInfoCode']
        if MaintInfoCode is not None:
            if len(MaintInfoCode) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return MaintInfoCode
    def clean_MaintInfoCoName(self):
        MaintInfoCoName = self.cleaned_data['MaintInfoCoName']
        if MaintInfoCoName is not None:
            if len(MaintInfoCoName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return MaintInfoCoName
    def clean_MaintInfoContName(self):
        MaintInfoContName = self.cleaned_data['MaintInfoContName']
        if MaintInfoContName is not None:
            if len(MaintInfoContName) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return MaintInfoContName
    def clean_EstimateNo(self):
        EstimateNo = self.cleaned_data['EstimateNo']
        if EstimateNo is not None:
            if len(EstimateNo) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return EstimateNo
    def clean_MaintRemarks(self):
        MaintRemarks = self.cleaned_data['MaintRemarks']
        if MaintRemarks is not None:
            if len(MaintRemarks) > 20:
                raise forms.ValidationError('20文字以内で入力してください')
        return MaintRemarks
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data