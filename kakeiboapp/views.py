from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login
from django.urls import reverse_lazy



class IndexView(TemplateView):
    template_name = "kakeiboapp/index.html"
