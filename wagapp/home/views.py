from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from taggit.models import Tag

from .models import Post, Review,Categories
from .forms import ReviewForm, SearchForm

def post_list(request):
    posts = Post.objects.all()
    tags = Tag.objects.all()
    categories = Categories.objects.all()

    post_per_page = 3
    paginator = Paginator(posts, post_per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {'posts': posts, 'page_object': page_object, 'tags': tags, 'categories':categories}
    return render(request, 'home/index.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug,)
    tags = Tag.objects.all()
    categories = Categories.objects.all()

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            data = review_form.cleaned_data
            Review.objects.create(
                post=post,
                author=data['author'],
                text=data['text'],
                rating=data['rating']
            )
        return redirect('home:post_detail', slug=post.slug)
    else:
        review_form = ReviewForm
    
    context = {'post': post,'review_form':review_form, 'tags': tags, 'categories':categories}
    return render(request, 'home/detail.html', context)

def post_filter(request, category=None, tag=None):
    posts = Post.objects.all()
    categories = Categories.objects.all()
    tags = Tag.objects.all()

    requested_category = None
    if category:
        requested_category = get_object_or_404(Categories, slug=category)
        posts = posts.filter(category__in = [requested_category])

    requested_tag = None
    if tag:
        requested_tag = get_object_or_404(Tag, slug=tag)
        posts = posts.filter(tags__in = [requested_tag])

    post_per_page = 5
    paginator = Paginator(posts, post_per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {'categories': categories, 'tags': tags, 'page_object':page_object}
    return render(request, 'home/filters.html', context)

def post_search(request,):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A', config='English') + SearchVector('body', weight='B', config='English')
            search_query = SearchQuery(query, config='English')
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector,search_query)).filter(rank__gte=0.3).order_by('-rank')

    categories = Categories.objects.all()
    tags = Tag.objects.all()
    post_per_page = 5
    paginator = Paginator(results, post_per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {'categories': categories, 'tags': tags, 'page_object':page_object}
    return render(request, 'home/post_search.html', context)