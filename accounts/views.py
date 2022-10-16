from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
# Create your views here.
from .forms import SignUpForm

    
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