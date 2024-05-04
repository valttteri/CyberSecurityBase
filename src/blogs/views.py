from django.shortcuts import render, redirect
from .models import Blog

def frontPageView(request):
    """Render the front page of the application"""

    blogs = Blog.objects.all()

    return render(request, 'frontpage.html', {'blogs' : blogs})

def createBlogView(request):
    """Create a new blog"""

    if request.method == 'POST':
        blog_content = request.POST.get('content', '').strip()
        blog_title = request.POST.get('title', '').strip()
        if 1000 > len(blog_content) > 0:
            Blog.objects.create(
                title=blog_title,
                content=blog_content
            )

    return redirect('/')

def flushBlogsView(request):
    """Remove all blogs"""

    if request.method == 'POST':
        Blog.objects.all().delete()

    return redirect('/')
