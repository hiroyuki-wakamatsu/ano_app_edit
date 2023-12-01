# Generated by Django 4.2.5 on 2023-10-05 02:07

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AnotherQuotationHeader",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "quotation_id",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default="",
                        max_digits=10,
                        null=True,
                        unique=True,
                        verbose_name="見積番号",
                    ),
                ),
                (
                    "quotation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="見積月日"),
                ),
                (
                    "customer_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="顧客名"
                    ),
                ),
                (
                    "end_user",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="エンドユーザー名"
                    ),
                ),
                (
                    "quotation_subject",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="見積件名"
                    ),
                ),
                (
                    "deadline",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="納期"
                    ),
                ),
                (
                    "delivery_place",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="受渡場所"
                    ),
                ),
                (
                    "payment_terms",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="支払い条件"
                    ),
                ),
                (
                    "validity_period",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="見積有効期間(期日)"
                    ),
                ),
                (
                    "quotation_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        max_digits=10,
                        null=True,
                        verbose_name="見積金額",
                    ),
                ),
                (
                    "notices",
                    models.TextField(blank=True, null=True, verbose_name="見積特記事項"),
                ),
                (
                    "opportunity_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="オポチュニティID"
                    ),
                ),
                (
                    "sales_person",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="担当営業"
                    ),
                ),
                (
                    "lp_sum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="標準価格合計",
                    ),
                ),
                (
                    "offer_unit_price_sum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="提供単価合計",
                    ),
                ),
                (
                    "offer_price_sum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="提供価格合計",
                    ),
                ),
                (
                    "create_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "update_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "その他製品_見積書ヘッダ",
                "verbose_name_plural": "その他製品_見積書ヘッダ",
                "db_table": "another_quotation_header",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TestAnotherQuotationHeader",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quotation_id",
                    models.CharField(
                        blank=True, max_length=255, unique=True, verbose_name="見積番号"
                    ),
                ),
                (
                    "quotation_date",
                    models.DateTimeField(auto_now_add=True, verbose_name="見積月日"),
                ),
                (
                    "customer_id",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="顧客名"
                    ),
                ),
            ],
            options={
                "verbose_name": "テスト用_その他製品_見積書ヘッダ",
                "verbose_name_plural": "テスト用_その他製品_見積書ヘッダ",
                "db_table": "test_another_quotation_header",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="TestAnotherQuotationMain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="項"
                    ),
                ),
                (
                    "znw_sku_jp",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="品名"
                    ),
                ),
                (
                    "znw_sku",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="型番"
                    ),
                ),
                (
                    "header",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="anoapp.testanotherquotationheader",
                    ),
                ),
            ],
            options={
                "verbose_name": "テスト用_その他製品_見積書メイン",
                "verbose_name_plural": "テスト用_その他製品_見積書メイン",
                "db_table": "test_another_quotation_main",
                "ordering": ["number"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="AnotherQuotationNotes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="注釈No.   "
                    ),
                ),
                ("notes", models.TextField(blank=True, null=True, verbose_name="注釈内容")),
                (
                    "create_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "update_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "header",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="anoapp.anotherquotationheader",
                    ),
                ),
            ],
            options={
                "verbose_name": "その他製品_見積書注釈",
                "verbose_name_plural": "その他製品_見積書注釈",
                "db_table": "another_quotation_notes",
                "ordering": ["number"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="AnotherQuotationMain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="項"
                    ),
                ),
                (
                    "znw_sku_jp",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="品名"
                    ),
                ),
                (
                    "znw_sku",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="型番"
                    ),
                ),
                (
                    "qty",
                    models.PositiveSmallIntegerField(
                        blank=True, default=1, null=True, verbose_name="数量"
                    ),
                ),
                (
                    "lp",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="標準価格",
                    ),
                ),
                (
                    "discount_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="仕切率",
                    ),
                ),
                (
                    "offer_unit_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="ご提供単価",
                    ),
                ),
                (
                    "offer_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="ご提供価格",
                    ),
                ),
                (
                    "offer_price_sum",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="見積合計",
                    ),
                ),
                (
                    "unitcost",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="原価/台",
                    ),
                ),
                (
                    "unitcost_by_number",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="原価*台数",
                    ),
                ),
                (
                    "gross_profit",
                    models.DecimalField(
                        blank=True,
                        decimal_places=0,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="粗利",
                    ),
                ),
                (
                    "profit_rate",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=0,
                        max_digits=100,
                        null=True,
                        verbose_name="利益率",
                    ),
                ),
                (
                    "notes_number",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="注釈No."
                    ),
                ),
                (
                    "create_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "update_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "header",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="anoapp.anotherquotationheader",
                    ),
                ),
            ],
            options={
                "verbose_name": "その他製品_見積書メイン",
                "verbose_name_plural": "その他製品_見積書メイン",
                "db_table": "another_quotation_main",
                "ordering": ["number"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="AnotherQuotationConfirm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "number",
                    models.PositiveSmallIntegerField(
                        blank=True, null=True, verbose_name="確認No."
                    ),
                ),
                (
                    "internal_confirm",
                    models.TextField(blank=True, null=True, verbose_name="社内確認内容"),
                ),
                (
                    "create_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "update_user",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("is_deleted", models.BooleanField(default=False)),
                (
                    "header",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="anoapp.anotherquotationheader",
                    ),
                ),
            ],
            options={
                "verbose_name": "その他製品_社内確認欄",
                "verbose_name_plural": "その他製品_社内確認欄",
                "db_table": "another_quotation_confirm",
                "ordering": ["number"],
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="custom_user_set", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="custom_user_set", to="auth.permission"
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
