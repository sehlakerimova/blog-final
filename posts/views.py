from django.shortcuts import render
from django.db.models import Q 
from .models import Category, Post, Author,About, Comment,Like, Favorite,Report,Tag
from django.shortcuts import render, redirect, get_object_or_404


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:4]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.  order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post(request, slug):
    # 📌 Post-u tap
    post_obj = Post.objects.get(slug=slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    comments = post_obj.comments.filter(active=True)

    if request.method == 'POST':
        if request.user.is_authenticated:
            content = request.POST.get('content')
            if content:
                Comment.objects.create(
                    post=post_obj,
                    user=request.user,
                    content=content
                )

    context = {
        'post': post_obj,
        'latest': latest,
        'comments': comments
    }
    return render(request, 'post.html', context)



def like_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.user.is_authenticated:
        like, created = Like.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            like.delete()

    return redirect('post', slug=slug)


def favorite_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.user.is_authenticated:
        fav, created = Favorite.objects.get_or_create(
            post=post,
            user=request.user
        )

        if not created:
            fav.delete()

    return redirect('post', slug=slug)

def report_post(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST' and request.user.is_authenticated:
        reason = request.POST.get('reason')
        Report.objects.create(
            post=post,
            user=request.user,
            reason=reason
        )
    return redirect('post', slug=slug)


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.posts.all()

    return render(request, 'posts/tag_posts.html', {
        'tag': tag,
        'posts': posts
    })



def about(request):
    about = About.objects.first()
    return render(request, 'about_page.html', {
        'about': about
    })


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)



