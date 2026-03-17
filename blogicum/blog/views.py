from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category, PostForm
from datetime import datetime
from django.contrib.auth import get_user_model
from .models import UserForm, CommentForm, Comment
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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
    comments = Comment.objects.all().filter(post=post).filter(
        Q(is_published=True) | Q(author_id=request.user.id)
    )
    return render(request, 'blog/detail.html',
                  {'post': post, 'form': CommentForm,
                   'comments': comments})


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
    if user.id == request.user.id:
        post_list = Post.objects.all().filter(
            author=user.id).order_by('-pub_date')
    else:
        post_list = Post.objects.all().filter(
            is_published=True, category__is_published=True,
            pub_date__lt=datetime.now(), author=user.id).order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html',
                  {'profile': user, 'page_obj': page_obj})


@login_required
def edit_profile(request):
    form = UserForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        res = form.save(commit=False)
        res.author_id = request.user.id
        res.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid() and request.user.id == post.author_id:
        res = form.save(commit=False)
        res.author_id = request.user.id
        res.save()
        return redirect('blog:post_detail', id=id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)
    if request.method == 'POST' and request.user.id == post.author_id:
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


@login_required
def add_comment(request, id):
    info = get_object_or_404(Post, pk=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = info
        comment.save()
        info.comment_count += 1
        info.save()
    return redirect('blog:post_detail', id=id)


@login_required
def edit_comment(request, post_id, com_id):
    info = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=com_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid() and request.user.id == comment.author_id:
        res = form.save(commit=False)
        res.author_id = request.user.id
        res.post = info
        res.save()
        return redirect('blog:post_detail', id=post_id)
    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment, 'post': info})


@login_required
def delete_comment(request, post_id, com_id):
    info = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=com_id)
    form = CommentForm(instance=comment)
    if request.method == 'POST' and request.user.id == comment.author_id:
        comment.delete()
        info.comment_count -= 1
        info.save()
        return redirect('blog:index')
    return render(request, 'blog/comment.html',
                  {'form': form, 'comment': comment, 'post': info})
