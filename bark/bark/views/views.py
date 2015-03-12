from bark.models import Post
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
    try:
        post = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        pass

    contextDictionary = {
        'post' : post
        }

    return render(request, 'bark/post.html', contextDictionary)

def addPost(request):
    contextDictionary = {}
    return render(request, 'bark/addPost.html', contextDictionary)

# Search view
def search(request):
    contextDictionary = {}
    return render(request, 'bark/search.html', contextDictionary)
