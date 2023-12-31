# Generated by Django 4.2.5 on 2023-10-05 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ZnwMasterDept",
            fields=[
                (
                    "dept_cd",
                    models.CharField(
                        max_length=16,
                        primary_key=True,
                        serialize=False,
                        verbose_name="部門コード",
                    ),
                ),
                ("dept_name", models.CharField(max_length=100, verbose_name="部門名")),
                (
                    "manager_employee_no",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="部門責任者社員番号"
                    ),
                ),
                (
                    "parent_id",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="上位部門コード"
                    ),
                ),
                (
                    "dept_name_short",
                    models.CharField(
                        blank=True, max_length=3, null=True, verbose_name="部門名１文字"
                    ),
                ),
                ("create_user", models.CharField(max_length=100, verbose_name="作成者")),
                ("create_date", models.DateTimeField(verbose_name="作成日")),
                ("update_user", models.CharField(max_length=100, verbose_name="更新者")),
                ("update_date", models.DateTimeField(verbose_name="更新日")),
                ("is_deleted", models.IntegerField(default=0, verbose_name="削除フラグ")),
            ],
            options={
                "verbose_name": "新見積システム 部門マスター",
                "verbose_name_plural": "新見積システム 部門マスター",
                "db_table": "znw_master_dept",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="ZnwQuotationNumbering",
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
                ("employee_no", models.CharField(max_length=16, verbose_name="社員番号")),
                ("quotation_num_date", models.DateField(verbose_name="見積番号基準日")),
                ("quotation_num", models.IntegerField(verbose_name="日毎の見積番号現状の最大値")),
                ("create_user", models.CharField(max_length=100, verbose_name="作成者")),
                ("create_date", models.DateTimeField(verbose_name="作成日")),
                ("update_user", models.CharField(max_length=100, verbose_name="更新者")),
                ("update_date", models.DateTimeField(verbose_name="更新日")),
                ("is_deleted", models.IntegerField(default=0, verbose_name="削除フラグ")),
            ],
            options={
                "verbose_name": "見積番号採番情報",
                "verbose_name_plural": "見積番号採番情報",
                "db_table": "znw_quotation_numbering",
                "managed": True,
                "unique_together": {("employee_no", "quotation_num_date")},
            },
        ),
        migrations.CreateModel(
            name="ZnwMasterEmployee",
            fields=[
                (
                    "employee_no",
                    models.CharField(
                        max_length=16,
                        primary_key=True,
                        serialize=False,
                        verbose_name="社員番号",
                    ),
                ),
                (
                    "employee_name",
                    models.CharField(max_length=100, verbose_name="社員氏名"),
                ),
                (
                    "position",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="役職"
                    ),
                ),
                (
                    "superior_employee_no",
                    models.CharField(
                        blank=True, max_length=16, null=True, verbose_name="上長社員番号"
                    ),
                ),
                (
                    "skip_approver_no",
                    models.CharField(
                        blank=True,
                        max_length=16,
                        null=True,
                        verbose_name="承認スキップ時の承認社員番号",
                    ),
                ),
                (
                    "irregular_approval_flow_flag",
                    models.BooleanField(default=False, verbose_name="承認フロースキップフラグ"),
                ),
                ("create_user", models.CharField(max_length=100, verbose_name="作成者")),
                ("create_date", models.DateTimeField(verbose_name="作成日")),
                ("update_user", models.CharField(max_length=100, verbose_name="更新者")),
                ("update_date", models.DateTimeField(verbose_name="更新日")),
                ("is_deleted", models.IntegerField(default=0, verbose_name="削除フラグ")),
                (
                    "dept",
                    models.ForeignKey(
                        blank=True,
                        db_column="dept_cd",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="commonapp.znwmasterdept",
                        verbose_name="部門コード",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "新見積システム 社員マスター",
                "verbose_name_plural": "新見積システム 社員マスター",
                "db_table": "znw_master_employee",
                "managed": True,
            },
        ),
    ]
