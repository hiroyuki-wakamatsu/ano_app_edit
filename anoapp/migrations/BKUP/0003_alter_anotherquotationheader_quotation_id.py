# Generated by Django 4.2.5 on 2023-10-10 05:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("anoapp", "0002_delete_customuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anotherquotationheader",
            name="quotation_id",
            field=models.PositiveIntegerField(
                default=None, unique=True, verbose_name="見積番号"
            ),
        ),
    ]