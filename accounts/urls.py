from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include
from .views import CustomLoginView

app_name = "accounts"

urlpatterns = [
    path("home/", views.home, name="home"),
    # 以下はadminのログアウトになる
    # path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # 現状このログアウトをしても、再度ログイン不要でhomeに入れてしまう
    # path(
    #     "",
    #     views.CustomLogoutView.as_view(template_name="accounts/login.html"),
    #     name="logout",
    # ),
    # path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("logout/", views.logout, name="logout"),
    # path("", views.CustomLoginView.as_view(), name="login"),
    path("", views.CustomLoginView.as_view(), name="login"),
    # path("", views.login, name="login"),
    # Minatotest
    path("navbase/", views.navbase, name="navbase"),
]
