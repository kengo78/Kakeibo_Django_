from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.
from .forms import LoginForm, SignUpForm
from django.contrib.auth import get_user_model
from .models import *


    
class HomeView(TemplateView):
    template_name = "accounts/home.html"
    
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
    
class Login(LoginView):
    form_class=LoginForm
    template_name = 'accounts/login.html'
    
class Logout(LogoutView):
    template_name = 'accounts/logout.html'
    
# def login(request):
#     if request.method=="POST":
#         email = request.POST.get('email')
#         form = LoginForm(request, data=request.POST)
        
#         # if form.is_valid():
#             # user = 
        
# '''自分しかアクセスできないようにするMixin(My Pageのため)'''
class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        # 今ログインしてるユーザーのpkと、そのマイページのpkが同じなら許可
        user = self.request.user
        return user.pk == self.kwargs['pk']


'''マイページ'''
class MyPage(OnlyYouMixin, DetailView):
    model = User
    template_name = 'accounts/my_page.html'
    # モデル名小文字(user)でモデルインスタンスがテンプレートファイルに渡される