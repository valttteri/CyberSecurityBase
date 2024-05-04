from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Blog

@login_required
def frontPageView(request):
    """Render the front page of the application"""

    blogs = Blog.objects.filter(Q(author=request.user))

    return render(request, 'frontpage.html', {'blogs' : blogs, 'user' : request.user})

def createBlogView(request):
    """Create a new blog"""

    if request.method == 'POST':
        blog_content = request.POST.get('content', '').strip()
        blog_title = request.POST.get('title', '').strip()
        if 1000 > len(blog_content) > 0:
            Blog.objects.create(
                title=blog_title,
                content=blog_content,
                author=request.user
            )

    return redirect('/')

def flushBlogsView(request):
    """Remove all blogs"""

    if request.method == 'POST':
        Blog.objects.all().delete()

    return redirect('/')

def loginView(request):
    """Render the login form"""
    
    return render(request, 'loginpage.html')

def logoutView(request):
    """Logout a user"""

    logout(request)

    return redirect('/login')

def createAccountView(request):
    """Render account creation form"""

    return render(request, 'registerpage.html')

def attemptedLoginView(request):
    """Check if a login attempt is valid"""
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')

    return redirect('/login')

def saveNewUserView(request):
    """Save a new user to the database"""
    username = request.POST["username"]
    password = request.POST["password"]

    User.objects.create_user(
        username=username,
        password=password
    )

    return redirect('/')

def deleteUserView(request, pk):
    """Delete a user"""

    remove_this_user = User.objects.get(id=pk)
    print(remove_this_user)
    remove_this_user.delete()

    return redirect('/')