from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from .forms import CategoryForm, BlogForm
from django.template.defaultfilters import slugify

# Create your views here.

@login_required(login_url='login')
def dashboard(request) :
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count' : category_count,
        'blogs_count' : blogs_count,
    }
    return render(request, 'dashboards/dashboard.html', context)


# Categories CRUD


def categories(request) :
    return render(request, 'dashboards/categories.html')

def add_category(request) :

    if request.method == 'POST' :
        form = CategoryForm(request.POST)
        if form.is_valid :
            form.save()
            return redirect('categories')
    form = CategoryForm()

    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_category.html', context)



def edit_category(request, pk) :
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST' :
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid() :
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    print(f"{category=}")

    context = {
        'form' : form,
        'category' : category,
    }
    return render(request, 'dashboards/edit_category.html', context)


def delete_category(request, pk) :
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')


# blog posts CRUD

def posts(request) :
    posts = Blog.objects.order_by('category')

    context = {
        'posts' : posts,
    }

    return render(request, 'dashboards/posts.html', context)


def edit_post(request, pk) :
    post = get_object_or_404(Blog, pk=pk)
    print(f"{post=}")
    if request.method == 'POST' :
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid() :
            post = form.save() 
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)  # this-is-a-new-post-<pk:1>     this-is-a-new-post-<pk:2>
            post.save()
            return redirect('posts')
    form = BlogForm(instance=post)

    context = {
        'form' : form,
        'post' : post,
    }
    return render(request, 'dashboards/edit_post.html', context)


def delete_post(request, pk) :
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')



def add_post(request) :
    if request.method == 'POST' :
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid() :
            post = form.save(commit=False)  # temp saving the form
            post.author = request.user
            post.save() # we have to save cuz only then 'post.id' will be accessable
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)  # this-is-a-new-post-<pk:1>     this-is-a-new-post-<pk:2>
            post.save()
            return redirect('posts')
        else :
            print('\/'*20)
            print(f"{form.errors=}")
    form = BlogForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_post.html', context)