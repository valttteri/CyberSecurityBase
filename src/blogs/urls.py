# views for the blogs app here

from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontPageView, name='frontpage'), # the frontpage
    path('login', views.loginView, name='login'), # login page
    path('logout', views.logoutView, name='logout'), # logout a user
    path('checklogin', views.attemptedLoginView, name='attempted login'), # check credentials
    path('createaccount', views.createAccountView, name='createaccount'), # register page
    path('saveuser', views.saveNewUserView, name='savenewuser'), # save a new user
    path('ownpage/<int:pk>', views.ownPageView, name='ownpage'), # user's information
    path('deleteuser/<int:pk>', views.deleteUserView, name='deleteuser'), # delete a user
    path('createblog', views.createBlogView, name='createblogs'), # save a new blog
    path('flushblogs', views.flushBlogsView, name='flushblogs') # delete all blogs
]