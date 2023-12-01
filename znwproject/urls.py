"""
URL configuration for znwproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("admin/", admin.site.urls),
    # HOME 暫定です
    # namespace="default" がないとURL namespaceがユニークではないと警告が出てしまう
    path("", include("accounts.urls", namespace="default")),
    # path("", include("anoapp.urls")),
    # wakamatsu test
    path("anoapp/", include("anoapp.urls")),  # その他製品見積システム
    # for testing joonhak
    path("sfa/", include("opportunity.urls")),  # 登録案件一覧
    path("contr/", include("neocontr.urls")),  # 契約一覧
    # Minato
    path("accounts/", include("accounts.urls")),
    # 管理画面_
    path("admin/", admin.site.urls),
]
