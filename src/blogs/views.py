from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from datetime import datetime
from string import ascii_uppercase, ascii_lowercase, punctuation
from .models import Blog, AppUser, LogEntry

@login_required
def frontPageView(request):
    """Render the front page of the application"""

    blogs = Blog.objects.filter(Q(author=request.user))
    blogs = blogs.order_by("-id").values()

    return render(
        request,
        "frontpage.html",
        {"blogs" : blogs, "user" : request.user}
    )

@login_required
def createBlogView(request):
    """Create a new blog"""

    if request.method == "POST":
        blog_content = request.POST.get("content", "").strip()
        blog_title = request.POST.get("title", "").strip()
        if (
            0 < len(blog_content) < 1000
            and 0 < len(blog_title) < 30
        ):
            Blog.objects.create(
                title=blog_title,
                content=blog_content,
                author=request.user
            )

            messages.success(request, "Blog saved successfully!")
        else:
            messages.error(request, "Limits: title < 30 characters, content < 1000 characters")

    return redirect("/")

@login_required
def flushBlogsView(request):
    """Remove all blogs of the logged user"""

    if request.method == "POST":
        blogs_to_delete = Blog.objects.filter(Q(author=request.user))
        blogs_to_delete.delete()

    return redirect("/")

def loginView(request):
    """Render the login form"""
    
    return render(request, "loginpage.html")

def logoutView(request):
    """Logout a user"""

    logout(request)
    messages.success(request, "Logout successful!")

    return redirect("/login")

def createAccountView(request):
    """Render account creation form"""

    return render(request, "registerpage.html")

def attemptedLoginView(request):
    """
    Check if a login attempt is valid. This login system does not support hashed passwords
    and must be fixed.
    """
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        # No password hashing available (FLAW 2)
        # Fix (1/4): Modify the login system to support hashed passwords

        #user = AppUser.objects.get(username=username) # uncomment
        user = AppUser.objects.get(username=username, password=password) # comment out
    except ObjectDoesNotExist:
        messages.error(request, "Invalid credentials")
        return redirect("/login")

    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    # No password hashing available (FLAW 2)
    # Fix (2/4):
    # The login system will now compare the raw password received as input
    # to the hashed password found in the database with the check_password() method.

    if user is not None: # comment out
    #if user.check_password(password): # uncomment
        login(request, user)
        messages.success(request, "Login successful!")

        # No security logging or monitoring available (FLAW 5)
        # Fix by adding a logging system that will create a new entry for each login attempt. 
        # Uncomment the following code

        """
        LogEntry.objects.create(
            name = "Login attempt",
            data = {
                "username": username,
                "password": password,
                "isValid": True
            },
            time = timestamp
        )
        """        

        return redirect("/")
    
    messages.error(request, "Invalid credentials")

    # No security logging or monitoring available (FLAW 5)
    # Fix by adding a logging system that will create a new entry for each login attempt.
    # Uncomment the following code

    """
    LogEntry.objects.create(
        name = "Login attempt",
        data = {
            "username": username,
            "password": password,
            "isValid": False
        },
        time = timestamp
    )
    """

    return redirect("/login")

def saveNewUserView(request):
    """Save a new user to the database"""
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    secret = request.POST["secret"]

    if len(username) < 5:
        messages.error(request, "Enter a valid username")
        return redirect("createaccount")
    
    # No password validation when creating an account (FLAW 4)
    # Fix by enabling password validation
    # Comment out the following block of code

    messages.success(request, "Account created successfully!")
    AppUser.objects.create_user(
        username=username,
        password=password,
        email=email,
        secret=secret
    )
    return redirect("/")

    # Comment out the code above & uncomment the code below (FLAW 4)

    """
    if password_isvalid(password):
        messages.success(request, "Account created successfully!")
        AppUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            secret=secret
        )
        return redirect("/")

    messages.error(
        request,
        "Password must be at least 8 characters long and\n"
        "contain uppercase, lowercase and special characters"
    )
    
    return redirect("createaccount")

    """

def password_isvalid(password: str):
    """
    Custom password validator
    """
    has_uppercase = False
    has_lowercase = False
    has_special_char = False

    if len(password) < 8:
        return False

    for char in password:
        if char in ascii_uppercase:
            has_uppercase = True
        if char in ascii_lowercase:
            has_lowercase = True
        if char in punctuation:
            has_special_char = True

    if (
        not has_uppercase
        or not has_lowercase
        or not has_special_char
    ):
        return False
    return True

@login_required
def deleteUserView(request, pk):
    """Delete a user"""

    remove_this_user = AppUser.objects.get(id=pk)

    # Anyone can delete other users' accounts (FLAW 1)
    # Fix by confirming the identity of the user attempting to delete an account
       
    #if request.user != remove_this_user:
    #    return redirect('/')

    remove_this_user.delete()

    messages.success(request, "Account deleted successfully!")

    return redirect("/")

@login_required
def ownPageView(request, pk):
    """Render the user"s own information"""

    log_entries = LogEntry.objects.all()
    log_entries = log_entries.order_by("-id").values()

    try:
        user_to_observe = AppUser.objects.get(id=pk)
    except ObjectDoesNotExist:
        return redirect("/")
    
    # Anyone can view other users' profiles (FLAW 1)
    # Fix by confirming the identity of the user attempting view a prfile

    #if request.user != user_to_observe:
    #    return redirect("/")

    return render(request, "ownpage.html", { "user" : user_to_observe, "log_entries" : log_entries  })
