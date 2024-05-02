from django.shortcuts import render, redirect

def frontPageView(request):
    """Render the front page of the application"""
    blogs = request.session.get('blogs', [])

    return render(request, 'frontpage.html', {'blogs' : blogs})

def createBlogView(request):
    """Create a new blog"""
    blogs = request.session.get('blogs', [])

    if request.method == 'POST':
        new_blog = request.POST.get('content', '').strip()
        if 1000 > len(new_blog) > 0:
            blogs.append(new_blog)

    request.session['blogs'] = blogs

    return redirect('/')

def flushBlogsView(request):
    """Remove all blogs"""

    if request.method == 'POST':
        request.session['blogs'] = []

    return redirect('/')
