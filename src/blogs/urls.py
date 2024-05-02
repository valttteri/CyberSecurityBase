# views for the blogs app here

from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontPageView, name='frontpage'),
    path('createblog', views.createBlogView, name='createblogs'),
    path('flushblogs', views.flushBlogsView, name='flushblogs')
]