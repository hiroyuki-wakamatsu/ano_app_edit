from django.contrib import admin

from .models import (
    AnotherQuotationHeader,
    AnotherQuotationMain,
    AnotherQuotationNotes,
    AnotherQuotationConfirm,
    TestAnotherQuotationHeader,
    TestAnotherQuotationMain,
)

# Register your models here.
# 管理画面で編集するテーブルを追加
admin.site.register(AnotherQuotationHeader)
admin.site.register(AnotherQuotationMain)
admin.site.register(AnotherQuotationNotes)
admin.site.register(AnotherQuotationConfirm)

# テスト用
admin.site.register(TestAnotherQuotationHeader)
admin.site.register(TestAnotherQuotationMain)
