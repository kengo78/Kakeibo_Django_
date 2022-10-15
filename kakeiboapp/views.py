from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy

from .forms import SignUpForm

class IndexView(TemplateView):
    template_name = "kakeiboapp/index.html"
    
class HomeView(TemplateView):
    template_name = "kakeiboapp/home.html"
    
class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "kakeiboapp/signup.html"
    success_url = reverse_lazy("kakeiboapp:home")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())