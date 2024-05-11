from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone

from .models import Category, Post


def fetch_required(db_manager):
    # =========================================================================
    # TODO: Replace with Custom Manager
    # =========================================================================
    return db_manager.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    template = 'blog/index.html'
    FIELDS = ('author', 'category', 'location')
    post_list = fetch_required(
        Post.objects.select_related(*FIELDS)
    )[:settings.DEFAULT_LIMIT]
    context = {
        'post_list': post_list,
    }
    return render(request, template, context)


def post_detail(request, pk):
    template = 'blog/detail.html'
    post = get_object_or_404(
        fetch_required(Post.objects),
        pk=pk,
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
        category.posts.all(),
        pub_date__lte=timezone.now(),
        is_published=True,
    )
    context = {
        'category': category,
        'post_list': post_list,
    }
    return render(request, template, context)
