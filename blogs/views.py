from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Category, Comment
from django.db.models import Q

# Create your views here.

# def page_not_found(request):
#     return render(request, '404.html')

def posts_by_category(request, category_id) :

    # print(f'{request=}')
    posts = Blog.objects.filter(status = 'Published', category = category_id)
    # category = Category.objects.get(pk=category_id)
    try :
        category = Category.objects.get(pk=category_id)
    except :
        return redirect('home')    
    # if category does not exist show 404 page for this use "get_object_or_404(table, condition/expression)"
    # category = get_object_or_404(Category, pk=category_id)

    # print(posts)
    context = {
        'category' : category,
        'posts' : posts,
    }
    # return HttpResponse(context)
    return render(request, 'posts_by_category.html', context)


def blogs(request, slug) :
    try :
        blog = Blog.objects.get(slug=slug)
    except :
        blog = None
    print(blog)
    print(f"{request.user=}")
    if request.method == 'POST' :
        if request.user != None :
            comments = Comment()
            comments.user = request.user
            comments.blog = blog
            comments.comment = request.POST['comment']
            comments.save()
            return HttpResponseRedirect(request.path_info)
        else :
            return redirect('login')
    comments = Comment.objects.filter(blog=blog)
    comments_count = comments.count()
    print(f"{comments=}")
    context = {
        'blog' : blog,
        'comments' : comments,
        'comments_count' : comments_count,
    }
    return render(request, 'blogs.html', context)

def search(request) :
    keyword = request.GET.get('keyword')
    print(f"{keyword=}")
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(blog_body__icontains=keyword) | Q(author__username__icontains=keyword), status='Published')
    print(f"{blogs=}")
    context = {
        'blogs' : blogs,
        'keyword' : keyword,
    }
    return render(request, 'search.html', context)