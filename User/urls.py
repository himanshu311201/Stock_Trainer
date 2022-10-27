from atexit import register
import imp
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from User.views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',register,name='register'),
    path('subscribe/',subscribe,name='subscribe'),
    path('create-blogs/',PostCreate.as_view(template_name='User/blog.html'),name="create-blog"),
    path('login/',auth_views.LoginView.as_view(template_name='User/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='User/logout.html'),name='logout'),
    path('blogs/',blog_list,name='blog_list'),
    path('upvote/',upvote.as_view(),name='upvote'),
    path('profile/<user>',profile,name='profile'),
    path('addSubscriber/',addSubscriber,name='addSubscriber'),
]