from bark.models import Post, Tag, UserProfile, PostTagging, PostLike, Comment, InstitutionTag, UserTag, CommentLike, TagFollowing
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from bark.forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from functools import reduce

import re
import operator
import unicodedata

numberOfTopPosts = 10

# Index Page
# Returns a welcome message
def index(request):
    post_list = Post.objects

    # First, check the user is logged in.
    foundUserProfile = None
    try:
        foundUserProfile = UserProfile.objects.get(user = request.user.id)

        # If the user is logged in, filter post_list by tags that the user follows.
        userTagFollowings = TagFollowing.objects.filter(user = foundUserProfile)
        userFollowedTags = [userTagFollowing.tag for userTagFollowing in userTagFollowings]

        post_list = post_list.filter(tag__name__in = userFollowedTags)
    except UserProfile.DoesNotExist:
        pass

    paginator = Paginator(post_list.order_by('-rating').distinct(), numberOfTopPosts)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # Page is out of range, deliver last page
        posts = paginator.page(paginator.num_pages)


    # Create a context dictionary with the top posts.
    contextDictionary = {
        'topPosts': posts
        }

    return render(request, 'bark/index.html', contextDictionary)

def userprofile(request, username):
    try:
        user = User.objects.get(username__iexact = username)
    except:
        return render(request, 'bark/profile.html', {'NOT_FOUND' : True})

    context_dic = { }

    #Show extra options if it's the current user
    if request.user.username == username:
        context_dic['current'] =  True

    #Get all user info for the Template
    context_dic['bio'] = user.userprofile.user_tag.description
    context_dic['img'] = user.userprofile.profile_picture
    context_dic['username'] = user.username

    context_dic['usertag'] = user.username.lower()

    posts = Post.objects.all().filter(author = user.userprofile)\
        .exclude(anonymous=True).order_by('-rating')[:numberOfTopPosts]

    context_dic['posts'] = posts
    context_dic['post_tags'] = { }
    post_likes = 0
    comment_likes = 0
    views = 0

    #Calculating total views and post likes for the user
    for p in posts:
        post_likes += p.postlike_set.count()
        views += p.views
        context_dic['post_tags'][p.title] = p.tags

    # Calculate the number of comment likes for the user
    for comment in user.userprofile.comment_set.all():
        comment_likes += comment.commentlike_set.count()

    context_dic['bark_count'] = posts.count()

    context_dic['post_likes'] = post_likes
    context_dic['comment_likes'] = comment_likes

    context_dic['bark_views'] = views

    return render(request, 'bark/profile.html', context_dic)


# Bark Tag listing
def viewPosts(request, url_extra):
    contextDictionary = {}

    tag_names = url_extra.split('/')
    if tag_names[-1] == '':
        tag_names = tag_names[:-1]

    contextDictionary['tagNames'] = tag_names

    queryResults = []
    tags = []

    if tag_names == []:
        queryResults = Post.objects.order_by('-rating')
    else:
        tags = Tag.objects.filter(name__in=tag_names)

        foundUserProfile = None
        try:
            foundUserProfile = UserProfile.objects.get(user = request.user.id)

            for tagIndex in range(0, len(tags)):
                tagFollowing = None
                try:
                    tagFollowing = TagFollowing.objects.get(user = foundUserProfile, tag = tags[tagIndex])
                except:
                    tagFollowing = None

                tags[tagIndex].followed_by_user = (tagFollowing != None)

        except UserProfile.DoesNotExist:
            # If we can't find the user profile (i.e. nobody is logged in),
            # then we just say that the "user" follows ALL the tags.
            # tagsAreFollowedByUser = [True] * len(tags)
            for tagIndex in range(0, len(tags)):
                tags[tagIndex].followed_by_user = False

        # The django.db.models.Q class is an object used
        # to encapsulate a collection of field lookups,
        # a more complex query object than a basic query.
        queryResults = Post.objects
        for tag_name in tag_names:
                if tag_name == '':
                    continue

                queryResults = queryResults.filter(tag__name=tag_name).order_by('-rating')

    paginator = Paginator(queryResults, numberOfTopPosts)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # Page is out of range, deliver last page
        posts = paginator.page(paginator.num_pages)

    contextDictionary['posts'] = posts
    contextDictionary['tags'] = tags

    return render(request, 'bark/postlist.html', contextDictionary)

# View a specific bark
def viewPost(request, post_id, post_slug):
    contextDictionary = {}

    if request.method == "GET":
        try:
            post = Post.objects.get(id=post_id)
            contextDictionary['post'] = post
            contextDictionary['post_tags'] = post.tags.exclude(name__iexact=post.author.user_tag.name
                                                               ).exclude(name__iexact=post.author.institution_tag.name)
            contextDictionary['post_likes'] = post.postlike_set.count()

            if post.tags.filter(name=post.author.institution_tag.name).exists():
                contextDictionary['post_inst_tag'] = post.author.institution_tag

            comments = post.comment_set.all()
            post.views += 1
            post.save()

            if request.user.is_authenticated():
                try:
                    user_profile = UserProfile.objects.get(user=request.user)
                    post_liked = False
                    if post.postlike_set.filter(author=user_profile).exists():
                        post_liked = True

                    contextDictionary['post_liked'] = post_liked

                    comments = post.comment_set.all()
                    for comment in comments:
                        comment.liked_by_user = False
                        if comment.commentlike_set.filter(author=user_profile).exists():
                            comment.liked_by_user = True
                except UserProfile.DoesNotExist:
                    pass
                except Comment.DoesNotExist:
                    pass

            contextDictionary['comments'] = comments

        except Post.DoesNotExist:
            pass

        form = CommentForm()

    elif request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid and request.user.is_authenticated:
            try:
                comment = form.save(commit=False)
                comment.author = UserProfile.objects.get(user=request.user)
                comment.post = Post.objects.get(id=post_id)
                comment.save()

            except Post.DoesNotExist:
                pass
            except UserProfile.DoesNotExist:
                pass

            return HttpResponseRedirect(request.get_full_path())


    contextDictionary['form'] = form
    return render(request, 'bark/postview.html', contextDictionary)


@login_required
def addPost(request, url_extra=""):
    contextDictionary = {}

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            newPost = form.save(commit=False)

            authorProfile = None
            # Try and get the user profile.
            try:
                authorProfile = UserProfile.objects.get(user = request.user)
            except UserProfile.DoesNotExist:
                # This means that the user in the site has no UserProfile- which should
                # be impossible as they should have been given one when they signed up.
                # Although it might be better if they were redirected to a meaningful error page.
                return redirect('index')

            newPost.author = authorProfile
            newPost.save()

            tags = request.POST.getlist('taggles[]')

            for tag in tags:
                if tag[-5:] == "ac.uk":
                    try:
                        inst_tag = InstitutionTag.objects.get(name=tag)
                        if authorProfile.can_post_to_inst_tag(inst_tag):
                            PostTagging.objects.get_or_create(post=newPost, tag=inst_tag)
                            contextDictionary['inst_tag'] = inst_tag
                    except InstitutionTag.DoesNotExist:
                        pass

                elif UserTag.objects.filter(name__iexact=tag).exists():
                    pass

                else:
                    post_tag = Tag.objects.get_or_create(name=tag)[0]
                    PostTagging.objects.get_or_create(post=newPost, tag=post_tag)

            return redirect(viewPost, post_id=newPost.id, post_slug=newPost.slug)
        else:
            print form.errors

    else:
        # Parse the tag names (if any), so we can autofill our
        # Taggle input field with them.
        tag_names = url_extra.split('/')
        if tag_names[-1] == '':
            tag_names = tag_names[:-1]

        form = PostForm()

        # Convert the unicode list of tag names to ASCII.
        tagNamesAsList = [normalisedString.encode('ascii', 'ignore') for normalisedString in tag_names]

        contextDictionary['defaultTagList'] = tagNamesAsList

    contextDictionary['form'] = form

    return render(request, 'bark/addPost.html', contextDictionary)

# Search view
maxNumberOfRelatedTags = 15

def search(request):
    if request.method=="POST":
        query = request.POST.get('query',None)
    else:
        query = ''

    # construct a context dictionary
    contextDictionary = {
        }

    if (query == ''):
        return render(request, 'bark/search.html', contextDictionary)

    posts = Post.objects
    # QueryAndTerms might look like ["cs", "bark", "all python"], this means
    # "cs" AND "bark" must appear, but then either of "all python" can appear.

    queryAndTerms = map(unicode.strip, query.strip().split("+"))

    for queryAndTerm in queryAndTerms:
        queryOrTerms = re.split("[| ]", queryAndTerm)

        # Posts starts out as all posts, then repeatedly gets filtered to include *any* posts
        # matching each "AND" term.
        posts = posts.filter(
            reduce(operator.or_, (Q(tag__name__icontains = queryWord) for queryWord in queryOrTerms)) |
            reduce(operator.or_, (Q(content__icontains = queryWord) for queryWord in queryOrTerms)) |
            reduce(operator.or_, (Q(title__icontains = queryWord) for queryWord in queryOrTerms))
            ).distinct().order_by('-rating')

    # This code uses the "re" regex package to split the query string into words (by any punctuation),
    # then creates a regex that will match any of these words, and then uses name__iregex to see if the tag
    # name matches any of the query words. I had to use this as so far in Django there is no __iin query
    # (a case insensitive "in" query).

    # The purpose of this variable is so if the user searches "python", the tag "python-list" will
    # be suggested, but if they search "c", the tag "computing" will not be suggested.
    minimumLengthOfTagToFlagTagsContainingIt = 2
    tagWords = [word for word in re.split("[+| ]+", query) if word != '']

    possibleMatchingTags = Tag.objects.none()
    for tagWord in tagWords:
        possibleMatchingTags |= Tag.objects.filter(name__iexact = tagWord)

        if (len(tagWord) > minimumLengthOfTagToFlagTagsContainingIt):
            possibleMatchingTags |= Tag.objects.filter(name__icontains = tagWord)

    # For matching tags, order them by how similar the length is to the query string length.
    orderedMatchingTags = sorted(
        possibleMatchingTags,
        key = lambda tag: abs(len(query) - len(tag.name)))[:maxNumberOfRelatedTags]

    contextDictionary['any_results'] = True
    contextDictionary['posts'] = posts
    contextDictionary['query'] = query
    contextDictionary['tags'] = orderedMatchingTags

    return render(request,'bark/search.html', contextDictionary)

@login_required
def like_post(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST['post_id'])
            author = UserProfile.objects.get(user=request.user)
            post = Post.objects.get(pk=post_id)

            post_like = post.postlike_set.filter(author=author)
            if post_like.exists():
                post_like.delete()
            else:
                PostLike.objects.get_or_create(author=author, post=post)

            return HttpResponse(post.postlike_set.count())
        except Post.DoesNotExist:
            pass
        return HttpResponse("Failed")

@login_required
def like_comment(request):
    if request.method == "POST":
        try:
            post_id = int(request.POST['post_id'])
            comment_num = int(request.POST['comment_num']) - 1
            author = UserProfile.objects.get(user=request.user)
            post = Post.objects.get(pk=post_id)
            comment = post.comment_set.all()[comment_num]

            comment_like = comment.commentlike_set.filter(author=author)
            if comment_like.exists():
                comment_like.delete()
            else:
                CommentLike.objects.get_or_create(author=author, comment=comment)

            return HttpResponse(comment.commentlike_set.count())
        except Post.DoesNotExist:
            pass
        except Comment.DoesNotExist:
            pass

    return HttpResponse("Failed to like comment.")


@login_required
def follow_tag(request,tagName):
    if request.method == 'GET':
        tag = Tag.objects.get(name=tagName)
        userProfile = UserProfile.objects.get(user=request.user)
        TagFollowing.objects.get_or_create(user=userProfile, tag=tag)
        referer = request.META.get('HTTP_REFERER')

    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('view_posts', tagName)

@login_required
def unfollow_tag(request, tagName):
    if request.method == 'GET':
        try:
            tag = Tag.objects.get(name=tagName)
            userProfile = UserProfile.objects.get(user=request.user)
        except (Tag.DoesNotExist, UserProfile.DoesNotExist):
            return redirect('index')

        try:
            TagFollowing.objects.get(user=userProfile, tag=tag).delete()
        except TagFollowing.DoesNotExist:
            pass

        referer = request.META.get('HTTP_REFERER')

    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect('view_posts', tagName)

def about(request):
    context_dict={}
    return render(request,'bark/about.html',context_dict)
