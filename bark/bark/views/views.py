from bark.models import Post, Tag, UserProfile, PostTagging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bark.forms import PostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


numberOfTopPosts = 10

# Index Page
# Returns a welcome message
def index(request):

    # Create a context dictionary with the top posts.
    contextDictionary = {
        'topPosts' : Post.objects.order_by('rating')[:numberOfTopPosts]
        }

    return render(request, 'bark/index.html', contextDictionary)

def userprofile(request, username):
    try:
        print username
        user = User.objects.get(username=username)
        print user
    except:
        return render(request, 'bark/profile.html', {'NOT_FOUND' : True})

    context_dic = { }

    #Show extra options if it's the current user
    if request.user.username == username:
        context_dic['current'] =  True

    #Get all user info for the Template
    context_dic['bio'] = user.userprofile.user_tag.description
    context_dic['img'] = user.userprofile.profile_picture
    context_dic['username'] = username

    posts = Post.objects.all().filter(author=user.userprofile)[:5]

    context_dic['posts'] = posts
    context_dic['post_tags'] = { }
    rating = 0
    views = 0

    #Calculating total views and rating for the user
    for p in posts:
        rating += p.rating
        views += p.views
        context_dic['post_tags'][p.title] = p.tags

    context_dic['bark_count'] = posts.count()

    if rating == 0:
        context_dic['bark_rating'] = 0
    else:
        context_dic['bark_rating'] = rating / posts.count()

    context_dic['bark_views'] = views

    return render(request, 'bark/profile.html', context_dic)


# Bark Tag listing
def viewPosts(request, url_extra):
    contextDictionary = {}

    tag_names = url_extra.split('/')
    print tag_names

    # TODO get the posts with the tag with the given id(s)
    # contextDictionary['posts'] = Post.objects.get(tags.id=tag_id)
    return render(request, 'bark/posts.html', contextDictionary)

# View a specific bark
def viewPost(request, post_id, post_slug):
    contextDictionary = {}

    try:
        post = Post.objects.get(id=post_id)
        contextDictionary['post'] = post
        contextDictionary['post'].tags.all().exclude(name=post.author.user_tag)

    except Post.DoesNotExist:
        pass

    return render(request, 'bark/post.html', contextDictionary)


@login_required
def addPost(request):
    contextDictionary = {}

    if request.method == 'POST':
        print request.POST
        form = PostForm(request.POST)

        if form.is_valid():
            newPost = form.save(commit = False)

            authorProfile = None
            # Try and get the user profile.
            try:
                authorProfile = UserProfile.objects.get(user = request.user)
            except UserProfile.DoesNotExist:
                # TODO: Redirect the user to a meaningful "Not logged in" page?
                return redirect('index')

            newPost.author = authorProfile
            newPost.save()
            tags = request.POST.getlist('taggles[]')

            for tag in tags:
                post_tag = Tag.objects.get_or_create(name=tag)[0]
                PostTagging.objects.get_or_create(post=newPost, tag=post_tag)

            return viewPost(request, newPost.id, newPost.slug)
        else:
            print form.errors

    else:
        form = PostForm()

    contextDictionary['form'] = form

    return render(request, 'bark/addPost.html', contextDictionary)

# Search view
def search(request):
    if request.method=="POST":
        query = request.POST.get('query',None)
    else:
        query = ''

    query=query.strip()
    posts = Post.objects.filter(tag__name__contains=query)
    content = Post.objects.filter(content__contains=query)

    return render(request,'bark/search.html', {'posts':posts, 'content':content})

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

@login_required
def like_post(request):

    Post_slug = None
    if request.method == 'GET':
        Post_slug = request.GET['Post.slug']

    rating = 0
    if Post_slug:
        post = Post.objects.get(id=int(Post_slug))
        if post:
            rating = Post.rating + 1
            Post.rating =  rating
            rating.save()

    return HttpResponse(rating)

@login_required
def auto_add_page(request):
    tag_name = None
    url = None
    context_dict = {}
    if request.method == 'GET':
        tag_name = request.GET['Tag.name']
        url = request.GET['url']
        if tag_name:
            tag = Tag.objects.get(id=tag_name)
            tag.followers += 1
    return render(request, 'bark/follow.html', context_dict)

def about(request):
    context_dict={}
    return render(request,'bark/about.html',context_dict)

def help(request):
    context_dict={}
    return render(request,'bark/help.html',context_dict)
