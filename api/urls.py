"""
URL configuration for make_notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from api.views import *

urlpatterns = [
    path('auth/signup', register, name='register'),
    path('auth/login/', auth_views.LoginView.as_view(template_name='api/login.html'), name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(template_name='api/logout.html'), name='logout'),
    path('profile/', profile, name='profile'),
    path('notes/', PostListView.as_view(), name='notes-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('note/<int:pk>/', PostDetailView.as_view(), name='note-detail'),
    path('note/new/', PostCreateView.as_view(), name='note-create'),
    path('note/<int:pk>/update/', PostUpdateView.as_view(), name='note-update'),
    path('note/<int:pk>/delete/', PostDeleteView.as_view(), name='note-delete'),
    path('search/', search_notes, name='search'),
    path('search2/<str:username>', PostSearch.as_view(template_name='api/search.html'), name='search2'),

]
