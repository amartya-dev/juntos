from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "main"
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('organizations/', views.organizations, name='organizations'),
    path('events/', views.events_list, name='events_list'),
    path('add_events/', views.add_event, name='add_events'),
    path('news/', views.news_list, name='news_list'),
    path('volunteers/', views.volunteers_list, name='volunteers_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('add_news/', views.add_news, name='add_news'),
    path('ambassador/', views.ambassador, name='ambassador'),
    path('spread/', views.spreads, name='spread'),
    path('job/', views.jobs, name='job'),
    path('<slug:slug>/', views.organization_details, name='organization'),
]
