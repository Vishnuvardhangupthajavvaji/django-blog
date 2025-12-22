# from django.http import HttpResponse
from django.shortcuts import render

from blogs.models import Category, Blog


def home(request) :
    categories = Category.objects.all()
    featured_posts = Blog.objects.filter(is_featured = True).order_by('-updated_at')
    # print(featured_posts)
    posts = Blog.objects.filter(is_featured = False, status='Published')
    context = {
        'categories' : categories,
        'featured_posts' : featured_posts,
        'posts' : posts, 
    }
    # for post in featured_posts :
    #     print(type(post.created_at))
    # return HttpResponse("<h2>this is home page</h2>")
    return render(request, "home.html", context)