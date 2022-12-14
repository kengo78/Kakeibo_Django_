from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    # path('home/', views.HomeView.as_view(), name="home"),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('login/', views.Login.as_view(), name="login"),
    path('logout', views.Logout.as_view(), name='logout'),
    path('mypage/<int:pk>/', views.MyPage.as_view(), name='my_page'),
]