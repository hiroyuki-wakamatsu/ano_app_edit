from datetime import date, timedelta
from django import forms
#from django.core.validators import MaxLengthValidator,RegexValidator,MaxValueValidator

InitOccureDateDays = 90

class OPsearchForm(forms.Form):

    CaseID = forms.IntegerField(
        label='案件情報ID', required=False, 
        widget=forms.NumberInput(attrs={'placeholder':'37748','max':100000,'style':'max-width: 5em' }),
        help_text='入力番号より大きい案件情報ID',
    #    validators=[MaxValueValidator(limit_value=100000,message='入力値は1000000以内の数字で入力してください')]
        ) 
    CaseName = forms.CharField(
        label='案件名', required=False, 
        widget=forms.TextInput(attrs={'max':30,'style':'max-width: 60em' }),
        help_text='入力文字列を含む案件名',
    #    validators=[MaxLengthValidator(limit_value=20,message='入力値は20文字以内で入力してください')]
        ) 
    Representative = forms.CharField(
        label='担当者名', required=False,
        widget=forms.TextInput(attrs={'max':10,'style':'max-width: 6em' }),
        help_text='入力文字列を含む担当者名',
    #    validators=[MaxLengthValidator(limit_value=20,message='入力値は20文字以内で入力してください')]
        ) 
    Category = forms.CharField(
        label='分類', required=False,
        initial='Fortinet',
        widget=forms.TextInput(attrs={'placeholder':'Fortinet','max':10,'style':'max-width: 6em' }),
        help_text='入力文字列を含む分類',
    #    validators=[MaxLengthValidator(limit_value=20,message='入力値は20文字以内で入力してください')]
        ) 
    
    CustomerName = forms.CharField(
        label='顧客名', required=False,
        widget=forms.TextInput(attrs={'max':20,'style':'max-width: 15em' }),
        help_text='入力文字列を含む顧客名',
    #    validators=[MaxLengthValidator(limit_value=20,message='入力値は20文字以内で入力してください')]
        ) 
    Creator = forms.CharField(
        label='作成者名', required=False, 
        widget=forms.TextInput(attrs={'max':10,'style':'max-width: 6em' }),
        help_text='入力文字列を含む担当者名',
    #    validators=[MaxLengthValidator(limit_value=20,message=('入力値は20文字以内で入力してくさい'),)]
        )
    OccurDate = forms.DateField(
        label='発生日', required=False,
        initial=date.today() - timedelta(days=InitOccureDateDays),
        widget=forms.DateInput(attrs={'placeholder':'2023-5-8','style':'max-width: 6em' }),
        help_text='入力日付(yyyy-mm-dd形式)より新しい発生日',
    #    #validators=[RegexValidator(regex=r'^[2000-2200]{4}-[1-12]{1,2}-[1-31]{1,2}$',message='日付はyyyy-mm-dd形式で入力してください') ]
        ) 
    ExpectedOrderDate = forms.DateField(
        label='受注予定日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-5-8','style':'max-width: 6em' }),
        help_text='入力日付(yyyy-mm-dd形式)より新しい発生日',
    #    #validators=[RegexValidator(regex=r'^[2000-2200]{4}-[1-12]{1,2}-[1-31]{1,2}$',message='日付はyyyy-mm-dd形式で入力してください') ]
        ) 
    ExpectedRevenueDate = forms.DateField(
        label='売上予定日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-5-8','style':'max-width: 6em' }),
        help_text='入力日付(yyyy-mm-dd形式)より新しい発生日',
    #    #validators=[RegexValidator(regex=r'^[2000-2200]{4}-[1-12]{1,2}-[1-31]{1,2}$',message='日付はyyyy-mm-dd形式で入力してください') ]
        ) 
    CreatedDate = forms.DateField(
        label='作成日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-5-8','style':'max-width: 8em' }),
        help_text='入力日付(yyyy-mm-dd形式)より新しい発生日',
    #    #validators=[RegexValidator(regex=r'^[2000-2200]{4}-[1-12]{1,2}-[1-31]{1,2}$',message='日付はyyyy-mm-dd形式で入力してください') ]
        ) 
    UpdatedDate = forms.DateField(
        label='更新日', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2023-5-8','style':'max-width: 8em' }),
        help_text='入力日付(yyyy-mm-dd形式)より新しい発生日',
    #    #validators=[RegexValidator(regex=r'^[2000-2200]{4}-[1-12]{1,2}-[1-31]{1,2}$',message='日付はyyyy-mm-dd形式で入力してください') ]
        ) 
    Updater = forms.CharField(
        label='更新者', required=False, 
        widget=forms.TextInput(attrs={'max':10,'style':'max-width: 6em' }),
        help_text='入力文字列を含む担当者名',
    #    validators=[MaxLengthValidator(limit_value=20,message=('入力値は20文字以内で入力してくさい'),)]
        )

    def clean_CaseID(self):
        CaseID = self.cleaned_data['CaseID']
        if CaseID is not None:
            if CaseID < 0:
                raise forms.ValidationError('案件情報IDは1以上の数字で入力してください。')
        return CaseID
    
    def clean_CaseName(self):
        CaseName = self.cleaned_data['CaseName']
        if CaseName is not None:
            if len(CaseName) > 20:
                raise forms.ValidationError('案件名は20文字以内で入力してください。')
        return CaseName
    
    def clean_Representative(self):
        Representative = self.cleaned_data['Representative']
        if Representative is not None:
            if len(Representative) > 20:
                raise forms.ValidationError('担当者名は20文字以内で入力してください。')
        return Representative
    
    def clean_Category(self):
        Category = self.cleaned_data['Category']
        if Category is not None:
            if len(Category) > 15:
                raise forms.ValidationError('製品カテゴリーを15文字以内で入力してください。')
        return Category
    
    def clean_CustomerName(self):
        CustomerName = self.cleaned_data['CustomerName']
        if CustomerName is not None:
            if len(CustomerName) > 20:
                raise forms.ValidationError('顧客名は20文字以内で入力してください。')
        return CustomerName
    
    def clean_Creator(self):
        Creator = self.cleaned_data['Creator']
        if Creator is not None:
            if len(Creator) > 20:
                raise forms.ValidationError('作成者名は20文字以内で入力してください。')
        return Creator
            
    def clean_OccurDate(self):
        OccurDate = self.cleaned_data['OccurDate']
        if OccurDate is not None:
            if not OccurDate.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
            if not self.cleaned_data.get('OccurDate'):
                self.cleaned_data['OccurDate'] = date.today() - timedelta(days=InitOccureDateDays)
        return OccurDate
    
    def clean_ExpectedOrderDate(self):
        ExpectedOrderDate = self.cleaned_data['ExpectedOrderDate']
        if ExpectedOrderDate is not None:
            if not ExpectedOrderDate.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return ExpectedOrderDate

    def clean_ExpectedRevenueDate(self):
        ExpectedRevenueDate= self.cleaned_data['ExpectedRevenueDate']
        if ExpectedRevenueDate is not None:
            if not ExpectedRevenueDate.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return ExpectedRevenueDate
    
    def clean_CreatedDate(self):
        CreatedDate = self.cleaned_data['CreatedDate']
        if CreatedDate is not None:
            if not CreatedDate.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return CreatedDate

    def clean_UpdatedDate(self):
        UpdatedDate = self.cleaned_data['UpdatedDate']
        if UpdatedDate is not None:
            if not UpdatedDate.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
        return UpdatedDate
    
    def clean_Updater(self):
        Updater = self.cleaned_data['Updater']
        if Updater is not None:
            if len(Updater) > 20:
                raise forms.ValidationError('作成者名は20文字以内で入力してください。')
        return Updater
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data