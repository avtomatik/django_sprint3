from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def index(request):
    template = 'blog/index.html'
    post_list = Post.objects.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post,
        pk=pk,
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )
    context = {
        'post': post,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_list_or_404(
        Post,
        pub_date__lte=timezone.now(),
        is_published=True,
        category=category
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
