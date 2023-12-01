from django.forms import ModelForm
#from betterforms.multiform import MultiModelForm
from django.forms import formset_factory, inlineformset_factory
from django import forms
from django.utils.safestring import mark_safe


from .models import (
    AnotherQuotationHeader,
    AnotherQuotationMain,
    AnotherQuotationNotes,
    AnotherQuotationConfirm,
)

# その他製品_ヘッダー情報
class AnotherHeaderForm(ModelForm):
    # customer_id = forms.CharField(required=True)
    # quotation_subject = forms.CharField(required=True)
    # deadline = forms.DateField(required=True)
    # delivery_place = forms.CharField(required=True)
    # payment_terms = forms.CharField(required=True)
    # validity_period = forms.DateField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnotherQuotationHeader
        # fields = "__all__"
        fields = [
            "id",
            "quotation_id",
            "customer_id",
            "end_user",
            "quotation_subject",
            "deadline",
            "delivery_place",
            "payment_terms",
            "validity_period",
            "quotation_price",
            "notices",
            "opportunity_id",
            "sales_person",
            "lp_sum",
            "offer_unit_price_sum",
            "offer_price_sum",
            "create_user",
            "update_user",
            "is_deleted",
        ]


# その他製品_製品情報
class AnotherMainForm(ModelForm):

    # 製品情報のフォームサイズをここで設定
    # 価格：120px、数量及び番号：50px
    #

    # 項番のフォームサイズ設定
    number = forms.CharField(
        label="No.",
        widget=forms.TextInput(attrs={"style": "width: 60px;"}),
    )

    # 品名のフォームサイズ設定
    znw_sku_jp = forms.CharField(
        label="品名",
        widget=forms.TextInput(attrs={"style": "width: 500px;"}),
    )

    # 型番のフォームサイズ設定
    znw_sku = forms.CharField(
        label="型番",
        widget=forms.TextInput(attrs={"style": "width: 250px;"}),
    )

    # 数量のフォームサイズ設定
    qty = forms.CharField(
        label="数量",
        widget=forms.TextInput(attrs={"style": "width: 50px;"}),
    )

    # 標準価格のフォームサイズ設定
    lp = forms.CharField(
        label="標準価格(￥)",
        widget=forms.TextInput(attrs={"style": "width: 120px;"}),
    )

    # 仕切率のフォームサイズ設定
    discount_rate = forms.CharField(
        label="仕切率(%)",
        widget=forms.TextInput(attrs={"style": "width: 80px;"}),
    )
    # 提供単価のフォームサイズ設定
    offer_unit_price = forms.CharField(
        label="ご提供単価(￥)",
        # 入力不可、背景色を変更
        widget=forms.TextInput(
            attrs={
                "style": "width: 120px; background-color:lightgray ;",
                "readonly": True,
            }
        ),
    )

    # 提供価格のフォームサイズ設定
    offer_price = forms.CharField(
        label="ご提供価格(￥)",
        widget=forms.TextInput(
            attrs={
                "style": "width: 120px; background-color:lightgray ;",
                "readonly": True,
            }
        ),
    )
    # 原価/台のフォームサイズ設定
    unitcost = forms.CharField(
        label="原価/台(￥)",
        widget=forms.TextInput(attrs={"style": "width: 120px;"}),
    )
    # 原価*台数のフォームサイズ設定
    unitcost_by_number = forms.CharField(
        label="原価*台数(￥)",
        # 入力不可、背景色を変更
        widget=forms.TextInput(
            attrs={
                "style": "width: 120px; background-color:lightgray ;",
                "readonly": True,
            }
        ),
    )
    # 粗利のフォームサイズ設定
    gross_profit = forms.CharField(
        label="粗利(￥)",
        widget=forms.TextInput(
            attrs={
                "style": "width: 120px; background-color:lightgray ;",
                "readonly": True,
            }
        ),
    )
    # 利益率のフォームサイズ設定
    profit_rate = forms.CharField(
        label="利益率(%)",
        widget=forms.TextInput(
            attrs={
                "style": "width: 80px; background-color:lightgray ;",
                "readonly": True,
            }
        ),
    )
    # notes_numbermのフォームサイズ設定
    # 注釈は必須入力にしない
    notes_number = forms.CharField(
        label="注釈No.",
        widget=forms.TextInput(attrs={"style": "width: 80px;"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnotherQuotationMain
        exclude = (
            "header",
            "id",
            "create_user",
            "update_user",
            "is_deleted",
            "offer_price_sum",
        )


# その他製品_注釈情報
class AnotherNotesForm(ModelForm):

    # 項番のフォームサイズ設定
    number = forms.CharField(
        label="注釈No.",
        widget=forms.TextInput(attrs={"style": "width: 60px;"}),
    )

    # 注釈内容のフォームサイズ設定
    notes = forms.CharField(
        label="注釈本文",
        widget=forms.Textarea(attrs={"rows": 3, "style": "width: 1600px;"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnotherQuotationNotes
        exclude = ("header", "id", "create_user", "update_user", "is_deleted")


# その他製品_社内確認情報
class AnotherConfirmForm(ModelForm):

    # 項番のフォームサイズ設定
    number = forms.CharField(
        label="確認No.",
        widget=forms.TextInput(attrs={"style": "width: 60px;"}),
    )

    # 社内確認欄内容のフォームサイズ設定
    internal_confirm = forms.CharField(
        label="社内確認情報本文",
        widget=forms.Textarea(attrs={"rows": 3, "style": "width: 1600px;"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = AnotherQuotationConfirm
        exclude = ("header", "id", "create_user", "update_user", "is_deleted")
        # fields = "__all__"


# 製品情報のフォームセット
AnotherMainFormSet = inlineformset_factory(
    AnotherQuotationHeader,
    AnotherQuotationMain,
    form=AnotherMainForm,
    extra=0,
    can_delete=True,
)


# 注釈情報のフォームセット
AnotherNotesFormSet = inlineformset_factory(
    AnotherQuotationHeader,
    AnotherQuotationNotes,
    form=AnotherNotesForm,
    extra=0,
    can_delete=True,
)

# 社内確認情報のフォームセット
AnotherConfirmFormSet = inlineformset_factory(
    AnotherQuotationHeader,
    AnotherQuotationConfirm,
    form=AnotherConfirmForm,
    extra=0,
    can_delete=True,
)
