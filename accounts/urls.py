from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('home/', views.HomeView.as_view(), name="home"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
]