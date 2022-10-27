from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
from .forms import LoginForm, SignUpForm

    
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
        