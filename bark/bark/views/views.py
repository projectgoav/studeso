from bark.models import Post,Tag
from django.shortcuts import render, redirect
from django.http import HttpResponse

numberOfTopPosts = 10

# Index Page
# Returns a welcome message
def index(request):

    # Create a context dictionary with the top posts.
    contextDictionary = {
        'topPosts' : Post.objects.order_by('rating')[:numberOfTopPosts]
        }

    return render(request, 'bark/index.html', contextDictionary)

# Bark Tag listing
def viewPosts(request):
    contextDictionary = {}
    return render(request, 'bark/posts.html', contextDictionary)

# View a specific bark
def viewPost(request, post_id, post_slug):
    contextDictionary = {}
    
    try:
        post = Post.objects.get(id = post_id)
        contextDictionary['post'] = post
    except Post.DoesNotExist:
        pass

    return render(request, 'bark/post.html', contextDictionary)

def addPost(request):
    contextDictionary = {}
    return render(request, 'bark/addPost.html', contextDictionary)

# Search view
def search(request):
    if request.method=="POST":
        query = request.POST['query']
    else:
        query = ''

    posts = Post.objects.filter(tags__icontains=query).order_by('-ranking')[:10]

    return render(request,'bark/search.html', {'posts':posts})

def get_tag_list(max_results=0, starts_with=''):
        tag_list = []
        if starts_with:
                tag_list = Tag.objects.filter(name__istartswith=starts_with)

        if max_results > 0:
                if len(tag_list) > max_results:
                        tag_list = tag_list[:max_results]

        return tag_list

def suggest_tags(request):
        tag_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        tag_list = get_tag_list(8, starts_with)

        return render(request, 'bark/tag_list.html', {'tag_list': tag_list })