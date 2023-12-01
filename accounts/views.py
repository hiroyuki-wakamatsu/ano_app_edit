from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm


# Create your views here.

def navbase(request):
    return render(request, "accounts/navbase.html")

# def newIn(request):
#    return render(request, "accounts/newlogin.html")
  
# class CustomLoginView(LoginView):
#     """ログインページ"""

#     template_name = "accounts/login.html"
#     #form_class = CustomAuthenticationForm
#     #template_name = "accounts/newlogin.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         return context

# new LoginView
class CustomLoginView(LoginView):
    """ログインページ"""
    form_class = CustomAuthenticationForm
    template_name = "accounts/newlogin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# class CustomLogoutView(LoginRequiredMixin, LogoutView):
#     # next_page = "accounts/login.html"  # この部分でリダイレクト先を設定します
#     # template_name = "accounts/login.html"
#     # next_page = "login" あってもなくても変わらない
#     success_url = reverse_lazy("login")

#     def dispatch(self, request, *args, **kwargs):
#         request.session.flush()  # セッションをフラッシュ
#         return super().dispatch(request, *args, **kwargs)

def logout(request):
  request.session.flush()  # セッションをフラッシュ
  return redirect(reverse_lazy(settings.LOGOUT_REDIRECT_URL)) #reverse_lazyはURLの逆引きを遅延評価するために使用される関数
  
# def login(request):
#   return redirect(reverse_lazy(settings.LOGIN_URL))
# def login(request):
#   return render(request, "accounts/login.html")

@login_required
def home(request):
    return render(request, "accounts/home.html")
  
