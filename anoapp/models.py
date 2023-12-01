from django.db import models

# add
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.contrib.auth.models import Group, Permission

# カスタムユーザーモデル
# class CustomUser(AbstractUser):
#    pass

# 20231004
# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(Group, related_name='custom_user_set')
#     user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')


# 見積書ヘッダモデル
class AnotherQuotationHeader(models.Model):
    id = models.AutoField(primary_key=True)
    # quotation_id = models.CharField(
    #    max_length=255, blank=True, unique=True, verbose_name="見積番号"
    # )
    quotation_id = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="見積番号",
        unique=True,
    )

    quotation_date = models.DateTimeField(auto_now_add=True, verbose_name="見積月日")
    customer_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="顧客名"
    )
    end_user = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="エンドユーザー名"
    )
    quotation_subject = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="見積件名"
    )
    deadline = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="納期"
    )
    delivery_place = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="受渡場所"
    )
    payment_terms = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="支払い条件"
    )
    validity_period = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="見積有効期間(期日)"
    )
    quotation_price = models.DecimalField(
        # default=0,
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="見積金額",
    )
    notices = models.TextField(blank=True, null=True, verbose_name="見積特記事項")
    opportunity_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="オポチュニティID"
    )
    sales_person = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="担当営業"
    )
    lp_sum = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="標準価格合計",
    )
    offer_unit_price_sum = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="提供単価合計",
    )
    offer_price_sum = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="提供価格合計",
    )

    # 基本情報
    create_user = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "another_quotation_header"
        verbose_name = verbose_name_plural = "その他製品_見積書ヘッダ"

    # 関数：一覧画面でデータ複製時に使用
    # 仕様：views.pyのduplicate_quotation関数からコール
    # 用途：AnotherQuotationHeaderのid,quotation_idは現在DBに保存されている最大値から+1する
    #
    #
    #
    def duplicate(self):
        # 01_AnotherQuotationHeaderを複製----START---------------------------------------------
        # 自身(AnotherQuotationHeader)の複製オブジェクトを作成
        dup = self.__class__.objects.get(id=self.id)
        # idをNoneに設定しておく(こうすることで保存時に新しいidが割り当てられる)
        dup.id = None

        # 新しいquotation_idの値を設定(MAX値+1)
        max_quotation_id = self.__class__.objects.aggregate(max_id=Max("quotation_id"))[
            "max_id"
        ]
        dup.quotation_id = max_quotation_id + 1 if max_quotation_id else 1

        # データを保存する(idは自動的にインクリメントされる)
        dup.save()
        # 01_AnotherQuotationHeaderを複製------END-------------------------------------------

        # 02_AnotherQuotationMainを複製----START---------------------------------------------
        for item in self.anotherquotationmain_set.all():
            # 子オブジェクトの複製
            dup_main = item.__class__.objects.get(id=item.id)
            # 親のidを設定
            dup_main.header_id = dup.id
            # idの削除
            dup_main.id = None
            # 親オブジェクトの設定
            dup_main.quotation = dup
            # 子オブジェクトの保存
            dup_main.save()
        # 02_AnotherQuotationMainを複製----END---------------------------------------------

        # 03_AnotherQuotationNotesを複製----START---------------------------------------------
        for item in self.anotherquotationnotes_set.all():
            # 子オブジェクトの複製
            dup_notes = item.__class__.objects.get(id=item.id)
            # 親のidを設定
            dup_notes.header_id = dup.id
            # idの削除
            dup_notes.id = None
            # 親オブジェクトの設定
            dup_notes.quotation = dup
            # 子オブジェクトの保存
            dup_notes.save()
        # 03_AnotherQuotationNotesを複製----END---------------------------------------------

        # 04_AnotherQuotationConfirmを複製----START---------------------------------------------
        for item in self.anotherquotationconfirm_set.all():
            # 子オブジェクトの複製
            dup_confirm = item.__class__.objects.get(id=item.id)
            # 親のidを設定
            dup_confirm.header_id = dup.id
            # idの削除
            dup_confirm.id = None
            # 親オブジェクトの設定
            dup_confirm.quotation = dup
            # 子オブジェクトの保存
            dup_confirm.save()
        # 04_AnotherQuotationConfirmを複製----END---------------------------------------------

        # idの削除
        dup.id = None

        return dup


# 見積書メインモデル
class AnotherQuotationMain(models.Model):
    header = models.ForeignKey(AnotherQuotationHeader, on_delete=models.CASCADE)
    # quotation_id = models.CharField(
    #    max_length=255, blank=True, null=True, verbose_name="見積番号"
    # )
    # 項番
    number = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="項")
    # 品名
    znw_sku_jp = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="品名"
    )
    # 型番
    znw_sku = models.CharField(max_length=255, blank=True, null=True, verbose_name="型番")
    # 数量
    qty = models.PositiveSmallIntegerField(
        default=1, blank=True, null=True, verbose_name="数量"
    )
    # 標準価格
    lp = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="標準価格",
    )
    # 仕切率
    discount_rate = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="仕切率",
    )
    # ご提供単価
    offer_unit_price = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="ご提供単価",
    )
    # ご提供価格
    offer_price = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="ご提供価格",
    )
    # 見積合計
    offer_price_sum = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="見積合計",
    )

    # その他製品独自カラム
    # 原価/台
    unitcost = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="原価/台",
    )
    # 原価*台数
    unitcost_by_number = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="原価*台数",
    )
    # 粗利
    gross_profit = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=0,
        blank=True,
        null=True,
        verbose_name="粗利",
    )
    # 利益率
    profit_rate = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="利益率",
    )

    # 注釈No.
    notes_number = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="注釈No."
    )

    # 基本情報
    create_user = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "another_quotation_main"
        verbose_name = verbose_name_plural = "その他製品_見積書メイン"
        ordering = ["number"]

    # AnotherQuotationMainレコード保存時に
    # 関連するHeaderのoffer_price_sumを更新する
    def update_header_offer_price_sum(self, *args, **kwargs):
        # このMainレコードの関連Headerを取得
        header = self.header

        # このHeaderに関連づく全Mainレコードの
        # offer_priceの合計を計算
        qs = AnotherQuotationMain.objects.filter(header=header)
        sum_offer_price = qs.aggregate(sum=Sum("offer_price"))["sum"] or 0

        # 計算した合計をHeaderのoffer_price_sumに保存
        header.offer_price_sum = sum_offer_price
        header.save()

        # 通常の保存処理
        super().save(*args, **kwargs)


# 見積書注釈モデル
class AnotherQuotationNotes(models.Model):
    header = models.ForeignKey(AnotherQuotationHeader, on_delete=models.CASCADE)
    # quotation_id = models.CharField(
    #    max_length=255, blank=True, null=True, verbose_name="見積番号"
    # )
    number = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="注釈No.   "
    )
    notes = models.TextField(blank=True, null=True, verbose_name="注釈内容")

    # 基本情報
    create_user = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "another_quotation_notes"
        verbose_name = verbose_name_plural = "その他製品_見積書注釈"
        ordering = ["number"]


# その他製品_社内確認欄モデル
class AnotherQuotationConfirm(models.Model):
    header = models.ForeignKey(AnotherQuotationHeader, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name="確認No."
    )
    internal_confirm = models.TextField(blank=True, null=True, verbose_name="社内確認内容")

    # 基本情報
    create_user = models.CharField(max_length=100, blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=100, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = "another_quotation_confirm"
        verbose_name = verbose_name_plural = "その他製品_社内確認欄"
        ordering = ["number"]


####テスト用　後で削除
# テストモデル_見積書ヘッダモデル
class TestAnotherQuotationHeader(models.Model):
    quotation_id = models.CharField(
        max_length=255, blank=True, unique=True, verbose_name="見積番号"
    )
    quotation_date = models.DateTimeField(auto_now_add=True, verbose_name="見積月日")
    customer_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="顧客名"
    )

    class Meta:
        managed = True
        db_table = "test_another_quotation_header"
        verbose_name = verbose_name_plural = "テスト用_その他製品_見積書ヘッダ"


# テストモデル_見積書メインモデル
class TestAnotherQuotationMain(models.Model):
    header = models.ForeignKey(TestAnotherQuotationHeader, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="項")
    znw_sku_jp = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="品名"
    )
    znw_sku = models.CharField(max_length=255, blank=True, null=True, verbose_name="型番")

    class Meta:
        managed = True
        db_table = "test_another_quotation_main"
        verbose_name = verbose_name_plural = "テスト用_その他製品_見積書メイン"
        ordering = ["number"]
