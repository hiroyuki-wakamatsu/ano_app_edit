from datetime import date, timedelta
from django import forms


STOCK_CHOICES =('True', 'False')
class BookSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
    
    No = forms.IntegerField(
         label='No', required=False,
         widget=forms.NumberInput(attrs={'placeholder':'10','style':'max-width: 2em' } ),
         help_text='入力数字以上',
         )
    title = forms.CharField(
        label='タイトル', required=False,
        widget=forms.TextInput(attrs={'placeholder':"老人と海", }),
        help_text='入力文字を含む',
        )
    category = forms.CharField(
        label='カテゴリ', required=False,
        widget=forms.TextInput(attrs={'placeholder':'小説', }),
        help_text='入力文字を含め',
        )
    author = forms.CharField(
        label='作者', required=False,
        widget=forms.TextInput(attrs={'placeholder':'ハーミング', }),
        help_text='入力文字を含む'
        )
    published_date = forms.DateField(
        label='出版日付', required=False,
        widget=forms.DateInput(attrs={'placeholder':'2020-11-1', }),
        help_text='入力日付より新しい',
        )
    price = forms.IntegerField(
         label='価格', required=False,
         widget=forms.NumberInput(attrs={'placeholder':'1000', } ),
         help_text='入力数字以上',
         )
    stock = forms.CharField(
        label='在庫', required=False,
        widget=forms.TextInput(attrs={'placeholder':'True', }),
         help_text='TrueかFalse入力',
        )
    
    def clean_No(self):
        No = self.cleaned_data['No']
        if No is not None:
            if 0 <= No and No <= 100000:
                raise forms.ValidationError('10万以下の数字を入力してください。')
        return No
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if title is not None:
            if len(title) > 20:
                raise forms.ValidationError('20文字以下を記入してください。')
        return title
    
    def clean_category(self):
        category = self.cleaned_data['category']
        if category is not None:
            if len(category) > 20:
                raise forms.ValidationError('20文字以下を記入してください。')
        return category
    
    def clean_author(self):
        author = self.cleaned_data['author']
        if author is not None:
            if len(author) > 20:
                raise forms.ValidationError('20文字以下を記入してください。')
        return author
    
    def clean_published_date(self):
        published_date = self.cleaned_data['published_date']
        if published_date is not None:
            if not published_date.strftime('%Y-%m-%d'):
                raise forms.ValidationError('入力形式が正しくありません。yyyy-mm-dd形式で入力してください。')
    
    def clean_price(self):
        price = self.cleaned_data['price']
        if price is not None:
            if 0 <= price and price > 100000:
                raise forms.ValidationError('10万以下の数字を入力してください。')
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock is None :
            raise forms.ValidationError('Checkを入れてください')
        return stock
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        