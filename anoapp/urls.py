from django.urls import path
from . import views

from django.contrib import admin


urlpatterns = [
    # ◆Class BaseView
    # 0_admin用
    # path("admin/", admin.site.urls),
    # 1_anoappアプリのルートページ。(プロジェクトのurls.pyにて”anoapp”をアプリのルートページに設定している為!!)
    # （EX. http://127.0.0.1/anoapp/）
    path("", views.QuotationListlView.as_view(), name="list-page"),
    # 2_見積書新規作成画面（EX. http://127.0.0.1/anoapp/create/）
    path("create/", views.HeaderCreateView.as_view(), name="header_main_create"),
    # 3_見積書編集画面（EX. http://127.0.0.1/anoapp/update/1）
    path(
        "update/<int:pk>",
        views.HeaderUpdateView.as_view(),
        name="header_main_update",
    ),
    # 4_見積書削除画面（EX. http://127.0.0.1/anoapp/delete/1）
    path(
        "delete/<int:pk>", views.HeaderDeleteView.as_view(), name="header_main_delete"
    ),
    # ◆function BaseView
    #
    # 1_見積書検索結果画面
    path("quotation_list/", views.quotation_list, name="quotation_list"),
    # 2_見積書複製画面（EX. http://127.0.0.1/anoapp/duplicate/1）
    path("duplicate/<int:id>", views.duplicate_quotation, name="duplicate"),
    # path("duplicate/<int:pk>", views.duplicate_quotation, name="duplicate"),
    # 3_見積書PDFプレビュー画面
    path("pdf_preview/<int:pk>", views.pdf_preview_view, name="pdf_preview"),
]
