from django.shortcuts import get_object_or_404, render, redirect
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CategoryForm, BlogForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .forms import AddUserForm


# Create your views here.

@login_required(login_url='login')
def dashboard(request) :
    allowed_groups = ['Manager', 'Editor']
    print(f"{request.user.is_superuser=}")
    # if not request.user.is_superuser or not request.user.is_staff :   #   this also works!!!
    if not ( request.user.is_superuser or request.user.groups.filter(name__in=allowed_groups).exists() ) :
        messages.warning(request, "You do not have permission to access dashboard.")
        return redirect('home')
    
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        'category_count' : category_count,
        'blogs_count' : blogs_count,
    }
    return render(request, 'dashboards/dashboard.html', context)


# Categories CRUD

@login_required(login_url='login')
def categories(request) :
    if not request.user.has_perm('blogs.view_category') :
        messages.warning(request, "You do not have permission to view Categories.")
        return redirect('home')
    
    return render(request, 'dashboards/categories.html')


@login_required(login_url='login')
def add_category(request) :
    if not request.user.has_perm('blogs.add_category') :
        messages.warning(request, "You do not have permission to add Categories.")
        return redirect('home')
    
    if request.method == 'POST' :
        form = CategoryForm(request.POST)
        if form.is_valid :
            form.save()
            messages.success(request, "Category added successfully!.")
            return redirect('categories')
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('add_category')
    form = CategoryForm()

    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_category.html', context)


@login_required(login_url='login')
def edit_category(request, pk) :
    if not request.user.has_perm('blogs.change_category') :
        messages.warning(request, "You do not have permission to change Categories.")
        return redirect('home')

    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST' :
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid() :
            form.save()
            messages.success(request, "Updated category successfully!.")
            return redirect('categories')
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('edit_category')
    form = CategoryForm(instance=category)
    print(f"{category=}")

    context = {
        'form' : form,
        'category' : category,
    }
    return render(request, 'dashboards/edit_category.html', context)


@login_required(login_url='login')
def delete_category(request, pk) :
    if not request.user.has_perm('blogs.delete_category') :
        messages.warning(request, "You do not have permission to delete Categories.")
        return redirect('home')

    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, "Category deleted successfully!.")
    return redirect('categories')


# blog posts CRUD


@login_required(login_url='login')
def posts(request) :
    if not request.user.has_perm('blogs.view_blog') :
        messages.warning(request, "You do not have permission to access dashboard.")
        return redirect('home')

    posts = Blog.objects.order_by('category')

    context = {
        'posts' : posts,
    }

    return render(request, 'dashboards/posts.html', context)


@login_required(login_url='login')
def edit_post(request, pk) :
    if not request.user.has_perm('blogs.change_blog') :
        messages.warning(request, "You do not have permission to edit post.")
        return redirect('home')

    post = get_object_or_404(Blog, pk=pk)
    print(f"{post=}")
    if request.method == 'POST' :
        form = BlogForm(request.POST, request.FILES, instance=post)
        if form.is_valid() :
            post = form.save() 
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)  # this-is-a-new-post-<pk:1>     this-is-a-new-post-<pk:2>
            post.save()
            messages.success(request, "Updated post successfully!.")
            return redirect('posts')
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('edit_post')
    form = BlogForm(instance=post)

    context = {
        'form' : form,
        'post' : post,
    }
    return render(request, 'dashboards/edit_post.html', context)


@login_required(login_url='login')
def delete_post(request, pk) :
    if not request.user.has_perm('blogs.delete_blog') :
        messages.warning(request, "You do not have permission to delete post.")
        return redirect('home')

    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    messages.success(request, "Post deleted successfully!.")
    return redirect('posts')


@login_required(login_url='login')
def add_post(request) :
    if not request.user.has_perm('blogs.add_blog') :
        messages.warning(request, "You do not have permission to add post.")
        return redirect('home')

    if request.method == 'POST' :
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid() :
            post = form.save(commit=False)  # temp saving the form
            post.author = request.user
            post.save() # we have to save cuz only then 'post.id' will be accessable
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)  # this-is-a-new-post-<pk:1>     this-is-a-new-post-<pk:2>
            post.save()
            messages.success(request, "Post added successfully!.")
            return redirect('posts')
        # else :
        #     print('\/'*20)
        #     print(f"{form.errors=}")
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('add_post')
    form = BlogForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_post.html', context)


# Users CRUD


@login_required(login_url='login')
def users(request) :
    if not request.user.has_perm('auth.view_user') :
        messages.warning(request, "You do not have permission to access dashboard.")
        return redirect('home')

    users = User.objects.all()

    context = {
        'users' : users,
    }

    return render(request, 'dashboards/users.html', context)


@login_required(login_url='login')
def add_user(request) :
    if not request.user.has_perm('auth.add_user') :
        messages.warning(request, "You do not have permission to add users.")
        return redirect('home')
    
    if request.method == 'POST' :
        form = AddUserForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request, "User added successfully!.")
            return redirect('users')
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('add_user')
    form = AddUserForm()
    context = {
        'form' : form,
    }
    return render(request, 'dashboards/add_user.html', context)


@login_required(login_url='login')
def delete_user(request, pk) :
    if not request.user.has_perm('auth.delete_user') :
        messages.warning(request, "You do not have permission to delete user.")
        return redirect('home')
    
    user = get_object_or_404(User, pk=pk)
    user.delete()
    messages.success(request, "User deleted successfully!.")
    return redirect('users')


@login_required(login_url='login')
def edit_user(request, pk) :
    if not request.user.has_perm('auth.change_user') :
        messages.warning(request, "You do not have permission to edit user.")
        return redirect('home')

    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' :
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid() :
            form.save()
            messages.success(request, "Updated User successfully!.")
            return redirect('users')
        else :
            print(f"{form.errors=}")
            messages.error(request, str(form.errors))
            return redirect('edit_user', pk)
    form = EditUserForm(instance=user)
    context = {
        'form' : form,
    }

    return render(request, 'dashboards/edit_user.html', context)