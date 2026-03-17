from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category, PostForm
from datetime import datetime
from django.contrib.auth import get_user_model
from .models import UserForm
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.urls import reverse_lazy


def index(request):
    post_list = Post.objects.select_related('category').filter(
        is_published=True, category__is_published=True,
        pub_date__lt=datetime.now()).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def post_detail(request, id):
    post = get_object_or_404(Post.objects.select_related('category').filter(
        is_published=True, category__is_published=True,
        pub_date__lt=datetime.now()), pk=id)
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(Category.objects.filter(
        is_published=True), slug=category_slug)
    post_list = Post.objects.select_related('category').filter(
        is_published=True, category_id=category.id,
        pub_date__lt=datetime.now())
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html',
                  {'category': category, 'page_obj': page_obj})


def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    post_list = Post.objects.all().filter(
        is_published=True, category__is_published=True,
        pub_date__lt=datetime.now(), author=user.id).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html',
                  {'profile': user, 'page_obj': page_obj})


def edit_profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', {'form': form})


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('blog:index')
