from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from .models import Blog, AppUser, LogEntry

@login_required
def frontPageView(request):
    """Render the front page of the application"""

    # Get all blogs by the logged user
    blogs = Blog.objects.filter(Q(author=request.user))
    blogs = blogs.order_by('-id').values()

    return render(
        request,
        'frontpage.html',
        {'blogs' : blogs, 'user' : request.user}
    )

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
    user = AppUser.objects.get(username=username)

    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # if user is not None:
    # user = AppUser.objects.get(username=username, password=password)
    if user.check_password(password):
        login(request, user)

        # log important events (5)
        LogEntry.objects.create(
            name = "Login attempt",
            data = {
                "username": username,
                "password": password,
                "isValid": True
            },
            time = timestamp
        )

        return redirect('/')
    
    LogEntry.objects.create(
        name = "Login attempt",
        data = {
            "username": username,
            "password": password,
            "isValid": False
        },
        time = timestamp
    )

    return redirect('/login')

def saveNewUserView(request):
    """Save a new user to the database"""
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    secret = request.POST["secret"]

    AppUser.objects.create_user(
        username=username,
        password=password,
        email=email,
        secret=secret
    )

    return redirect('/')

def deleteUserView(request, pk):
    """Delete a user"""

    remove_this_user = AppUser.objects.get(id=pk)
    remove_this_user.delete()

    return redirect('/')

def ownPageView(request, pk):
    """Render the user's own information"""

    log_entries = LogEntry.objects.all()

    try:
        user_to_observe = AppUser.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect('/')

    return render(request, 'ownpage.html', { 'user' : user_to_observe, 'log_entries' : log_entries  })
