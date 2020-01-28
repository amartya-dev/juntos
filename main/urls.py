from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = "main"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('add_news/', views.add_news, name='add_news'),
    path('', views.base_check,name='base_check'),
]