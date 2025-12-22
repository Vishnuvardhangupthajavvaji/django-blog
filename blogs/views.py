from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Blog, Category

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